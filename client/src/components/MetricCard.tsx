import React from 'react';
import { LucideIcon } from 'lucide-react';
import './MetricCard.css';

interface MetricCardProps {
  title: string;
  value: number;
  unit: string;
  icon: LucideIcon;
  color?: string;
  subtitle?: string;
}

const MetricCard: React.FC<MetricCardProps> = ({ title, value, unit, icon: Icon, color = '#ffffff', subtitle }) => {
  return (
    <div className="metric-card">
      <div className="metric-value">
        <Icon size={32} color={color} style={{ marginRight: 12, marginTop: 12 }} />
        <span className="value">{value.toFixed(0)}</span>
        <span className="unit">{unit}</span>
      </div>
      <div className="metric-header">
        <h3>{title}</h3>
        {subtitle && <span className="metric-subtitle" style={{ color: color !== '#ffffff' ? color : '#ff9500' }}>{subtitle}</span>}
      </div>
    </div>
  );
};

export default MetricCard;
