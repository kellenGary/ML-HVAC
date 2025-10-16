# ML-HVAC Smart Home Display

A smart home HVAC monitoring and control system with a dark-themed Streamlit interface.

## Features

- **Real-time Monitoring**: Display current temperature and humidity readings from Bluetooth Low Energy sensor
- **Interactive Temperature Control**: Adjust target temperature with intuitive +/- buttons
- **Historical Data Visualization**: View temperature and humidity trends over time with interactive graphs
- **Dark Mode Theme**: Modern, sleek interface designed for smart home displays
- **Statistics**: View average, min, and max temperature and humidity readings

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your environment variables (create a `.env` file):
```
DEVICE_NAME=LYWSD03MMC
DEVICE_ADDRESS=YOUR_DEVICE_MAC_ADDRESS
DEVICE_ADDRESS_MACOS=YOUR_DEVICE_MAC_ADDRESS_FOR_MACOS
TEMPERATURE_HUMIDITY_UUID=ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6
```

## Usage

### Quick Start (Demo Mode)

To try the dashboard without Bluetooth hardware:

```bash
# Generate sample data
python demo.py

# Launch the dashboard
streamlit run streamlit_app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`.

### Production Mode (with Bluetooth Sensor)

#### 1. Start the sensor data collection:

```bash
python main.py
```

This will connect to your Bluetooth HVAC sensor and start collecting temperature and humidity data, storing it in `sensor_data.json`.

#### 2. Launch the Streamlit dashboard:

In a separate terminal:
```bash
streamlit run streamlit_app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`.

## Dashboard Features

### Current Status
- **Current Temperature**: Shows the latest temperature reading in both Celsius and Fahrenheit
- **Current Humidity**: Displays the current humidity percentage
- **Target Temperature**: Your desired room temperature with delta from current
- **Last Update**: Timestamp of the most recent sensor reading

### Temperature Control
Use the control buttons to adjust your target temperature:
- **❄️ --**: Decrease by 1°C
- **🔽 -**: Decrease by 0.5°C
- **🔼 +**: Increase by 0.5°C
- **🔥 ++**: Increase by 1°C

### Historical Data
- **Temperature Over Time**: Line graph showing temperature trends with target temperature indicator
- **Humidity Over Time**: Line graph showing humidity trends
- **Statistics**: Average, minimum, and maximum values

## Data Storage

The system stores sensor data in `sensor_data.json` with the following structure:
- Up to 1000 most recent readings
- Temperature (°C)
- Humidity (%)
- Timestamp
- Target temperature setting

## Architecture

- `main.py`: Main application that connects to Bluetooth sensor and collects data
- `streamlit_app.py`: Streamlit web interface for visualization and control
- `data_store.py`: JSON-based data persistence layer
- `packet_handler.py`: Bluetooth packet parsing logic
- `connection_handler.py`: Bluetooth connection management
- `packet_timer.py`: Packet timing statistics
- `contants.py`: Configuration and constants

## Notes

- The dashboard auto-refreshes every 5 seconds to show the latest data
- Make sure the sensor is running before launching the Streamlit app
- The dark mode theme is optimized for viewing on smart home displays
