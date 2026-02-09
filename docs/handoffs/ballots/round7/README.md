# Round 7 Ballots

Folder ini berisi ballot JSON dari tiap agent.

## Naming
- `docs/handoffs/ballots/round7/20260209_<agent>_round7_ballot.json`

## Minimal Agent Set
- Wajib minimal 4 ballot valid.
- Disarankan: `claude`, `gemini`, `deepseek`, `kimi`, plus `trae` opsional.

## Tally
```powershell
python scripts/tally_round7_votes.py `
  --ballots-dir docs/handoffs/ballots/round7 `
  --output docs/handoffs/20260209_round7_vote_tally.md
```
