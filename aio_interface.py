import json
class AIOSensorInterface:
    def __init__(self, config_path="sensors_input.json"):
        with open(config_path, "r") as f:
            self.sensor_config = {sensor['name']: sensor for sensor in json.load(f)["sensors"]}

    def process_sensor_input(self, sensor_id, value, unit):
        if sensor_id not in self.sensor_config:
            return {"status": "invalid_sensor"}

        sensor = self.sensor_config[sensor_id]
        if str(value) in sensor["values"] and unit in sensor["conditions"]:
            return {"status": sensor["expected_results"][sensor["values"].index(str(value))]}
        return {"status": "invalid_value"}
