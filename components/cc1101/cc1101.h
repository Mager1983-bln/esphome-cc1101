#pragma once
#include "esphome/core/component.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "esphome/components/switch/switch.h"
#include <RadioLib.h>

namespace esphome {
namespace cc1101 {

class CC1101Component : public Component {
 public:
  // Setter-Methoden für YAML-Werte
  void set_cs_pin(int pin) { this->cs_pin_ = pin; }
  void set_gdo0_pin(int pin) { this->gdo0_pin_ = pin; }
  void set_gdo2_pin(int pin) { this->gdo2_pin_ = pin; }
  void set_frequency(float freq) { this->frequency_ = freq; }
  void set_modulation(const std::string &mod) { this->modulation_ = mod; }
  void set_bitrate(float bitrate) { this->bitrate_kbps_ = bitrate; }
  void set_bandwidth(float bw) { this->rx_bandwidth_khz_ = bw; }
  void set_tx_power(int power) { this->tx_power_dbm_ = power; }

  void set_rx_sensor(text_sensor::TextSensor *sens) { this->rx_sensor_ = sens; }
  void set_tx_switch(switch_::Switch *sw) { this->tx_switch_ = sw; }

  // Standard-ESPHome Methoden
  void setup() override;
  void loop() override;
  void dump_config() override;

  // Zugriff für Switch
  CC1101 *radio() const { return this->radio_; }

 protected:
  // Konfigurationswerte
  int cs_pin_{-1};
  int gdo0_pin_{-1};
  int gdo2_pin_{-1};
  float frequency_{433.92};
  std::string modulation_{"OOK"};
  float bitrate_kbps_{2.4};
  float rx_bandwidth_khz_{58.0};
  int tx_power_dbm_{10};

  // Entities
  text_sensor::TextSensor *rx_sensor_{nullptr};
  switch_::Switch *tx_switch_{nullptr};

  // RadioLib Objekte
  Module *module_{nullptr};
  CC1101 *radio_{nullptr};
};

class CC1101TxSwitch : public switch_::Switch {
 public:
  explicit CC1101TxSwitch(CC1101Component *parent) : parent_(parent) {}
 protected:
  void write_state(bool state) override;
  CC1101Component *parent_;
};

}  // namespace cc1101
}  // namespace esphome
