import json
import os
import shutil
from jinja2 import Template

def ensure_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)

# Create necessary directories
ensure_directory("features")
ensure_directory("features/steps")
ensure_directory("tests")

# Load input data
with open("sensors_input.json", "r") as f:
    sensors = json.load(f)["sensors"]

# Load Jinja2 templates
with open("templates/gherkin_template.feature", "r") as f:
    gherkin_template = Template(f.read())

with open("templates/pytest_template.j2", "r") as f:
    pytest_template = Template(f.read())

# Create __init__.py files for proper Python packaging
for directory in ["tests", "features/steps"]:
    init_file = os.path.join(directory, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, "w") as f:
            pass

# Copy AIO interface to tests directory
shutil.copy2("aio_interface.py", "tests/aio_interface.py")
print("✓ Copied aio_interface.py to tests directory")

# Generate environment.py for behave
environment_content = """from tests.aio_interface import AIOSensorInterface

def before_scenario(context, scenario):
    context.aio_interface = AIOSensorInterface()
"""

with open("features/environment.py", "w") as f:
    f.write(environment_content)

# Generate files for each sensor
for sensor in sensors:
    sensor_name = sensor["name"]
    test_cases = list(zip(sensor["values"], sensor["conditions"], sensor["expected_results"]))

    # Generate Gherkin feature file
    feature_content = gherkin_template.render(
        sensor_name=sensor_name,
        test_cases=test_cases
    )
    with open(f"features/{sensor_name}.feature", "w") as f:
        f.write(feature_content)

    # Generate pytest script
    pytest_content = pytest_template.render(
        sensor_name=sensor_name,
        test_cases=test_cases
    )
    with open(f"tests/test_{sensor_name}.py", "w") as f:
        f.write(pytest_content)

print("Test files generated successfully!")
print("\nDirectory structure created:")
print("aio_bdd_framework/")
print("├── features/")
print("│   ├── environment.py")
print("│   ├── steps/")
print("│   │   ├── __init__.py")
print("│   │   └── sensor_steps.py")
print("│   ├── occupant_detection.feature")
print("│   ├── posture_sensor.feature")
print("│   └── size_sensor.feature")
print("├── tests/")
print("│   ├── __init__.py")
print("│   ├── aio_interface.py  <- Copied from root")
print("│   ├── test_occupant_detection.py")
print("│   ├── test_posture_sensor.py")
print("│   └── test_size_sensor.py")
print("├── templates/")
print("│   ├── gherkin_template.feature")
print("│   └── pytest_template.py")
print("├── aio_interface.py")
print("├── sensors_input.json")
print("├── generate_tests.py")
print("└── requirements.txt")