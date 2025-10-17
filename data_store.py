import duckdb
import time


class DataStore:
    def __init__(self) -> None:
        # Initialize DuckDB and create a database for HVAC data
        # Use IF NOT EXISTS so re-running the script doesn't error
        self.conn = duckdb.connect('HVAC_Data.duckdb')
        # create tables if they don't exist
        self.conn.execute('CREATE TABLE IF NOT EXISTS sensor_readings (timestamp DOUBLE, temperature DOUBLE, humidity INTEGER);')
        self.conn.execute('CREATE TABLE IF NOT EXISTS actions (timestamp DOUBLE, action_name VARCHAR, target_temp DOUBLE);')

    def write_packet(self, timeStamp, temperature, humidity) -> None:
        # write a sensor reading
        self.conn.execute('INSERT INTO sensor_readings (timestamp, temperature, humidity) VALUES (?, ?, ?);', (timeStamp, temperature, humidity))

    def write_action(self, actionTimeStamp, action_name, target_temp) -> None:
        # write action data
        self.conn.execute('INSERT INTO actions (timestamp, action_name, target_temp) VALUES (?, ?, ?);', (actionTimeStamp, action_name, target_temp))

    def read_packets(self):
        # return up to 100 sensor readings
        cur = self.conn.execute('SELECT * FROM sensor_readings ORDER BY timestamp LIMIT 100;')
        return cur.fetchall()

    def read_actions(self):
        # return all actions
        cur = self.conn.execute('SELECT * FROM actions ORDER BY timestamp;')
        return cur.fetchall()

    def write_dummy_data(self, sensor_count: int = 10, action_count: int = 5) -> None:
        # write some dummy data for testing
        for i in range(sensor_count):
            self.write_packet(time.time(), 20.0 + i, 50 + i)
            # tiny pause to ensure different timestamps when needed
            time.sleep(0.01)
        for i in range(action_count):
            self.write_action(time.time(), f"Action_{i}", 22.0 + i)
            time.sleep(0.01)


def main():
    ds = DataStore()
    print('Writing dummy data...')
    ds.write_dummy_data()
    print('\nSensor readings (up to 100):')
    packets = ds.read_packets()
    for row in packets:
        print(row)

    print('\nActions:')
    actions = ds.read_actions()
    for row in actions:
        print(row)


if __name__ == "__main__":
    main()