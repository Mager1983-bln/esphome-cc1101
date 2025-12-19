import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor, switch
from esphome.const import CONF_ID, CONF_NAME

cc1101_ns = cg.esphome_ns.namespace("cc1101")
CC1101Component = cc1101_ns.class_("CC1101Component", cg.Component)
CC1101TxSwitch = cc1101_ns.class_("CC1101TxSwitch", switch.Switch)

CONF_CS_PIN = "cs_pin"
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

    # ✅ Pins korrekt validieren
    cv.Required(CONF_CS_PIN): cv.pin,
    cv.Required(CONF_GDO0_PIN): cv.pin,
    cv.Required(CONF_GDO2_PIN): cv.pin,

    # ✅ Zahlen
    cv.Required(CONF_FREQUENCY): cv.float_,
    cv.Required(CONF_MODULATION): cv.one_of("OOK", "FSK", upper=True),
    cv.Required(CONF_BITRATE): cv.float_,
    cv.Required(CONF_BANDWIDTH): cv.float_,
    cv.Required(CONF_TX_POWER): cv.int_,

    # ✅ Entities
    cv.Optional(CONF_RX_SENSOR): text_sensor.text_sensor_schema(CONF_NAME),
    cv.Optional(CONF_TX_SWITCH): switch.switch_schema(CC1101TxSwitch),
})

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    # ✅ Pins
    cg.add(var.set_cs_pin(config[CONF_CS_PIN]))
    cg.add(var.set_gdo0_pin(config[CONF_GDO0_PIN]))
    cg.add(var.set_gdo2_pin(config[CONF_GDO2_PIN]))

    # ✅ Radio-Parameter
    cg.add(var.set_frequency(config[CONF_FREQUENCY]))
    cg.add(var.set_modulation(config[CONF_MODULATION]))
    cg.add(var.set_bitrate(config[CONF_BITRATE]))
    cg.add(var.set_bandwidth(config[CONF_BANDWIDTH]))
    cg.add(var.set_tx_power(config[CONF_TX_POWER]))

    # ✅ Textsensor
    if CONF_RX_SENSOR in config:
        sens = await text_sensor.new_text_sensor(config[CONF_RX_SENSOR])
        cg.add(var.set_rx_sensor(sens))

    # ✅ Switch
    if CONF_TX_SWITCH in config:
        sw = await switch.new_switch(config[CONF_TX_SWITCH])
        cg.add(var.set_tx_switch(sw))
