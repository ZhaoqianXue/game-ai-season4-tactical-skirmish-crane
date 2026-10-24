# Season 4: Zone and Support

## Design goal

The army should keep a presence in the capture zone while footmen protect nearby archers. Cavalry should switch between taking ground and supported attacks, rather than rushing ahead alone.

Rating question: **How clearly did the army change between capturing the zone, protecting nearby allies, and supported attacks as the battle changed?**

## Design and Season 3 revision

Season 3 finished first on the automated leaderboard (mean 63.05), with a human rating of 3.7 from six peers. Comments praised grouping but criticized unsupported cavalry charges, uneven infantry screens, and inconsistent use of terrain.

This agent starts from the official Banner example. Its tactical blocks remain recognizable, but `assign` now runs on every activation:

- The only visible friendly zone holder keeps capturing instead of leaving to escort.
- Footmen brace when locally outnumbered; rear-numbered footmen can screen a threatened nearby archer when the zone already has cover.
- Archers kite, with a low-health retreat when melee gets close.
- Cavalry first helps establish zone cover. It charges only when visible allies near the proposed landing can match the estimated threats; otherwise it holds near the zone.
- A reverse terrain-distance map helps the advance and capture blocks find crossings. Legal moves and targets always come from the action mask.

Short messages report actual block changes, no more frequently than every three rounds. They make the policy easier to inspect in a replay; units do not treat them as shared omniscient orders.

A full multi-round simulator was considered but not used. This policy uses local counts and a one-activation threat estimate to keep decisions cheap. The estimate ignores unseen enemies and the exact shuffled activation order. Protecting the zone can also delay a promising attack, and the original shield-wall and kiting blocks are still imperfect.

## Verification

The official `season.json` enables the army roster, field extent 12, terrain, abilities, and one capture zone. The round cap and capture target use the official defaults.

- Untouched Banner: 145 tests passed; seeds 0–4 against Naive scored 100.00 from each side.
- Revised agent: 148 tests passed, including three new assignment regressions and the existing mask-legality checks. Seeds 0–4 against Naive again scored 100.00 from each side.
- `python verify_roles.py`: fixed Banner assignment and revised assignment, using the same blocks, each scored 100 on seeds 0, 11, and 23 from both sides. The revised policy changed jobs for 8–11 units per match; the fixed policy changed none.
- In seed 23 as Red, footman 4 changed from capture to screen in round 8 and returned to capture in round 9. Footman 1 changed from capture to shield wall in round 6.

These results demonstrate reassignment, not a score improvement over a baseline already at the ceiling. Naive is a weak opponent, and these local results do not predict classmates' armies or the leaderboard.

Run from this folder:

```console
python -m sandbox test
python -m sandbox eval
python -m sandbox eval --seat 1
python verify_roles.py
python -m sandbox watch --seed 23
```

## AI-use disclosure and reflection

OpenAI Codex read the assignment and peer feedback, adapted Banner's assignment and movement policy, wrote the regression tests and comparison script, ran local checks, and drafted this README. No Claude or other coding agent was used for this season. The agent makes no LLM API calls.

Checks included the supplied suite, constructed assignment cases, both-side seeded evaluation, and actual role-change traces. An early regression in games without capture zones was caught and fixed by retaining Banner's original assignment there. Coding assistance made it easy to add rules, but the tests were needed to separate intended coordination from behavior that actually occurred. Scores alone could not establish that distinction.

The official `sandbox/`, manifest, and dependency files are unchanged. The inherited Banner blocks and framework remain credited to the course template.
