import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import DEVICE_CLASS_RUNNING
from . import ECODAN, CONF_ECODAN_ID

AUTO_LOAD = ["ecodan"]


def running(icon):
    return binary_sensor.binary_sensor_schema(device_class=DEVICE_CLASS_RUNNING, icon=icon)


CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_ECODAN_ID): cv.use_id(ECODAN),
        cv.Optional("compressor"): running("mdi:heat-pump"),
        cv.Optional("booster_heater"): running("mdi:heating-coil"),
        cv.Optional("booster_heater_2"): running("mdi:heating-coil"),
        cv.Optional("immersion_heater"): running("mdi:heating-coil"),
        cv.Optional("water_pump_1"): running("mdi:pump"),
        cv.Optional("water_pump_2"): running("mdi:pump"),
        cv.Optional("water_pump_3"): running("mdi:pump"),
        cv.Optional("three_way_valve"): binary_sensor.binary_sensor_schema(icon="mdi:valve"),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    heatpump = await cg.get_variable(config[CONF_ECODAN_ID])

    binary_sensors = []
    for key, conf in config.items():
        if not isinstance(conf, dict):
            continue
        var = await binary_sensor.new_binary_sensor(conf)
        cg.add(getattr(heatpump, f"set_{key}")(var))
        binary_sensors.append(f"F({key})")

    cg.add_define(
        "ECODAN_BINARY_SENSOR_LIST(F, sep)", cg.RawExpression(" sep ".join(binary_sensors))
    )
