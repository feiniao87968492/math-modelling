from pathlib import Path

from command_export_flow import run_export_command_flow
from run_paper_grounding_scan import run_paper_grounding_scan

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "regression" / "paper-grounding"


def test_paper_grounding_fixtures_directory_is_registered():
    expected = {
        "happy-path-all-grounded.md",
        "number-without-claim-entry.md",
        "figure-without-meta-json.md",
        "formula-without-derivation-link.md",
    }
    actual = {p.name for p in FIXTURES.glob("*.md")}
    missing = expected - actual
    assert not missing, f"missing fixture files: {sorted(missing)}"


def test_grounding_protocol_doc_is_registered():
    proto = ROOT / "references" / "protocol-paper-grounding-scan.md"
    assert proto.exists()
    content = proto.read_text(encoding="utf-8")
    assert "Anchor Conventions" in content
    assert "<!-- claim:" in content
    assert "<!-- derivation:" in content
    assert "<!-- claim-table:" in content
    assert "Forbidden Behavior" in content


def test_evidence_gate_lists_grounding_scan_as_check():
    gate = (ROOT / "references" / "evidence-gate.md").read_text(encoding="utf-8")
    assert "paper grounding scan" in gate
    assert "protocol-paper-grounding-scan.md" in gate


def test_grounding_scan_passes_when_all_anchors_resolve():
    result = run_paper_grounding_scan(
        {
            "registry_claim_ids": ["c-q1-wape", "c-q2-obj", "c-q3-obj"],
            "derivation_targets_present": [
                "stage-4/model-q1.md:loss-function",
                "stage-7/sensitivity-q1.md:c-grid-search",
            ],
            "figure_meta_present": [
                "figures/q1-residuals.png",
                "figures/q1-cv.png",
                "figures/q2-packaging.png",
                "figures/q3-equipment.png",
            ],
            "paper_anchors": [
                {"kind": "claim", "target": "c-q1-wape"},
                {"kind": "claim-table", "target": "c-q2-obj"},
                {"kind": "claim", "target": "c-q3-obj"},
                {"kind": "derivation", "target": "stage-4/model-q1.md:loss-function"},
                {"kind": "derivation", "target": "stage-7/sensitivity-q1.md:c-grid-search"},
            ],
            "paper_figures": [
                "figures/q1-residuals.png",
                "figures/q1-cv.png",
                "figures/q2-packaging.png",
                "figures/q3-equipment.png",
            ],
        }
    )
    assert result["status"] == "PASS"
    assert result["unresolved_claims"] == []
    assert result["unresolved_derivations"] == []
    assert result["figures_without_meta"] == []
    assert result["blocked_anchors"] == []


def test_grounding_scan_blocks_on_unresolved_claim():
    result = run_paper_grounding_scan(
        {
            "registry_claim_ids": ["c-q2-obj", "c-q3-obj"],
            "derivation_targets_present": [],
            "figure_meta_present": [],
            "paper_anchors": [
                {"kind": "claim", "target": "c-q1-wape"},
            ],
            "paper_figures": [],
        }
    )
    assert result["status"] == "BLOCKED"
    assert "c-q1-wape" in result["unresolved_claims"]


def test_grounding_scan_blocks_on_figure_without_meta():
    result = run_paper_grounding_scan(
        {
            "registry_claim_ids": ["c-q1-wape"],
            "derivation_targets_present": [],
            "figure_meta_present": ["figures/q1-cv.png"],
            "paper_anchors": [
                {"kind": "claim", "target": "c-q1-wape"},
            ],
            "paper_figures": ["figures/q1-residuals.png"],
        }
    )
    assert result["status"] == "BLOCKED"
    assert "figures/q1-residuals.png" in result["figures_without_meta"]


def test_grounding_scan_blocks_on_unresolved_derivation():
    result = run_paper_grounding_scan(
        {
            "registry_claim_ids": [],
            "derivation_targets_present": ["stage-4/model-q1.md:loss-function"],
            "figure_meta_present": [],
            "paper_anchors": [
                {"kind": "derivation", "target": "stage-4/model-q1.md:loss-function"},
                {"kind": "derivation", "target": "stage-7/sensitivity-q1.md:c-grid-search"},
            ],
            "paper_figures": [],
        }
    )
    assert result["status"] == "BLOCKED"
    assert "stage-7/sensitivity-q1.md:c-grid-search" in result["unresolved_derivations"]
    assert "stage-4/model-q1.md:loss-function" not in result["unresolved_derivations"]


def test_grounding_scan_flags_malformed_anchors():
    result = run_paper_grounding_scan(
        {
            "registry_claim_ids": [],
            "derivation_targets_present": [],
            "figure_meta_present": [],
            "paper_anchors": [
                {"kind": "unknown-kind", "target": "c-q1-wape"},
            ],
            "paper_figures": [],
            "malformed_anchors": ["<!-- claaim: c-q1-wape -->"],
        }
    )
    assert result["status"] == "BLOCKED"
    assert any("unknown anchor kind" in a for a in result["blocked_anchors"])
    assert "<!-- claaim: c-q1-wape -->" in result["blocked_anchors"]


def test_export_command_flow_blocks_when_grounding_scenario_absent(tmp_path):
    project_dir = tmp_path / "project"
    result = run_export_command_flow(
        "/math-modeling export",
        project_dir,
        ROOT,
        {
            "pending_decisions": [],
            "final_gate_status": "PASS",
            "claims_supported": True,
            # paper_grounding_scenario intentionally absent
        },
    )
    assert result["ok"] is True
    assert result["export_allowed"] is False
    assert "paper_grounding_scan_blocked" in result["blockers"]
    assert result["paper_grounding_scan"]["status"] == "BLOCKED"


def test_export_command_flow_blocks_on_unresolved_claim(tmp_path):
    project_dir = tmp_path / "project"
    result = run_export_command_flow(
        "/math-modeling export",
        project_dir,
        ROOT,
        {
            "pending_decisions": [],
            "final_gate_status": "PASS",
            "claims_supported": True,
            "paper_grounding_scenario": {
                "registry_claim_ids": [],
                "derivation_targets_present": [],
                "figure_meta_present": [],
                "paper_anchors": [
                    {"kind": "claim", "target": "c-q1-wape"},
                ],
                "paper_figures": [],
            },
        },
    )
    assert result["ok"] is True
    assert result["export_allowed"] is False
    assert "paper_grounding_scan_blocked" in result["blockers"]
    assert "c-q1-wape" in result["paper_grounding_scan"]["unresolved_claims"]


def test_export_command_flow_passes_with_grounded_bundle(tmp_path):
    project_dir = tmp_path / "project"
    result = run_export_command_flow(
        "/math-modeling export",
        project_dir,
        ROOT,
        {
            "pending_decisions": [],
            "final_gate_status": "PASS",
            "claims_supported": True,
            "paper_grounding_scenario": {
                "registry_claim_ids": ["c-q1-wape"],
                "derivation_targets_present": [
                    "stage-4/model-q1.md:loss-function",
                ],
                "figure_meta_present": ["figures/q1-cv.png"],
                "paper_anchors": [
                    {"kind": "claim", "target": "c-q1-wape"},
                    {"kind": "derivation", "target": "stage-4/model-q1.md:loss-function"},
                ],
                "paper_figures": ["figures/q1-cv.png"],
            },
        },
    )
    assert result["ok"] is True
    assert result["export_allowed"] is True
    assert result["paper_grounding_scan"]["status"] == "PASS"
