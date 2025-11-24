const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface CurrentData {
  temperature: number;
  humidity: number;
}

export interface HistoryDataPoint {
  timestamp: string;
  temperature: number;
  humidity: number;
}

export interface DeviceState {
  on: boolean;
  level?: number;
}

export const hvacApi = {
  async getCurrentData(): Promise<CurrentData> {
    const response = await fetch(`${API_BASE_URL}/api/current`);
    if (!response.ok) throw new Error('Failed to fetch current data');
    return response.json();
  },

  async getHistoryData(hours: number = 24): Promise<HistoryDataPoint[]> {
    const response = await fetch(`${API_BASE_URL}/api/history/${hours}h`);
    if (!response.ok) throw new Error('Failed to fetch history data');
    return response.json();
  },

  async setDeviceState(device: string, state: DeviceState): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/api/devices/${device}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(state),
    });
    if (!response.ok) throw new Error(`Failed to set ${device} state`);
  },

  async setDeviceLevel(device: string, level: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/api/devices/${device}/level`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ level }),
    });
    if (!response.ok) throw new Error(`Failed to set ${device} level`);
  },
};
