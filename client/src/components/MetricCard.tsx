import React from 'react';
import { LucideIcon } from 'lucide-react';
import './MetricCard.css';

interface MetricCardProps {
  title: string;
  value: number;
  unit: string;
  icon: LucideIcon;
  color: string;
}

const MetricCard: React.FC<MetricCardProps> = ({ title, value, unit, icon: Icon, color }) => {
  return (
    <div className="metric-card" style={{ borderColor: color }}>
      <div className="metric-header">
        <Icon size={24} color={color} />
        <h3>{title}</h3>
      </div>
      <div className="metric-value">
        <span className="value" style={{ color }}>{value.toFixed(1)}</span>
        <span className="unit">{unit}</span>
      </div>
    </div>
  );
};

export default MetricCard;
