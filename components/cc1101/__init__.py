import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor, switch
from esphome.const import (
    CONF_ID, CONF_NAME, CONF_CS_PIN,
)

cc1101_ns = cg.esphome_ns.namespace("cc1101")
CC1101Component = cc1101_ns.class_("CC1101Component", cg.Component)
CC1101TxSwitch = cc1101_ns.class_("CC1101TxSwitch", switch.Switch)

CONF_GDO0_PIN = "gdo0_pin"
CONF_GDO2_PIN = "gdo2_pin"
CONF_FREQUENCY = "frequency"
CONF_MODULATION = "modulation"
CONF_BITRATE = "bitrate_kbps"
CONF_BANDWIDTH = "rx_bandwidth_khz"
CONF_TX_POWER = "tx_power_dbm"
CONF_RX_SENSOR = "rx_sensor"
CONF_TX_SWITCH = "tx_switch"

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(CC1101Component),
    cv.Required(CONF_CS_PIN): cv.int_,
    cv.Required(CONF_GDO0_PIN): cv.int_,
    cv.Required(CONF_GDO2_PIN): cv.int_,
    cv.Required(CONF_FREQUENCY): cv.float_,
    cv.Required(CONF_MODULATION): cv.one_of("OOK", "FSK", upper=True),
    cv.Required(CONF_BITRATE): cv.float_,
    cv.Required(CONF_BANDWIDTH): cv.float_,
    cv.Required(CONF_TX_POWER): cv.int_,
    cv.Optional(CONF_RX_SENSOR): text_sensor.text_sensor_schema(CONF_NAME),
    cv.Optional(CONF_TX_SWITCH): switch.switch_schema(CONF_NAME),
})

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    cg.add(var.cfg.cs_pin = config[CONF_CS_PIN])
    cg.add(var.cfg.gdo0_pin = config[CONF_GDO0_PIN])
    cg.add(var.cfg.gdo2_pin = config[CONF_GDO2_PIN])
    cg.add(var.cfg.frequency = config[CONF_FREQUENCY])
    cg.add(var.cfg.modulation = config[CONF_MODULATION])
    cg.add(var.cfg.bitrate_kbps = config[CONF_BITRATE])
    cg.add(var.cfg.rx_bandwidth_khz = config[CONF_BANDWIDTH])
    cg.add(var.cfg.tx_power_dbm = config[CONF_TX_POWER])

    if CONF_RX_SENSOR in config:
        sens = await text_sensor.new_text_sensor(config[CONF_RX_SENSOR])
        cg.add(var.rx_sensor.set_parent(sens))

    if CONF_TX_SWITCH in config:
        sw = await switch.new_switch(config[CONF_TX_SWITCH])
        cg.add(sw.set_parent(var))
