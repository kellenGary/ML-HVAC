import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './HistoryChart.css';

interface DataPoint {
  timestamp: string;
  temperature: number;
  humidity: number;
}

interface HistoryChartProps {
  data: DataPoint[];
}

const HistoryChart: React.FC<HistoryChartProps> = ({ data }) => {
  return (
    <div className="history-chart">
      <h2>24-Hour History</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis
            dataKey="timestamp"
            stroke="#888"
            style={{ fontSize: '12px' }}
            tick={{ fill: '#888' }}
          />
          <YAxis
            yAxisId="left"
            stroke="#ffffff"
            style={{ fontSize: '12px' }}
            tick={{ fill: '#888' }}
            label={{ value: 'Temperature (°F)', angle: -90, position: 'insideLeft', fill: '#888' }}
          />
          <YAxis
            yAxisId="right"
            orientation="right"
            stroke="#ff9500"
            style={{ fontSize: '12px' }}
            tick={{ fill: '#888' }}
            label={{ value: 'Humidity (%)', angle: 90, position: 'insideRight', fill: '#888' }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1a1a1a',
              border: '1px solid #333',
              borderRadius: '4px',
              padding: '12px',
              color: '#fff'
            }}
            itemStyle={{ color: '#fff' }}
            labelStyle={{ color: '#888' }}
          />
          <Legend wrapperStyle={{ color: '#fff' }} />
          <Line
            yAxisId="left"
            type="monotone"
            dataKey="temperature"
            stroke="#ffffff"
            activeDot={{ r: 8 }}
            name="Temperature"
          />
          <Line
            yAxisId="right"
            type="monotone"
            dataKey="humidity"
            stroke="#ff9500"
            name="Humidity"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default HistoryChart;
