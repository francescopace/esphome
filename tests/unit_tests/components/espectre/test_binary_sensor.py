"""Validation tests for ESPectre binary sensors."""

from pathlib import Path

import pytest

from esphome.config import validate_config
from esphome.core import CORE


@pytest.mark.parametrize(
    ("first", "second"),
    [("motion", "motion"), ("calibrating", "calibrating"), ("motion", "calibrating")],
)
def test_binary_sensor_uniqueness(tmp_path: Path, first: str, second: str) -> None:
    CORE.reset()
    CORE.config_path = tmp_path / "test.yaml"
    result = validate_config(
        {
            "esphome": {"name": "espectre-test"},
            "esp32": {"board": "esp32dev", "framework": {"type": "esp-idf"}},
            "wifi": {"ssid": "test", "password": "password1"},
            "espectre": {"id": "hub"},
            "binary_sensor": [
                {
                    "platform": "espectre",
                    "espectre_id": "hub",
                    first: {"name": "First"},
                },
                {"platform": "espectre", second: {"name": "Second"}},
            ],
        },
        {},
    )
    if first == second:
        assert any(f"Only one {first}" in str(e) for e in result.errors)
    else:
        assert not result.errors
