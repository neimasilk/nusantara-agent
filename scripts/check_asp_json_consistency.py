import argparse
import json
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Tuple


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class RuleMapping:
    required: List[str] = field(default_factory=list)
    optional: List[str] = field(default_factory=list)
    note: str = ""


BALI_RULE_MAP: Dict[str, RuleMapping] = {
    "BAL-001": RuleMapping(
        required=[
            r"\bpatrilineal\.",
            r"status_purusa\(P\)\s*:-\s*sentana_rajeg\(P\)\.",
        ],
        note="Asas patrilineal/purusa dan sentana rajeg sebagai purusa.",
    ),
    "BAL-002": RuleMapping(
        required=[
            r"status_purusa\(P\)\s*:-\s*male\(P\)\.",
            r"can_inherit\(P,\s*A\)\s*:-\s*[\s\S]*asset_type\(A,\s*druwe_gabro\)\.",
            r"gugur_hak_waris\(P\)\s*:-\s*menolak_ngaben\(P\)\.",
            r"gugur_hak_waris\(P\)\s*:-\s*not\s+kewajiban_ngayah\(P\),\s*status_purusa\(P\)\.",
        ],
        note="Hak waris purusa + kewajiban swadharma/ngayah.",
    ),
    "BAL-003": RuleMapping(
        required=[r"status_purusa\(P\)\s*:-\s*sentana_rajeg\(P\)\."],
        optional=[r"#defined\s+keluarga_camput/1\."],
        note="Sentana rajeg ter-encode; syarat nyentana/camput tidak eksplisit penuh.",
    ),
    "BAL-004": RuleMapping(
        required=[
            r"asset_type\(tanah_sanggah,\s*druwe_tengah\)\.",
            r"asset_type\(tanah_tegal_laba_pura,\s*druwe_tengah\)\.",
            r"asset_type\(tanah_pkd,\s*druwe_tengah\)\.",
            r"conflict\(A,\s*sell\)\s*:-\s*asset_type\(A,\s*druwe_tengah\),\s*action\(A,\s*sell\)\.",
        ],
        note="Klasifikasi druwe tengah + inalienable (larangan jual).",
    ),
    "BAL-005": RuleMapping(
        required=[
            r"asset_type\(harta_druwe_gabro,\s*druwe_gabro\)\.",
            r"asset_type\(gunakaya,\s*druwe_gabro\)\.",
        ]
    ),
    "BAL-006": RuleMapping(
        required=[
            r"asset_type\(harta_tetadan,\s*tetadan\)\.",
            r"ownership_type\(tetadan,\s*individual\)\.",
        ]
    ),
    "BAL-007": RuleMapping(
        required=[
            r"asset_type\(harta_bekel,\s*bekel\)\.",
            r"ownership_type\(bekel,\s*pemberian_putus\)\.",
        ],
        note="Klasifikasi bekel sebagai pemberian putus.",
    ),
    "BAL-008": RuleMapping(
        required=[
            r"asset_type\(jiwa_dana,\s*jiwa_dana\)\.",
            r"conflict\(jiwa_dana,\s*invalid_transfer\)\s*:-\s*action\(jiwa_dana,\s*grant\),\s*not\s*disaksikan_prajuru\.",
        ]
    ),
    "BAL-009": RuleMapping(
        required=[
            r"asset_type\(harta_pusaka,\s*pusaka_magis\)\.",
            r"conflict\(A,\s*sell\)\s*:-\s*asset_type\(A,\s*pusaka_magis\),\s*action\(A,\s*sell\)\.",
            r"can_inherit\(P,\s*A\)\s*:-\s*[\s\S]*asset_type\(A,\s*pusaka_magis\),\s*not\s*kawin_keluar\(P\)\.",
        ]
    ),
    "BAL-010": RuleMapping(
        required=[
            r"status_purusa\(P\)\s*:-\s*male\(P\)\.",
            r"can_inherit\(P,\s*A\)\s*:-\s*[\s\S]*asset_type\(A,\s*druwe_gabro\)\.",
        ],
        optional=[r"prioritas_sanggah\(P,\s*tanah_sanggah\)\s*:-\s*ngamong_sanggah\(P\)\."],
        note="Hak dasar anak laki-laki ada; porsi 'lebih besar' tidak dimodelkan numerik.",
    ),
    "BAL-011": RuleMapping(
        required=[
            r"#defined\s+ngamong_sanggah/1\.",
            r"prioritas_sanggah\(P,\s*tanah_sanggah\)\s*:-\s*ngamong_sanggah\(P\)\.",
            r"can_inherit\(P,\s*tanah_sanggah\)\s*:-\s*prioritas_sanggah\(P,\s*tanah_sanggah\)\.",
        ]
    ),
    "BAL-012": RuleMapping(
        required=[r"gugur_hak_waris\(P\)\s*:-\s*ninggal_kedaton\(P\)\."],
        note="Konsekuensi ninggal kedaton ada; sebab pindah agama tidak diekspresikan langsung.",
    ),
    "BAL-013": RuleMapping(
        required=[
            r"ahli_waris_terbatas\(P\)\s*:-\s*female\(P\),\s*kawin_keluar\(P\)\.",
            r"can_inherit\(P,\s*A\)\s*:-\s*[\s\S]*ahli_waris_terbatas\(P\),\s*asset_type\(A,\s*druwe_gabro\)\.",
        ]
    ),
    "BAL-014": RuleMapping(
        required=[r"(?:setengah|1/2|share_ratio|bagian_*)"],
        optional=[r"can_inherit\(P,\s*A\)\s*:-\s*[\s\S]*ahli_waris_terbatas\(P\),\s*asset_type\(A,\s*druwe_gabro\)\."],
        note="Hak dasar anak perempuan terencode, namun rasio maksimal 1/2 tidak eksplisit.",
    ),
    "BAL-015": RuleMapping(
        required=[
            r":-\s*female\(P\),\s*kawin_keluar\(P\),\s*can_inherit\(P,\s*A\),\s*asset_type\(A,\s*druwe_tengah\)\.",
            r":-\s*female\(P\),\s*kawin_keluar\(P\),\s*can_inherit\(P,\s*A\),\s*asset_type\(A,\s*pusaka_magis\)\.",
        ]
    ),
    "BAL-016": RuleMapping(
        required=[
            r"conflict\(A,\s*sell\)\s*:-\s*asset_type\(A,\s*druwe_tengah\),\s*action\(A,\s*sell\)\.",
            r"conflict\(A,\s*sell\)\s*:-\s*asset_type\(A,\s*pusaka_magis\),\s*action\(A,\s*sell\)\.",
        ]
    ),
    "BAL-017": RuleMapping(
        required=[r"hak_pakai|hak_kelola"],
        optional=[
            r"ownership_type\(pusaka_magis,\s*komunal_ritual\)\.",
            r"conflict\(A,\s*transfer_outside_desa\)\s*:-\s*asset_type\(A,\s*druwe_tengah\),\s*action\(A,\s*transfer_outside_desa\)\.",
        ],
        note="Larangan transfer luar desa ada, namun konsep hak pakai/hak kelola tidak eksplisit.",
    ),
    "BAL-018": RuleMapping(
        required=[
            r"asset_type\(tanah_pelaba_pura,\s*druwe_tengah\)\.",
            r"conflict\(A,\s*split_individual\)\s*:-\s*asset_type\(A,\s*tanah_pelaba_pura\),\s*action\(A,\s*split_individual\)\.",
        ]
    ),
    "BAL-019": RuleMapping(
        required=[r"adopsi\([\w_]+\).*disaksikan_prajuru|disaksikan_prajuru.*adopsi"],
        optional=[
            r"adopsi_sah\(P\)\s*:-\s*adopsi\(P\),\s*upacara_widhi_widana\(P\),\s*tri_upasaksi\(P\)\.",
            r"conflict\(jiwa_dana,\s*invalid_transfer\)\s*:-\s*action\(jiwa_dana,\s*grant\),\s*not\s*disaksikan_prajuru\.",
        ],
        note="Syarat saksi prajuru spesifik untuk adopsi belum eksplisit; ada mekanisme saksi pada jiwa dana.",
    ),
    "BAL-020": RuleMapping(
        required=[r"ditarik_desa\(tanah_ayahan_desa\)\s*:-\s*keluarga_camput\(_\)\."]
    ),
    "BAL-021": RuleMapping(
        required=[
            r"gugur_hak_waris\(P\)\s*:-\s*menolak_ngaben\(P\)\.",
            r"gugur_hak_waris\(P\)\s*:-\s*not\s+kewajiban_ngayah\(P\),\s*status_purusa\(P\)\.",
        ]
    ),
    "BAL-022": RuleMapping(
        required=[r"biaya_ngaben|prioritas_pitra_yadnya|sebelum_sisa_dibagi"],
        note="Prioritas biaya upacara sebelum distribusi belum ditemukan.",
    ),
    "BAL-023": RuleMapping(
        required=[
            r"adopsi_sah\(P\)\s*:-\s*adopsi\(P\),\s*upacara_widhi_widana\(P\),\s*tri_upasaksi\(P\)\."
        ]
    ),
    "BAL-024": RuleMapping(
        required=[r"adopsi_sah\(P\).*kewajiban_ngayah|kewajiban_sanggah.*adopsi_sah"],
        optional=[
            r"can_inherit\(P,\s*A\)\s*:-\s*[\s\S]*adopsi_sah\(P\),\s*asset_type\(A,\s*druwe_gabro\)\.",
            r"can_inherit\(P,\s*A\)\s*:-\s*[\s\S]*adopsi_sah\(P\),\s*asset_type\(A,\s*druwe_tengah\)\.",
        ],
        note="Hak waris anak angkat ada; kesetaraan kewajiban (sanggah/ngayah) belum eksplisit.",
    ),
    "BAL-025": RuleMapping(
        required=[r"mulih_daha|cerai|janda_kehilangan_hak"],
        note="Aturan dampak cerai khusus 'mulih daha' belum ditemukan.",
    ),
    "BAL-026": RuleMapping(
        required=[r"hak_asuh|anak_mengikut_ayah|garis_purusa_setelah_cerai"],
        note="Aturan pasca cerai untuk anak belum ditemukan.",
    ),
    "BAL-027": RuleMapping(
        required=[r"sangkep|musyawarah_keluarga|dadia|suka_duka"],
        note="Prosedur sengketa internal keluarga belum ditemukan.",
    ),
    "BAL-028": RuleMapping(
        required=[r"banjar|kerta_desa|pengadilan_negeri|eskalasi_sengketa"],
        note="Prosedur eskalasi sengketa belum ditemukan.",
    ),
    "BAL-029": RuleMapping(
        required=[r"wangsa|beda_wangsa|nyeburin|kewajiban_adat_terpenuhi"],
        note="Perubahan kontemporer beda wangsa belum ditemukan.",
    ),
    "BAL-030": RuleMapping(
        required=[
            r"hak_penguasaan\(P,\s*A\)\s*:-\s*janda\(P\),\s*[\s\S]*not\s*menikah_lagi\(P\)\."
        ]
    ),
    "BAL-031": RuleMapping(
        required=[r"pada_gelahang|dua_purusa|hak_waris_dibagi_dua"],
        note="Aturan perkawinan pada gelahang belum ditemukan.",
    ),
    "BAL-032": RuleMapping(
        required=[
            r":-\s*astra\(P\),\s*male\(Ayah\),\s*parent\(Ayah,\s*P\),\s*not\s*bisa_relasi_ayah\(P\),\s*can_inherit\(P,\s*_\)\.",
            r"bisa_relasi_ayah\(P\)\s*:-\s*pengesahan_ayah\(P\)\.",
        ]
    ),
    "BAL-033": RuleMapping(
        required=[r"alpaka_guru|durhaka|mencoba_membunuh|keputusan_sangkep"],
        note="Ground disinherit karena alpaka guru belum ditemukan.",
    ),
    "BAL-034": RuleMapping(
        required=[r"sepertiga|1/3|potongan_sanggah|prioritas_harta_pusaka"],
        note="Mekanisme sisih 1/3 sebelum pembagian belum ditemukan.",
    ),
}


def _build_domain_config(domain: str) -> Tuple[Path, Path, Dict[str, RuleMapping]]:
    if domain != "bali":
        raise ValueError(f"Domain belum didukung: {domain}")
    return (
        ROOT / "data" / "rules" / "bali_rules.json",
        ROOT / "src" / "symbolic" / "rules" / "bali.lp",
        BALI_RULE_MAP,
    )


def _find_line(lp_text: str, pattern: str) -> Optional[int]:
    match = re.search(pattern, lp_text)
    if not match:
        return None
    return lp_text.count("\n", 0, match.start()) + 1


def _evaluate_rule(
    mapping: RuleMapping,
    lp_text: str,
) -> Dict[str, object]:
    matched_required: List[Dict[str, object]] = []
    missing_required: List[str] = []
    matched_optional: List[Dict[str, object]] = []

    for pattern in mapping.required:
        if re.search(pattern, lp_text):
            line_no = _find_line(lp_text, pattern)
            matched_required.append({"pattern": pattern, "line": line_no})
        else:
            missing_required.append(pattern)

    for pattern in mapping.optional:
        if re.search(pattern, lp_text):
            line_no = _find_line(lp_text, pattern)
            matched_optional.append({"pattern": pattern, "line": line_no})

    if mapping.required and not missing_required:
        status = "COVERED"
    elif matched_required or matched_optional:
        status = "PARTIAL"
    else:
        status = "GAP"

    return {
        "status": status,
        "matched_required": matched_required,
        "missing_required": missing_required,
        "matched_optional": matched_optional,
        "note": mapping.note,
    }


def run_consistency_check(
    domain: str,
    json_rules_path: Optional[Path] = None,
    asp_rules_path: Optional[Path] = None,
) -> Dict[str, object]:
    default_json, default_lp, mapping = _build_domain_config(domain)
    json_path = json_rules_path or default_json
    lp_path = asp_rules_path or default_lp

    if not json_path.exists():
        raise FileNotFoundError(f"JSON rules tidak ditemukan: {json_path}")
    if not lp_path.exists():
        raise FileNotFoundError(f"ASP rules tidak ditemukan: {lp_path}")

    rules = json.loads(json_path.read_text(encoding="utf-8"))
    if not isinstance(rules, list):
        raise ValueError("Format JSON rules harus list.")

    lp_text = lp_path.read_text(encoding="utf-8")

    per_rule: List[Dict[str, object]] = []
    by_status = {"COVERED": 0, "PARTIAL": 0, "GAP": 0}
    by_type: Dict[str, Dict[str, int]] = {}

    for item in rules:
        rule_id = str(item.get("id", "")).strip()
        rule_type = str(item.get("type", "")).strip() or "unknown"
        rule_text = str(item.get("rule", "")).strip()
        verifier = str(item.get("verification_status", "")).strip() or "UNKNOWN"

        domain_mapping = mapping.get(rule_id)
        if domain_mapping is None:
            result = {
                "status": "GAP",
                "matched_required": [],
                "missing_required": [],
                "matched_optional": [],
                "note": "Rule ID belum punya mapping audit.",
            }
        else:
            result = _evaluate_rule(domain_mapping, lp_text)

        status = str(result["status"])
        by_status[status] = by_status.get(status, 0) + 1
        by_type.setdefault(rule_type, {"COVERED": 0, "PARTIAL": 0, "GAP": 0})
        by_type[rule_type][status] += 1

        per_rule.append(
            {
                "id": rule_id,
                "type": rule_type,
                "verification_status": verifier,
                "rule": rule_text,
                "status": status,
                "note": result["note"],
                "matched_required": result["matched_required"],
                "missing_required": result["missing_required"],
                "matched_optional": result["matched_optional"],
            }
        )

    report = {
        "as_of": date.today().isoformat(),
        "domain": domain,
        "inputs": {
            "json_rules_path": str(json_path.relative_to(ROOT)),
            "asp_rules_path": str(lp_path.relative_to(ROOT)),
        },
        "summary": {
            "total_rules": len(per_rule),
            "covered": by_status.get("COVERED", 0),
            "partial": by_status.get("PARTIAL", 0),
            "gap": by_status.get("GAP", 0),
        },
        "by_type": by_type,
        "rules": per_rule,
    }
    return report


def _to_markdown(report: Dict[str, object]) -> str:
    summary = report["summary"]
    lines = [
        "# ASP vs JSON Consistency Report",
        "",
        f"- Date: {report['as_of']}",
        f"- Domain: {report['domain']}",
        f"- JSON: `{report['inputs']['json_rules_path']}`",
        f"- ASP: `{report['inputs']['asp_rules_path']}`",
        "",
        "## Summary",
        "",
        f"- Total rules: {summary['total_rules']}",
        f"- COVERED: {summary['covered']}",
        f"- PARTIAL: {summary['partial']}",
        f"- GAP: {summary['gap']}",
        "",
        "## GAP Rules",
        "",
    ]

    gap_rules = [r for r in report["rules"] if r["status"] == "GAP"]
    if not gap_rules:
        lines.append("- (none)")
    else:
        for item in gap_rules:
            note = item.get("note") or "-"
            lines.append(f"- {item['id']} ({item['type']}): {note}")

    lines.extend(["", "## PARTIAL Rules", ""])
    partial_rules = [r for r in report["rules"] if r["status"] == "PARTIAL"]
    if not partial_rules:
        lines.append("- (none)")
    else:
        for item in partial_rules:
            note = item.get("note") or "-"
            lines.append(f"- {item['id']} ({item['type']}): {note}")

    return "\n".join(lines) + "\n"


def _print_summary(report: Dict[str, object]) -> None:
    summary = report["summary"]
    print("[ASP-JSON CONSISTENCY]")
    print(f"- domain: {report['domain']}")
    print(f"- total_rules: {summary['total_rules']}")
    print(f"- covered: {summary['covered']}")
    print(f"- partial: {summary['partial']}")
    print(f"- gap: {summary['gap']}")

    gap_ids = [item["id"] for item in report["rules"] if item["status"] == "GAP"]
    partial_ids = [item["id"] for item in report["rules"] if item["status"] == "PARTIAL"]
    print(f"- gap_ids: {gap_ids}")
    print(f"- partial_ids: {partial_ids}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit konsistensi aturan expert-verified JSON vs ASP rules."
    )
    parser.add_argument(
        "--domain",
        type=str,
        default="bali",
        choices=["bali"],
        help="Domain rules yang diaudit.",
    )
    parser.add_argument(
        "--json-rules",
        type=str,
        default="",
        help="Override path JSON rules.",
    )
    parser.add_argument(
        "--asp-rules",
        type=str,
        default="",
        help="Override path ASP rules (.lp).",
    )
    parser.add_argument(
        "--out-json",
        type=str,
        default="",
        help="Path output laporan JSON.",
    )
    parser.add_argument(
        "--out-md",
        type=str,
        default="",
        help="Path output laporan Markdown.",
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    json_override = Path(args.json_rules) if args.json_rules else None
    asp_override = Path(args.asp_rules) if args.asp_rules else None

    report = run_consistency_check(
        domain=args.domain,
        json_rules_path=json_override,
        asp_rules_path=asp_override,
    )
    _print_summary(report)

    if args.out_json:
        out_json = Path(args.out_json)
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[OK] JSON report saved: {out_json}")

    if args.out_md:
        out_md = Path(args.out_md)
        out_md.parent.mkdir(parents=True, exist_ok=True)
        out_md.write_text(_to_markdown(report), encoding="utf-8")
        print(f"[OK] Markdown report saved: {out_md}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
