# Energy Monitoring with InfluxDB

## Overview
This Python script collects power consumption data from an InfluxDB database, processes it, and stores the cumulative energy consumption back into the database. The script is designed to monitor two metrics:
1. **Feed-in energy** (`feed`)
2. **Photovoltaic (PV) energy** (`pv`)

The script calculates the total energy consumed over time using the trapezoidal rule and stores the results back in the InfluxDB bucket for further analysis or visualization.

## Prerequisites
Before running this script, ensure that you have:
- Python installed (version 3.8 or above recommended)
- The `influxdb-client` Python package installed
- An InfluxDB instance running and accessible
- Appropriate access credentials (bucket, organization, token, and URL)

### Required Python Package
To install the required `influxdb-client` package, run:

```bash
pip install influxdb-client
```

## Configuration
In the script, you will need to configure the following parameters with your InfluxDB credentials:

```python
bucket = "BUCKETNAME"
org = "ORGNAME"
token = "your_influxdb_token"
url = "your-url-to-influxDB"
```

Make sure to replace these values with your actual InfluxDB settings.

## How It Works
1. **Initialization**:
   - The script connects to your InfluxDB instance using the provided credentials.
   - It initializes variables for storing the total energy consumption (`feed` and `pv`) and keeps track of the previous wattage values and timestamps.

2. **Reading Wattage Data**:
   - The function `read_average_wattage()` queries the InfluxDB database for the average wattage over the past 120 seconds for the specified measurement and field.
   - It returns the average wattage and the most recent timestamp.

3. **Processing Energy Consumption**:
   - The `process_energy()` function calculates the energy consumed using the trapezoidal rule:
     - It calculates the time difference between the current and previous timestamp.
     - It uses the previous and current wattage readings to estimate energy consumption over that interval.
   - The cumulative energy is stored in the `total_energy` dictionary and written back to InfluxDB.

4. **Continuous Monitoring**:
   - The script continuously monitors the energy usage, updating the total consumption every 30 seconds.

## Usage
To run the script, simply execute:

```bash
python energy_monitor.py
```

The script will print real-time updates to the console, such as:

```
Total energy for feed is: 92.642389 kWh
Current wattage for feed is: 1500.00 W
Total energy for pv is: 190.316559 kWh
Current wattage for pv is: 3500.00 W
```

## Example Output
- **Feed-in Energy**: Displays the total feed-in energy (kWh) and current feed-in wattage (W).
- **PV Energy**: Displays the total PV energy (kWh) and current PV wattage (W).

## Notes
- The script uses a 30-second interval (`time.sleep(30)`) for updating data. You can adjust this interval to suit your needs.
- Ensure your InfluxDB instance is accessible and that the measurements and fields specified in the script match your database schema.
- Be mindful of your InfluxDB token security—avoid sharing sensitive credentials in public repositories.

## Future Improvements
- Add error handling for network failures or InfluxDB connection issues.
- Implement logging instead of print statements for better monitoring.
- Optimize the query interval to reduce database load if necessary.

## License
This project is licensed under the MIT License.

---

Feel free to modify the script or extend its functionality to suit your specific needs.
