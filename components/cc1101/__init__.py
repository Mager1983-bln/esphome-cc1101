import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor, switch
from esphome.const import CONF_ID

cc1101_ns = cg.esphome_ns.namespace("cc1101")
CC1101Component = cc1101_ns.class_("CC1101Component", cg.Component)
CC1101TxSwitch = cc1101_ns.class_("CC1101TxSwitch", switch.Switch)

# Basis-Schema für die Komponente
CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(CC1101Component),
})

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

# TextSensor-Registrierung
TEXT_SENSOR_SCHEMA = text_sensor.text_sensor_schema().extend({
    cv.GenerateID(): cv.declare_id(CC1101Component),
})

@text_sensor.register("cc1101", TEXT_SENSOR_SCHEMA)
async def text_sensor_to_code(config):
    parent = await cg.get_variable(config[CONF_ID])
    sens = await text_sensor.new_text_sensor(config)
    cg.add(parent.rx_sensor.set_parent(sens))

# Switch-Registrierung
SWITCH_SCHEMA = switch.switch_schema(CC1101TxSwitch).extend({
    cv.GenerateID(): cv.declare_id(CC1101Component),
})

@switch.register("cc1101", SWITCH_SCHEMA)
async def switch_to_code(config):
    parent = await cg.get_variable(config[CONF_ID])
    sw = await switch.new_switch(config)
    cg.add(sw.set_parent(parent))


