import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor, switch
from esphome.const import CONF_ID, CONF_NAME

cc1101_ns = cg.esphome_ns.namespace("cc1101")
CC1101Component = cc1101_ns.class_("CC1101Component", cg.Component)
CC1101TxSwitch = cc1101_ns.class_("CC1101TxSwitch", switch.Switch)

CONF_RX_SENSOR = "rx_sensor"
CONF_TX_SWITCH = "tx_switch"

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(CC1101Component),
    cv.Optional(CONF_RX_SENSOR): text_sensor.text_sensor_schema(CONF_NAME),
    cv.Optional(CONF_TX_SWITCH): switch.switch_schema(CONF_NAME),
})

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    if CONF_RX_SENSOR in config:
        sens = await text_sensor.new_text_sensor(config[CONF_RX_SENSOR])
        cg.add(var.rx_sensor.set_parent(sens))

    if CONF_TX_SWITCH in config:
        sw = await switch.new_switch(config[CONF_TX_SWITCH])
        cg.add(sw.set_parent(var))
