import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from esphome.const import CONF_ID

cc1101_ns = cg.esphome_ns.namespace("cc1101")
CC1101Component = cc1101_ns.class_("CC1101Component", cg.Component)

CONFIG_SCHEMA = text_sensor.text_sensor_schema().extend({
    cv.GenerateID(): cv.declare_id(CC1101Component),
})

async def to_code(config):
    parent = await cg.get_variable(config[CONF_ID])
    sens = await text_sensor.new_text_sensor(config)
    cg.add(parent.rx_sensor = sens)
