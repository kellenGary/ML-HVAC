import duckdb

class DataStore:
    def __init__(self) -> None:
        # Initialize DuckDB and create a database for HVAC data
        # Use IF NOT EXISTS so re-running the script doesn't error
        self.conn = duckdb.connect('HVAC_Data.duckdb')
        # create tables if they don't exist
        self.conn.execute('CREATE TABLE IF NOT EXISTS sensor_readings (timestamp DOUBLE, temperature DOUBLE, humidity INTEGER);')
        self.conn.execute('CREATE TABLE IF NOT EXISTS actions (timestamp DOUBLE, action_name VARCHAR, target_temp DOUBLE);')

    def write_packet(self, timestamp, temperature, humidity) -> None:
        # write a sensor reading
        self.conn.execute('INSERT INTO sensor_readings (timestamp, temperature, humidity) VALUES (?, ?, ?);', (timestamp, temperature, humidity))

    def write_action(self, timestamp, action_name, target_temp) -> None:
        # write action data
        self.conn.execute('INSERT INTO actions (timestamp, action_name, target_temp) VALUES (?, ?, ?);', (timestamp, action_name, target_temp))

    def read_packets(self):
        # return up to 100 sensor readings
        cur = self.conn.execute('SELECT * FROM sensor_readings ORDER BY timestamp LIMIT 100;')
        return cur.fetchall()

    def read_actions(self):
        # return all actions
        cur = self.conn.execute('SELECT * FROM actions ORDER BY timestamp;')
        return cur.fetchall()
