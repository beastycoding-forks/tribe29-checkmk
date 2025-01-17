#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from cmk.base.check_api import LegacyCheckDefinition
from cmk.base.check_legacy_includes.hp_msa import parse_hp_msa
from cmk.base.config import check_info

# <<<hp_msa_fan>>>
# fan 1 durable-id fan_1.1
# fan 1 name Fan Loc:left-PSU 1
# fan 1 location Enclosure 1 - Left
# fan 1 status Up
# fan 1 status-numeric 0
# fan 1 speed 3760
# fan 1 position Left
# fan 1 position-numeric 0
# fan 1 serial-number
# fan 1 fw-revision
# fan 1 hw-revision
# fan 1 health OK
# fan 1 health-numeric 0
# fan 1 health-reason
# fan 1 health-recommendation
# fan 2 durable-id fan_1.2
# fan 2 name Fan Loc:right-PSU 2
# fan 2 location Enclosure 1 - Right
# fan 2 status Up
# fan 2 status-numeric 0
# fan 2 speed 3880
# fan 2 position Right
# fan 2 position-numeric 1
# fan 2 serial-number
# fan 2 fw-revision
# fan 2 hw-revision
# fan 2 health OK
# fan 2 health-numeric 0
# fan 2 health-reason
# fan 2 health-recommendation

hp_msa_state_numeric_map = {
    "0": (0, "up"),
    "1": (2, "error"),
    "2": (1, "off"),
    "3": (3, "missing"),
}

hp_msa_health_state_numeric_map = {
    "0": (0, "OK"),
    "1": (1, "degraded"),
    "2": (2, "fault"),
    "3": (2, "N/A"),
    "4": (3, "unknown"),
}


def inventory_hp_msa_fan(parsed):
    for item in parsed:
        yield item, None


def check_hp_msa_fan(item, params, parsed):
    if item in parsed:
        fan_speed = int(parsed[item]["speed"])
        fan_state, fan_state_readable = hp_msa_state_numeric_map[parsed[item]["status-numeric"]]
        fan_health_state, fan_health_state_readable = hp_msa_health_state_numeric_map[
            parsed[item]["health-numeric"]
        ]
        fan_health_reason = parsed[item].get("health-reason", "")

        yield fan_state, f"Status: {fan_state_readable}, speed: {fan_speed} RPM"

        if fan_health_state and fan_health_reason:
            yield fan_health_state, "health: {} ({})".format(
                fan_health_state_readable,
                fan_health_reason,
            )


check_info["hp_msa_fan"] = LegacyCheckDefinition(
    parse_function=parse_hp_msa,
    service_name="Fan %s",
    discovery_function=inventory_hp_msa_fan,
    check_function=check_hp_msa_fan,
)
