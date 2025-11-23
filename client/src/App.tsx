import { useState, useEffect } from 'react';
import { Thermometer, Droplets, Fan, Flame, Wind } from 'lucide-react';
import MetricCard from './components/MetricCard';
import DeviceControl from './components/DeviceControl';
import HistoryChart from './components/HistoryChart';
import './App.css';

interface HistoryData {
  timestamp: string;
  temperature: number;
  humidity: number;
}

function App() {
  const [temperature, setTemperature] = useState(72.5);
  const [humidity, setHumidity] = useState(45.0);
  const [fanOn, setFanOn] = useState(false);
  const [fanLevel, setFanLevel] = useState(50);
  const [heaterOn, setHeaterOn] = useState(false);
  const [heaterLevel, setHeaterLevel] = useState(50);
  const [humidifierOn, setHumidifierOn] = useState(false);
  const [humidifierLevel, setHumidifierLevel] = useState(50);
  const [historyData, setHistoryData] = useState<HistoryData[]>([]);

  useEffect(() => {
    fetchCurrentData();
    fetchHistoryData();

    const interval = setInterval(() => {
      fetchCurrentData();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const fetchCurrentData = async () => {
    try {
      const response = await fetch('/api/current');
      const data = await response.json();
      setTemperature(data.temperature);
      setHumidity(data.humidity);
    } catch (error) {
      console.error('Error fetching current data:', error);
      setTemperature(70 + Math.random() * 10);
      setHumidity(40 + Math.random() * 20);
    }
  };

  const fetchHistoryData = async () => {
    try {
      const response = await fetch('/api/history/24h');
      const data = await response.json();
      setHistoryData(data);
    } catch (error) {
      console.error('Error fetching history data:', error);
      const mockData: HistoryData[] = [];
      const now = Date.now();
      for (let i = 24; i >= 0; i--) {
        const time = new Date(now - i * 60 * 60 * 1000);
        mockData.push({
          timestamp: time.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
          temperature: 70 + Math.random() * 10,
          humidity: 40 + Math.random() * 20,
        });
      }
      setHistoryData(mockData);
    }
  };

  const handleDeviceToggle = async (device: string, isOn: boolean) => {
    try {
      await fetch(`/api/devices/${device}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ on: !isOn }),
      });
    } catch (error) {
      console.error(`Error toggling ${device}:`, error);
    }
  };

  const handleDeviceLevel = async (device: string, level: number) => {
    try {
      await fetch(`/api/devices/${device}/level`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ level }),
      });
    } catch (error) {
      console.error(`Error setting ${device} level:`, error);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <Wind size={32} />
        <h1>HVAC Control Dashboard</h1>
      </header>

      <div className="container">
        <section className="metrics-section">
          <MetricCard
            title="Temperature"
            value={temperature}
            unit="°F"
            icon={Thermometer}
            color="#ef4444"
          />
          <MetricCard
            title="Humidity"
            value={humidity}
            unit="%"
            icon={Droplets}
            color="#3b82f6"
          />
        </section>

        <section className="controls-section">
          <h2>Device Controls</h2>
          <div className="controls-grid">
            <DeviceControl
              name="Ceiling Fan"
              icon={Fan}
              isOn={fanOn}
              onToggle={() => {
                setFanOn(!fanOn);
                handleDeviceToggle('fan', fanOn);
              }}
              color="#8b5cf6"
              level={fanLevel}
              onLevelChange={(level) => {
                setFanLevel(level);
                handleDeviceLevel('fan', level);
              }}
              hasLevel={true}
            />
            <DeviceControl
              name="Heater"
              icon={Flame}
              isOn={heaterOn}
              onToggle={() => {
                setHeaterOn(!heaterOn);
                handleDeviceToggle('heater', heaterOn);
              }}
              color="#f59e0b"
              level={heaterLevel}
              onLevelChange={(level) => {
                setHeaterLevel(level);
                handleDeviceLevel('heater', level);
              }}
              hasLevel={true}
            />
            <DeviceControl
              name="Humidifier"
              icon={Droplets}
              isOn={humidifierOn}
              onToggle={() => {
                setHumidifierOn(!humidifierOn);
                handleDeviceToggle('humidifier', humidifierOn);
              }}
              color="#06b6d4"
              level={humidifierLevel}
              onLevelChange={(level) => {
                setHumidifierLevel(level);
                handleDeviceLevel('humidifier', level);
              }}
              hasLevel={true}
            />
          </div>
        </section>

        <HistoryChart data={historyData} />
      </div>
    </div>
  );
}

export default App;
