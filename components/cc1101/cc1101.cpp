#include "cc1101.h"
#include "esphome/core/log.h"

namespace esphome {
namespace cc1101 {

static const char *TAG = "cc1101";

void CC1101Component::setup() {
  // RadioLib Modulobjekt aus Pins bauen
  this->module_ = new Module(this->cfg.cs_pin, this->cfg.gdo0_pin, this->cfg.gdo2_pin);
  this->radio_ = new CC1101(this->module_);

  int state = this->radio_->begin();
  if (state != RADIOLIB_ERR_NONE) {
    ESP_LOGE(TAG, "Init fehlgeschlagen: %d", state);
    if (this->rx_sensor) this->rx_sensor->publish_state("Init-Fehler");
    return;
  }

  // Frequenz
  this->radio_->setFrequency(this->cfg.frequency);

  // Modulation
  if (this->cfg.modulation == "OOK") {
    this->radio_->setOOK(true);
  } else {
    this->radio_->setOOK(false); // FSK
  }

  // Bitrate & Bandbreite
  this->radio_->setBitRate(this->cfg.bitrate_kbps);
  this->radio_->setRxBandwidth(this->cfg.rx_bandwidth_khz);

  // Sendeleistung
  this->radio_->setOutputPower(this->cfg.tx_power_dbm);

  ESP_LOGI(TAG, "CC1101 bereit (%.2f MHz, %s)", this->cfg.frequency, this->cfg.modulation.c_str());
  if (this->rx_sensor) this->rx_sensor->publish_state("Bereit");
}

void CC1101Component::loop() {
  if (!this->radio_) return;

  // Einfacher Empfang von Payload (Demo)
  String payload;
  int state = this->radio_->receive(payload);
  if (state == RADIOLIB_ERR_NONE && payload.length() > 0) {
    ESP_LOGD(TAG, "RX: %s", payload.c_str());
    if (this->rx_sensor) this->rx_sensor->publish_state(payload.c_str());
  }
}

void CC1101Component::dump_config() {
  ESP_LOGCONFIG(TAG, "CC1101:");
  ESP_LOGCONFIG(TAG, "  CS: GPIO%d, GDO0: GPIO%d, GDO2: GPIO%d", this->cfg.cs_pin, this->cfg.gdo0_pin, this->cfg.gdo2_pin);
  ESP_LOGCONFIG(TAG, "  Freq: %.2f MHz, Mod: %s, Bitrate: %.2f kbps, BW: %.2f kHz, Pwr: %d dBm",
                this->cfg.frequency, this->cfg.modulation.c_str(),
                this->cfg.bitrate_kbps, this->cfg.rx_bandwidth_khz,
                this->cfg.tx_power_dbm);
}

void CC1101TxSwitch::write_state(bool state) {
  if (!state) return; // nur beim Einschalten senden
  if (!this->parent_ || !this->parent_->radio_) return;

  const char *msg = "ON";  // Demo: einfacher Text
  int tx = this->parent_->radio_->transmit(msg);
  if (tx == RADIOLIB_ERR_NONE) {
    ESP_LOGI(TAG, "TX OK: %s", msg);
  } else {
    ESP_LOGE(TAG, "TX Fehler: %d", tx);
  }
  // automatisch zurücksetzen
  this->publish_state(false);
}

}  // namespace cc1101
}  // namespace esphome
