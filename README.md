# Energy Monitoring with InfluxDB (Dockerized)

## Overview
This project is a Python script designed to monitor energy consumption using data from an InfluxDB database. It calculates cumulative energy usage for **feed-in energy** (`feed`) and **photovoltaic (PV) energy** (`pv`) using the trapezoidal rule, and stores the results back into InfluxDB. The entire application is packaged to run as a Docker container, making it easy to deploy and run on any system with Docker installed.

## Prerequisites
Before running this project, ensure you have the following installed:
- **Docker** (version 20.10 or later recommended)
- An **InfluxDB** instance running and accessible
- Python dependencies listed in the `requirements.txt` file

## Project Structure
```
├── Dockerfile
├── energy_meter.py
├── requirements.txt
└── README.md
```

### `Dockerfile`
This file is used to build a Docker image for the Python application.

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Run the script when the container launches
CMD ["python", "./energy_meter.py"]
```

### `requirements.txt`
```txt
influxdb-client
numpy
```

## Configuration
Before building and running the Docker container, you need to configure your **InfluxDB** connection details in the `energy_meter.py` file:

```python
bucket = "BUCKETNAME"
org = "ORGNAME"
token = "your_influxdb_token"
url = "your-url-to-influxdb"
```

Replace these values with your actual **bucket**, **organization**, **token**, and **InfluxDB URL**.

## Building and Running the Docker Container

### Step 1: Build the Docker Image
Open a terminal in the project directory and run the following command:

```bash
docker build -t energy-monitor .
```

This will build a Docker image named `energy-monitor`.

### Step 2: Run the Docker Container
After building the image, run the container with:

```bash
docker run -d --name energy-monitor-container energy-monitor
```

The `-d` flag runs the container in detached mode.

### Step 3: View Logs
To check if the script is running correctly, you can view the logs:

```bash
docker logs -f energy-monitor-container
```

### Step 4: Stopping the Container
To stop and remove the running container:

```bash
docker stop energy-monitor-container
docker rm energy-monitor-container
```

## How It Works
The script performs the following tasks:

1. **Connects to InfluxDB** using the provided credentials.
2. **Reads average wattage data** for the specified measurements (`feed` and `pv`) from InfluxDB.
3. **Calculates total energy consumption** using the trapezoidal rule:
   - Uses the current and previous wattage readings to estimate energy consumed during the interval.
   - Updates the total energy values for each metric (`feed` and `pv`).
4. **Writes the updated total energy** back to the InfluxDB bucket.
5. **Repeats the process every 30 seconds**.

### Console Output Example
```
Total energy for feed is: 92.642389 kWh
Current wattage for feed is: 1500.00 W
Total energy for pv is: 190.316559 kWh
Current wattage for pv is: 3500.00 W
```

## Environment Variables (Optional)
For added security, you can configure your InfluxDB credentials using environment variables in Docker:

```bash
docker run -d \
  -e INFLUX_BUCKET=BUCKETNAME \
  -e INFLUX_ORG=ORGNAME \
  -e INFLUX_TOKEN=your_influxdb_token \
  -e INFLUX_URL=your-url-to-influxdb \
  --name energy-monitor-container energy-monitor
```

In your `energy_meter.py` script, update the configuration to read from environment variables:

```python
import os

bucket = os.getenv("INFLUX_BUCKET")
org = os.getenv("INFLUX_ORG")
token = os.getenv("INFLUX_TOKEN")
url = os.getenv("INFLUX_URL")
```

## Future Improvements
- Add more robust error handling for database connectivity issues.
- Implement logging to a file for better monitoring.
- Optimize data querying intervals for better performance.

## License
This project is licensed under the MIT License.

Feel free to customize and extend the functionality of this project to fit your needs!
