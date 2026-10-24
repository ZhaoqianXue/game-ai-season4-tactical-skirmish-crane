"""Compare assignment policies with identical blocks against Naive, both seats.

Run from this repository. No network calls; actual role-change traces come from
the private agent instances controlled in these local test matches.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "tests"))
import agent
import blocks
from test_banner import _season_4_match


class FixedBanner:
    def reset(self, seed, observation):
        self.memory = {}
        self.block = None
        self.goal = None

    def act(self, observation):
        if self.block is None:
            self.block, self.goal = blocks.banner_assign(observation, self.memory)
        return self.block(observation, self.memory, self.goal) or blocks.advance(observation, self.memory, self.goal)


if __name__ == "__main__":
    for policy, factory in (("fixed_banner_assignment", FixedBanner), ("revised_assignment", agent.Agent)):
        for blue in (False, True):
            for seed in (0, 11, 23):
                score, army = _season_4_match(seed, blue=blue, wrap=factory)
                traces = [(index, unit.memory.get("changes", [])) for index, unit in enumerate(army)
                          if len(unit.memory.get("changes", [])) > 1]
                print(json.dumps({"policy": policy, "seat": int(blue), "seed": seed,
                                  "score": score, "units_changing_jobs": len(traces),
                                  "examples": [(index, events[:8]) for index, events in traces[:3]]}), flush=True)
