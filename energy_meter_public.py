import time
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Define your InfluxDB parameters
bucket = "BUCKETNAME" #ADJUST
org = "ORGNAME" #ADJUST
token = "add-token-here" #ADJUST
url = "add-url-here" #ADJUST

# Create a client
client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)
query_api = client.query_api()
write_api = client.write_api(write_options=SYNCHRONOUS)

# Initialize the energy variables and previous timestamps
total_energy = {
    "feed": 92.637389783472230 , #init with previous readings if available #ADJUST
    "pv": 189.916559832430720 #ADJUST
}
prev_values = {
    "feed": None,
    "pv": None
}
prev_timestamps = {
    "feed": None,
    "pv": None
}

# Function to read the average wattage from InfluxDB
def read_average_wattage(measurement, field):
    query = f'''
    from(bucket: "{bucket}")
    |> range(start: -120s)
    |> filter(fn: (r) => r._measurement == "{measurement}")
    |> filter(fn: (r) => r["_field"] == "{field}")
    |> yield(name: "mean")
    '''
    result = query_api.query(org=org, query=query)
    
    values = []
    timestamps = []

    for table in result:
        for record in table.records:
            try:
                value = float(record.get_value())
                timestamp = record.get_time()
                values.append(value)
                timestamps.append(timestamp)
            except (ValueError, TypeError):
                continue
    
    if values:
        average_value = sum(values) / len(values)
        last_timestamp = max(timestamps)
        return average_value, last_timestamp
    else:
        return None, None

def process_energy(measurement, field, total_key, unit_key):
    current_wattage, current_timestamp = read_average_wattage(measurement, field)
    if current_wattage is None or current_timestamp is None:
        print(f"No wattage data available for {total_key}; skipping this interval.")
        return
    
    if prev_timestamps[total_key] is not None and current_timestamp == prev_timestamps[total_key]:
        print(f"No new data for {total_key}; skipping calculation.")
        return

    if prev_timestamps[total_key] is not None:
        timerange = (current_timestamp - prev_timestamps[total_key]).total_seconds() / 3600000  # time difference in hours
        energy_increment = (current_wattage + prev_values[total_key]) / 2 * timerange  # Trapezoidal rule
        total_energy[total_key] += energy_increment

    prev_values[total_key] = current_wattage
    prev_timestamps[total_key] = current_timestamp
    
    # Writing the updated total energy back to InfluxDB
    point = influxdb_client.Point("EnergyMeter-JN") \
        .tag("unit", "kWh") \
        .field(unit_key, total_energy[total_key])
    write_api.write(bucket=bucket, org=org, record=point)

    print(f"Total energy for {total_key} is: {total_energy[total_key]:.6f} kWh")
    print(f"Current wattage for {total_key} is: {current_wattage:.2f} W")

while True:
    process_energy("powerfox2.0.devices.<ID>.currentFeedIn", "value", "feed", "TotalFeedIn") #ADJUST
    process_energy("mqtt.0.hms800wt2.pv_current_power", "value", "pv", "TotalPVyield")
    time.sleep(30)
