import { useState } from 'react';
import { 
  Thermometer, 
  Droplets, 
  Fan, 
  Flame,
} from 'lucide-react';
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
  const [temperature] = useState(72.5);
  const [humidity] = useState(45.0);
  const [fanOn, setFanOn] = useState(false);
  const [fanLevel] = useState(50);
  const [heaterOn, setHeaterOn] = useState(false);
  const [historyData] = useState<HistoryData[]>([]);

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

  return (
    <div className="app">
      <header className="app-header">
        <h1>Services</h1>
      </header>

      <div className="container">
        <div className="dashboard-grid">
          {/* Climate Card */}
          <div className="dashboard-item">
             <MetricCard
              title="Climate"
              value={temperature}
              unit="°"
              icon={Thermometer}
              color="#ffffff"
              subtitle=""
            />
          </div>

          {/* Humidity */}
          <div className="dashboard-item">
             <MetricCard
              title="Humidity"
              value={humidity}
              unit="%"
              icon={Droplets}
              color="#ffffff"
              subtitle=""
            />
          </div>

          {/* Heater */}
          <div className="dashboard-item">
            <DeviceControl
              name="Heater"
              icon={Flame}
              isOn={heaterOn}
              onToggle={() => {
                setHeaterOn(!heaterOn);
                handleDeviceToggle('heater', heaterOn);
              }}
              subtitle={heaterOn ? 'ON' : 'OFF'}
              color="#ff3b30"
            />
          </div>

           {/* Fan Control */}
           <div className="dashboard-item">
            <DeviceControl
              name="Fan"
              icon={Fan}
              isOn={fanOn}
              onToggle={() => {
                setFanOn(!fanOn);
                handleDeviceToggle('fan', fanOn);
              }}
              subtitle={fanOn ? `${fanLevel}%` : 'OFF'}
              color="#ff9500"
            />
          </div>

        </div>
        
        {/* Chart Section */}
        <div style={{ marginTop: '20px', padding: '20px', background: '#121212', border: '1px solid #333' }}>
           <HistoryChart data={historyData} />
        </div>
      </div>
    </div>
  );
}

export default App;
