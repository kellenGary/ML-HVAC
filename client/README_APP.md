# HVAC Control Dashboard

A modern React application for monitoring temperature and humidity, as well as controlling HVAC devices (ceiling fan, heater, and humidifier).

## Features

- **Real-time Monitoring**: Display current temperature and humidity with beautiful metric cards
- **Device Controls**: Control ceiling fan, heater, and humidifier with ON/OFF toggles and level sliders (0-100%)
- **24-Hour History**: Interactive charts showing temperature and humidity trends over the last 24 hours
- **Modern UI**: Gradient background, smooth animations, and responsive design
- **Auto-refresh**: Data refreshes every 5 seconds automatically

## Components

- **MetricCard**: Displays temperature/humidity with icons and color-coded values
- **DeviceControl**: Interactive device controls with toggle buttons and level sliders
- **HistoryChart**: Dual-axis line chart using Recharts for 24-hour history

## Getting Started

### Installation

```bash
npm install --legacy-peer-deps
```

### Development

```bash
npm start
```

Runs the app at [http://localhost:3000](http://localhost:3000)

### Production Build

```bash
npm run build
```

### Environment Variables

Create a `.env` file based on `.env.example`:

```
REACT_APP_API_URL=http://localhost:8000
```

## API Integration

The app expects the following API endpoints:

- `GET /api/current` - Current temperature and humidity
  ```json
  {
    "temperature": 72.5,
    "humidity": 45.0
  }
  ```

- `GET /api/history/24h` - 24-hour history data
  ```json
  [
    {
      "timestamp": "10:00",
      "temperature": 72.5,
      "humidity": 45.0
    }
  ]
  ```

- `POST /api/devices/{device}` - Toggle device on/off
  ```json
  {
    "on": true
  }
  ```

- `POST /api/devices/{device}/level` - Set device level
  ```json
  {
    "level": 75
  }
  ```

Devices: `fan`, `heater`, `humidifier`

## Technologies

- React 19
- TypeScript
- Recharts (for charts)
- Lucide React (for icons)
- CSS3 (custom styling)
