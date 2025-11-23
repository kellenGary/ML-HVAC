import React from 'react';
import { LucideIcon } from 'lucide-react';
import './DeviceControl.css';

interface DeviceControlProps {
  name: string;
  icon: LucideIcon;
  isOn: boolean;
  onToggle: () => void;
  color: string;
  level?: number;
  onLevelChange?: (level: number) => void;
  hasLevel?: boolean;
}

const DeviceControl: React.FC<DeviceControlProps> = ({
  name,
  icon: Icon,
  isOn,
  onToggle,
  color,
  level = 0,
  onLevelChange,
  hasLevel = false,
}) => {
  return (
    <div className={`device-control ${isOn ? 'active' : ''}`}>
      <div className="device-header">
        <div className="device-info">
          <Icon size={32} color={isOn ? color : '#ccc'} />
          <h3>{name}</h3>
        </div>
        <button
          className={`toggle-button ${isOn ? 'on' : 'off'}`}
          onClick={onToggle}
          style={isOn ? { backgroundColor: color } : {}}
        >
          {isOn ? 'ON' : 'OFF'}
        </button>
      </div>
      {hasLevel && isOn && (
        <div className="device-level">
          <input
            type="range"
            min="0"
            max="100"
            value={level}
            onChange={(e) => onLevelChange?.(Number(e.target.value))}
            className="level-slider"
            style={{
              background: `linear-gradient(to right, ${color} ${level}%, #e0e0e0 ${level}%)`,
            }}
          />
          <span className="level-value">{level}%</span>
        </div>
      )}
    </div>
  );
};

export default DeviceControl;
