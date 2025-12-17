#pragma once
#include "esphome/core/component.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "esphome/components/switch/switch.h"
#include <RadioLib.h>

namespace esphome {
namespace cc1101 {

struct CC1101Config {
  int cs_pin;
  int gdo0_pin;
  int gdo2_pin;
  float frequency;
  std::string modulation;     // "OOK" oder "FSK"
  float bitrate_kbps;
  float rx_bandwidth_khz;
  int tx_power_dbm;
};

class CC1101Component : public Component {
 public:
  CC1101Config cfg;
  text_sensor::TextSensor *rx_sensor{nullptr};
  switch_::Switch *tx_switch{nullptr};

  void setup() override;
  void loop() override;
  void dump_config() override;

 protected:
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
