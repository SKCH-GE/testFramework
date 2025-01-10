class AIOSensorInterface:
    def __init__(self):
        self.sensor_states = {}

    def process_sensor_input(self, sensor_id, value, unit):
        """
        Process sensor input and return status based on validation rules
        """
        if sensor_id == "occupant_detection":
            return self._validate_occupant_detection(value)
        elif sensor_id == "posture_sensor":
            return self._validate_posture(value)
        elif sensor_id == "size_sensor":
            return self._validate_size(value, unit)
        else:
            return {"status": "invalid_sensor"}

    def _validate_occupant_detection(self, value):
        try:
            value = int(value)
            if value == 1:
                return {"status": "detected"}
            elif value == 0:
                return {"status": "not_detected"}
            return {"status": "invalid_value"}
        except ValueError:
            return {"status": "invalid_value"}

    def _validate_posture(self, value):
        if value in ["upright", "slouched"]:
            return {"status": "valid"}
        return {"status": "invalid_value"}

    def _validate_size(self, value, unit):
        try:
            value = float(value)
            if unit == "cm" and 0 <= value <= 200:  # Reasonable range for human size
                return {"status": "valid"}
            return {"status": "faulty"}
        except ValueError:
            return {"status": "faulty"}