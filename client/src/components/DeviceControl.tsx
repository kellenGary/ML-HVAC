import React from 'react';
import { LucideIcon } from 'lucide-react';
import './DeviceControl.css';

interface DeviceControlProps {
  name: string;
  icon: LucideIcon;
  isOn: boolean;
  onToggle: () => void;
  color?: string;
  level?: number;
  onLevelChange?: (level: number) => void;
  hasLevel?: boolean;
  subtitle?: string;
}

const DeviceControl: React.FC<DeviceControlProps> = ({
  name,
  icon: Icon,
  isOn,
  onToggle,
  color = '#ffffff',
  subtitle
}) => {
  return (
    <div className={`device-control ${isOn ? 'active' : ''}`} onClick={onToggle}>
      <div className="device-header">
        <div className="device-info">
          <Icon size={48} color={isOn ? color : '#666'} strokeWidth={1.5} />
          <h3>{name}</h3>
          <span className="device-status" style={{ color: isOn ? '#ff9500' : '#666' }}>
            {subtitle || (isOn ? 'ON' : 'OFF')}
          </span>
        </div>
      </div>
    </div>
  );
};

export default DeviceControl;
