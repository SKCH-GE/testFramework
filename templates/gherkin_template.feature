Feature: Test {{ sensor_name }}

  {% for value, condition, result in test_cases %}
  Scenario: Validate {{ sensor_name }} with value "{{ value }}"
    Given the AIO sensor system is initialized
    When the sensor "{{ sensor_name }}" sends value "{{ value }}" in condition "{{ condition }}"
    Then the system should return "{{ result }}"
  {% endfor %}