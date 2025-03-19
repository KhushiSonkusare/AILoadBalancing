from flask import Flask, jsonify, request
import psutil
import time
from influxdb import InfluxDBClient
import csv
from datetime import datetime
import os
import platform
import random
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

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
    disk_usage = psutil.disk_usage('/')
    disk_io = psutil.disk_io_counters()
    net_io = psutil.net_io_counters()
    uptime = time.time() - psutil.boot_time()
    process_count = len(psutil.pids())
    thread_count = psutil.Process().num_threads()
    
    temperatures = psutil.sensors_temperatures() if hasattr(psutil, 'sensors_temperatures') else {}
    cpu_temp = 0.0
    if temperatures:
        for name, entries in temperatures.items():
            if entries:
                cpu_temp = entries[0].current
                break
    
    load_avg_1 = load_avg_5 = load_avg_15 = 0.0
    if hasattr(os, 'getloadavg'):
        load_avg_1, load_avg_5, load_avg_15 = os.getloadavg()

    return {
        "disk_usage_percent": disk_usage.percent,
        "disk_read_bytes": disk_io.read_bytes,
        "disk_write_bytes": disk_io.write_bytes,
        "network_sent_bytes": net_io.bytes_sent,
        "network_recv_bytes": net_io.bytes_recv,
        "uptime_seconds": uptime,
        "process_count": process_count,
        "thread_count": thread_count,
        "cpu_temperature": cpu_temp,
        "load_avg_1m": load_avg_1,
        "load_avg_5m": load_avg_5,
        "load_avg_15m": load_avg_15
    }

def determine_health(cpu, memory, response_time):
    if cpu < 50 and memory < 60 and response_time < 500:
        return "Healthy"
    elif cpu < 80 and memory < 80 and response_time < 1000:
        return "Warning"
    else:
        return "Critical"

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Service 1!"})

@app.route('/process', methods=['GET'])
def process_request():
    start_time = time.time()

    # ✅ Get query params
    delay = float(request.args.get('delay', 0.5))  # default to 0.5 seconds
    request_type = request.args.get('type', 'standard')

    # Simulate variable delay
    if request_type == 'heavy':
        delay *= 2
    elif request_type == 'light':
        delay /= 2

    time.sleep(delay)

    cpu = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory().percent
    active_connections = len(psutil.net_connections())
    response_time = (time.time() - start_time) * 1000  # in ms

    health_status = determine_health(cpu, memory, response_time)
    additional_metrics = get_additional_metrics()

    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "cpu": cpu,
        "memory": memory,
        "active_connections": active_connections,
        "response_time": response_time,
        "health_status": health_status,
        "delay_used": delay,
        "request_type": request_type,
        **additional_metrics
    }

    json_body = [
        {
            "measurement": "app_metrics",
            "tags": {"app": "service1"},  # ✅ Change to service2 in service2 app
            "fields": data
        }
    ]
    client.write_points(json_body)
    log_to_csv(data)

    logging.info(f"Processed /process with delay={delay}, type={request_type}")
    return jsonify({
        "message": f"Processed by Service 1 (delay={delay}, type={request_type})",
        **data
    })

@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        time.sleep(random.uniform(0.1, 0.5))
        logging.info(f"Received POST data: {data}")

        response_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "received_data": data
        }

        return jsonify({
            "message": "Data submitted successfully!",
            **response_data
        }), 201

    except Exception as e:
        logging.error(f"Error in /submit: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True)
  # ✅ Change to port 5002 for service2