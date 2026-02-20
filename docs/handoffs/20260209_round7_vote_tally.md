# Round 7 Vote Tally

## Input Summary
- Valid ballots: `5`
- Parsing/validation errors: `1`

### Invalid Ballots
- 20260209_claude_counterfactual_ballot.json: missing agent

## Weight Table
- `claude`: `1.0`
- `deepseek`: `0.8`
- `gemini`: `0.9`
- `human_expert`: `1.0`
- `kimi`: `0.6`
- `trae`: `0.75`

## Proposal Scores
| Proposal | Weighted Total | Approve | Reject | Abstain |
|---|---:|---:|---:|---:|
| `P3` | `9.5800` | `4` | `0` | `1` |
| `P4` | `7.5600` | `2` | `1` | `2` |
| `P2` | `3.5900` | `2` | `0` | `3` |
| `P1` | `-3.7600` | `0` | `3` | `2` |

## Decision Gate
- Tentative winner: `P3`
- High-cap unresolved blockers >= 2: `True`
- Unresolved high-cap blockers:
  - `claude` -> `BLK-C01`
  - `claude` -> `BLK-C02`
  - `deepseek` -> `BK-D01`
  - `gemini` -> `BLK-G01`
  - `gemini` -> `BLK-G02`

- Final status: `HOLD` (gate triggered).

## Contributor Detail
### P3
- `claude` vote=`abstain` score=`3.0` conf=`0.55` weight=`1.0` contrib=`0.0`
- `deepseek` vote=`approve` score=`4.0` conf=`0.8` weight=`0.8` contrib=`2.56`
- `gemini` vote=`approve` score=`4.0` conf=`0.8` weight=`0.9` contrib=`2.88`
- `kimi` vote=`approve` score=`4.0` conf=`0.85` weight=`0.6` contrib=`2.04`
- `trae` vote=`approve` score=`4.0` conf=`0.7` weight=`0.75` contrib=`2.1`
### P4
- `claude` vote=`approve` score=`5.0` conf=`0.9` weight=`1.0` contrib=`4.5`
- `deepseek` vote=`abstain` score=`3.0` conf=`0.55` weight=`0.8` contrib=`0.0`
- `gemini` vote=`approve` score=`5.0` conf=`1.0` weight=`0.9` contrib=`4.5`
- `kimi` vote=`reject` score=`3.0` conf=`0.8` weight=`0.6` contrib=`-1.44`
- `trae` vote=`abstain` score=`2.0` conf=`0.5` weight=`0.75` contrib=`0.0`
### P2
- `claude` vote=`abstain` score=`4.0` conf=`0.65` weight=`1.0` contrib=`0.0`
- `deepseek` vote=`approve` score=`4.0` conf=`0.7` weight=`0.8` contrib=`2.24`
- `gemini` vote=`abstain` score=`3.0` conf=`0.5` weight=`0.9` contrib=`0.0`
- `kimi` vote=`abstain` score=`4.0` conf=`0.6` weight=`0.6` contrib=`0.0`
- `trae` vote=`approve` score=`3.0` conf=`0.6` weight=`0.75` contrib=`1.35`
### P1
- `claude` vote=`reject` score=`2.0` conf=`0.8` weight=`1.0` contrib=`-1.6`
- `deepseek` vote=`abstain` score=`2.0` conf=`0.65` weight=`0.8` contrib=`0.0`
- `gemini` vote=`reject` score=`1.0` conf=`1.0` weight=`0.9` contrib=`-0.9`
- `kimi` vote=`reject` score=`3.0` conf=`0.7` weight=`0.6` contrib=`-1.26`
- `trae` vote=`abstain` score=`2.0` conf=`0.5` weight=`0.75` contrib=`0.0`
