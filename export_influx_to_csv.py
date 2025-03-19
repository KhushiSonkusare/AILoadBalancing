from influxdb import InfluxDBClient
import csv

# Connection parameters
INFLUX_HOST = 'localhost'  # Or 'influxdb' if you run this inside Docker
INFLUX_PORT = 8086
DATABASE = 'load_balancer_metrics'

# Connect to InfluxDB
client = InfluxDBClient(host=INFLUX_HOST, port=INFLUX_PORT)
client.switch_database(DATABASE)

# Query your measurement data
query = 'SELECT * FROM "app_metrics"'
result = client.query(query)

points = list(result.get_points())

# CSV output file path
csv_file = 'exported_metrics.csv'

# Write points to CSV
if points:
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=points[0].keys())
        writer.writeheader()
        writer.writerows(points)

    print(f"Exported {len(points)} records to {csv_file}")
else:
    print("No data found.")
