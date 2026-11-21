import esphome.codegen as cg
from esphome.components import binary_sensor
import esphome.config_validation as cv
from esphome.const import CONF_MOTION, DEVICE_CLASS_MOTION, ENTITY_CATEGORY_DIAGNOSTIC
import esphome.final_validate as fv
from esphome.types import ConfigType

from . import CONF_ESPECTRE_ID, DOMAIN, ESPectreComponent

DEPENDENCIES = ["espectre"]
CONF_CALIBRATING = "calibrating"

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(CONF_ESPECTRE_ID): cv.use_id(ESPectreComponent),
            cv.Optional(CONF_MOTION): binary_sensor.binary_sensor_schema(
                device_class=DEVICE_CLASS_MOTION
            ),
            cv.Optional(CONF_CALIBRATING): binary_sensor.binary_sensor_schema(
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC
            ),
        }
    ),
    cv.has_at_least_one_key(CONF_MOTION, CONF_CALIBRATING),
)


def _final_validate(config: ConfigType) -> None:
    hub_id = config[CONF_ESPECTRE_ID]
    entries = fv.platform_entries(
        domain=binary_sensor.DOMAIN, platform=DOMAIN, match={CONF_ESPECTRE_ID: hub_id}
    )
    for key in (CONF_MOTION, CONF_CALIBRATING):
        if key in config and sum(key in entry for entry in entries) > 1:
            raise cv.Invalid(
                f"Only one {key} binary sensor is allowed for ESPectre hub '{hub_id}'",
                path=[key],
            )


FINAL_VALIDATE_SCHEMA = _final_validate


async def to_code(config: ConfigType) -> None:
    hub = await cg.get_variable(config[CONF_ESPECTRE_ID])
    binary_sensors = binary_sensor.sub_binary_sensors(config)
    await binary_sensors(CONF_MOTION, hub.set_motion_binary_sensor)
    await binary_sensors(CONF_CALIBRATING, hub.set_calibrating_binary_sensor)
