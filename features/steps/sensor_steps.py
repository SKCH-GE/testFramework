from behave import given, when, then
from tests.aio_interface import AIOSensorInterface

@given(u'the AIO sensor system is initialized')
def step_impl(context):
    context.aio_interface = AIOSensorInterface()

@when(u'the sensor "{sensor_id}" sends value "{value}" in condition "{condition}"')
def step_impl(context, sensor_id, value, condition):
    context.result = context.aio_interface.process_sensor_input(
        sensor_id=sensor_id,
        value=value,
        unit=condition
    )

@then(u'the system should return "{expected_status}"')
def step_impl(context, expected_status):
    assert context.result["status"] == expected_status