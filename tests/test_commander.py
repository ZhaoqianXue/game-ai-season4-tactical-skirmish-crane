"""Behavioral regressions for our dynamic assignment, not a replacement for legality tests."""
import agent
import blocks
from test_banner import _observation, _visible, _zone


def test_last_zone_holder_does_not_abandon_capture():
    obs = _observation("red_footman_0", (7, 7), (),
                       (_visible("blue_cavalry_0", (9, 7), 10),),
                       zones=(_zone((7, 7)),), capture_zones=1)
    assert blocks.assign(obs, {})[0] is blocks.capture


def test_unit_reassigns_on_new_activation_and_reports_real_change():
    obs = _observation("red_archer_0", (7, 7), ((5,),),
                       (_visible("blue_cavalry_0", (8, 7), 10),),
                       zones=(_zone((7, 7)),), capture_zones=1)
    unit = agent.Agent()
    obs["observation"]["round"] = 1
    unit.reset(0, obs)
    unit.act(obs)
    assert unit.block is blocks.kite
    assert unit.chat([])
    obs["observation"]["self"]["hit_points"] = 2
    obs["observation"]["round"] = 4
    unit.act(obs)
    assert unit.block is blocks.fall_back
    assert unit.memory["changes"] == [(1, "kite"), (4, "fall_back")]
    assert "fall_back" in unit.chat([])[0]["text"]


def test_cavalry_captures_instead_of_charging_without_zone_cover():
    obs = _observation("red_cavalry_0", (3, 7), ((2, 2, 2),),
                       (_visible("blue_archer_0", (7, 7), 6),),
                       zones=(_zone((7, 7)),), capture_zones=1)
    assert blocks.assign(obs, {})[0] is blocks.capture
