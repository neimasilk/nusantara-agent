import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple


DEFAULT_WEIGHTS: Dict[str, float] = {
    "claude": 1.00,
    "gemini": 0.90,
    "deepseek": 0.80,
    "trae": 0.75,
    "kimi": 0.60,
    "human_expert": 1.00,
}

HIGH_CAP_AGENTS = {"claude", "gemini", "deepseek"}
VALID_VOTES = {"approve", "reject", "abstain"}
VALID_PROPOSALS = {"P1", "P2", "P3", "P4"}


def _vote_sign(vote: str) -> int:
    if vote == "approve":
        return 1
    if vote == "reject":
        return -1
    return 0


def _load_ballot(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc


def _validate_ballot(ballot: dict, path: Path) -> Tuple[bool, str]:
    agent = str(ballot.get("agent", "")).strip().lower()
    votes = ballot.get("votes", [])
    if not agent:
        return False, f"{path.name}: missing agent"
    if not isinstance(votes, list) or not votes:
        return False, f"{path.name}: votes must be non-empty list"
    for item in votes:
        pid = str(item.get("proposal_id", "")).strip().upper()
        vote = str(item.get("vote", "")).strip().lower()
        score = item.get("score")
        conf = item.get("confidence")
        if pid not in VALID_PROPOSALS:
            return False, f"{path.name}: invalid proposal_id {pid}"
        if vote not in VALID_VOTES:
            return False, f"{path.name}: invalid vote {vote}"
        if not isinstance(score, (int, float)):
            return False, f"{path.name}: score must be number"
        if not isinstance(conf, (int, float)):
            return False, f"{path.name}: confidence must be number"
    return True, "ok"


def _collect_ballots(ballots_dir: Path) -> Tuple[List[dict], List[str]]:
    ballots: List[dict] = []
    errors: List[str] = []
    for path in sorted(ballots_dir.glob("*.json")):
        if path.name == "round7_ballot_template.json":
            continue
        try:
            ballot = _load_ballot(path)
            valid, msg = _validate_ballot(ballot, path)
            if not valid:
                errors.append(msg)
                continue
            ballot["_path"] = str(path)
            ballots.append(ballot)
        except ValueError as exc:
            errors.append(str(exc))
    return ballots, errors


def _aggregate(ballots: List[dict], weights: Dict[str, float]) -> Tuple[dict, dict]:
    per_proposal = {
        pid: {
            "weighted_total": 0.0,
            "approve_count": 0,
            "reject_count": 0,
            "abstain_count": 0,
            "contributors": [],
        }
        for pid in sorted(VALID_PROPOSALS)
    }

    unresolved_high_cap_blockers = []
    unsupported_agents = []

    for ballot in ballots:
        agent = str(ballot.get("agent", "")).strip().lower()
        weight = float(weights.get(agent, 0.50))

        blockers = ballot.get("blockers", [])
        if isinstance(blockers, list) and agent in HIGH_CAP_AGENTS:
            for blk in blockers:
                sev = str(blk.get("severity", "")).strip().upper()
                resolved = bool(blk.get("resolved", False))
                if sev == "HIGH" and not resolved:
                    unresolved_high_cap_blockers.append((agent, blk.get("id", "unknown")))

        votes = ballot.get("votes", [])
        if not votes:
            unsupported_agents.append(agent)
            continue

        for item in votes:
            pid = str(item.get("proposal_id", "")).strip().upper()
            vote = str(item.get("vote", "")).strip().lower()
            score = float(item.get("score", 0))
            conf = float(item.get("confidence", 0))
            signed = _vote_sign(vote)
            contribution = signed * score * conf * weight
            entry = per_proposal[pid]
            entry["weighted_total"] += contribution
            if vote == "approve":
                entry["approve_count"] += 1
            elif vote == "reject":
                entry["reject_count"] += 1
            else:
                entry["abstain_count"] += 1
            entry["contributors"].append(
                {
                    "agent": agent,
                    "vote": vote,
                    "score": score,
                    "confidence": conf,
                    "weight": weight,
                    "contribution": round(contribution, 4),
                }
            )

    gate_hold = len(unresolved_high_cap_blockers) >= 2
    return per_proposal, {
        "gate_hold": gate_hold,
        "unresolved_high_cap_blockers": unresolved_high_cap_blockers,
        "unsupported_agents": unsupported_agents,
    }


def _render_markdown(
    ballots: List[dict],
    errors: List[str],
    per_proposal: dict,
    meta: dict,
    weights: Dict[str, float],
) -> str:
    lines: List[str] = []
    lines.append("# Round 7 Vote Tally")
    lines.append("")
    lines.append("## Input Summary")
    lines.append(f"- Valid ballots: `{len(ballots)}`")
    lines.append(f"- Parsing/validation errors: `{len(errors)}`")
    lines.append("")
    if errors:
        lines.append("### Invalid Ballots")
        for err in errors:
            lines.append(f"- {err}")
        lines.append("")

    lines.append("## Weight Table")
    for agent, w in sorted(weights.items()):
        lines.append(f"- `{agent}`: `{w}`")
    lines.append("")

    lines.append("## Proposal Scores")
    lines.append("| Proposal | Weighted Total | Approve | Reject | Abstain |")
    lines.append("|---|---:|---:|---:|---:|")
    ranked = sorted(
        per_proposal.items(),
        key=lambda x: x[1]["weighted_total"],
        reverse=True,
    )
    for pid, rec in ranked:
        lines.append(
            f"| `{pid}` | `{rec['weighted_total']:.4f}` | `{rec['approve_count']}` | `{rec['reject_count']}` | `{rec['abstain_count']}` |"
        )
    lines.append("")

    winner = ranked[0][0] if ranked else "N/A"
    lines.append("## Decision Gate")
    lines.append(f"- Tentative winner: `{winner}`")
    lines.append(f"- High-cap unresolved blockers >= 2: `{meta['gate_hold']}`")

    if meta["unresolved_high_cap_blockers"]:
        lines.append("- Unresolved high-cap blockers:")
        for agent, blk_id in meta["unresolved_high_cap_blockers"]:
            lines.append(f"  - `{agent}` -> `{blk_id}`")
    else:
        lines.append("- Unresolved high-cap blockers: none")
    lines.append("")

    final_decision = "HOLD" if meta["gate_hold"] else f"GO_{winner}"
    if final_decision == "HOLD":
        lines.append("- Final status: `HOLD` (gate triggered).")
    else:
        lines.append(f"- Final status: `{final_decision}` (no gate hold).")
    lines.append("")

    lines.append("## Contributor Detail")
    for pid, rec in ranked:
        lines.append(f"### {pid}")
        if not rec["contributors"]:
            lines.append("- No contributors.")
            continue
        for c in rec["contributors"]:
            lines.append(
                "- "
                f"`{c['agent']}` vote=`{c['vote']}` score=`{c['score']}` "
                f"conf=`{c['confidence']}` weight=`{c['weight']}` contrib=`{c['contribution']}`"
            )
    lines.append("")
    return "\n".join(lines)


def _load_weights(raw: str) -> Dict[str, float]:
    if not raw:
        return dict(DEFAULT_WEIGHTS)
    parsed = json.loads(raw)
    merged = dict(DEFAULT_WEIGHTS)
    for k, v in parsed.items():
        merged[str(k).strip().lower()] = float(v)
    return merged


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate Round 7 ballots into weighted vote tally.")
    parser.add_argument(
        "--ballots-dir",
        type=str,
        default="docs/handoffs/ballots/round7",
        help="Directory containing ballot JSON files.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="docs/handoffs/20260209_round7_vote_tally.md",
        help="Output markdown file path.",
    )
    parser.add_argument(
        "--weights-json",
        type=str,
        default="",
        help="Optional JSON object to override agent weights.",
    )
    args = parser.parse_args()

    ballots_dir = Path(args.ballots_dir)
    if not ballots_dir.exists():
        print(f"[ERROR] ballots directory not found: {ballots_dir}")
        return 1

    ballots, errors = _collect_ballots(ballots_dir)
    if len(ballots) < 4:
        print(f"[ERROR] need at least 4 valid ballots, got {len(ballots)}")
        if errors:
            print("[DETAIL] validation errors:")
            for err in errors:
                print(f" - {err}")
        return 2

    try:
        weights = _load_weights(args.weights_json)
    except Exception as exc:
        print(f"[ERROR] invalid --weights-json: {exc}")
        return 3

    per_proposal, meta = _aggregate(ballots, weights)
    markdown = _render_markdown(ballots, errors, per_proposal, meta, weights)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")

    print(f"[OK] wrote tally: {output_path}")
    winner = max(per_proposal.items(), key=lambda x: x[1]["weighted_total"])[0]
    print(f"[SUMMARY] winner={winner} gate_hold={meta['gate_hold']} ballots={len(ballots)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
