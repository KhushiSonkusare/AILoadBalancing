from flask import Flask, jsonify
import psutil
import time
from influxdb import InfluxDBClient
import csv
from datetime import datetime
import os
import platform
import random

app = Flask(__name__)
client = InfluxDBClient(host='influxdb', port=8086)
client.switch_database('load_balancer_metrics')

csv_file = "/shared_data/metrics.csv"

def log_to_csv(data):
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def get_additional_metrics():
    # Disk usage
    disk_usage = psutil.disk_usage('/')
    
    # Disk I/O
    disk_io = psutil.disk_io_counters()
    
    # Network I/O
    net_io = psutil.net_io_counters()
    
    # Uptime (seconds since boot)
    uptime = time.time() - psutil.boot_time()
    
    # Number of processes
    process_count = len(psutil.pids())
    
    # Thread count (of current process)
    thread_count = psutil.Process().num_threads()
    
    # Temperature (if available)
    temperatures = psutil.sensors_temperatures() if hasattr(psutil, 'sensors_temperatures') else {}
    cpu_temp = None
    if temperatures:
        for name, entries in temperatures.items():
            if entries:
                cpu_temp = entries[0].current
                break
    
    # Load averages (only on Unix)
    if hasattr(os, 'getloadavg'):
        load_avg_1, load_avg_5, load_avg_15 = os.getloadavg()
    else:
        load_avg_1 = load_avg_5 = load_avg_15 = 0.0
    
    # Health status (random for simulation; you can base this on thresholds)
    health_status = random.choice(["Healthy", "Warning", "Critical"])
    
    return {
        "disk_usage_percent": disk_usage.percent,
        "disk_read_bytes": disk_io.read_bytes,
        "disk_write_bytes": disk_io.write_bytes,
        "network_sent_bytes": net_io.bytes_sent,
        "network_recv_bytes": net_io.bytes_recv,
        "uptime_seconds": uptime,
        "process_count": process_count,
        "thread_count": thread_count,
        "cpu_temperature": cpu_temp if cpu_temp else 0.0,
        "load_avg_1m": load_avg_1,
        "load_avg_5m": load_avg_5,
        "load_avg_15m": load_avg_15,
        "health_status": health_status
    }

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Service 1!"})

@app.route('/process', methods=['GET'])
def process_request():
    start_time = time.time()

    # Simulate processing delay
    time.sleep(random.uniform(0.2, 1.0))  # More realistic delay

    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    active_connections = len(psutil.net_connections())
    response_time = (time.time() - start_time) * 1000  # in ms
    
    # Gather additional metrics
    additional_metrics = get_additional_metrics()

    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "cpu": cpu,
        "memory": memory,
        "active_connections": active_connections,
        "response_time": response_time,
        **additional_metrics
    }

    # Send to InfluxDB
    json_body = [
        {
            "measurement": "app_metrics",
            "tags": {"app": "service1"},  # Change to service2 in service2 app
            "fields": data
        }
    ]
    client.write_points(json_body)

    # Log to CSV
    log_to_csv(data)

    return jsonify({
        "message": "Processed by Service 1",
        **data
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
