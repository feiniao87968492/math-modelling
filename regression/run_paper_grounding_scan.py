"""Paper grounding scan for v4.2 工作项 5.

Deterministic text-based scan. No LLM, no semantic inference. The scanner
takes a scenario dict describing the export bundle's anchors / figures and
returns whether every anchored item resolves to an audit document.

The actual scanner at runtime would walk paper/ markdown, extract anchors
via regex, and probe filesystem. This module models that behavior in a
test-friendly way: scenarios pre-declare what the runtime would have found,
and the simulator returns the verdict.
"""
from __future__ import annotations


def run_paper_grounding_scan(scenario: dict) -> dict:
    registry_claim_ids = set(scenario.get("registry_claim_ids", []))
    derivation_targets = set(scenario.get("derivation_targets_present", []))
    figure_meta_present = set(scenario.get("figure_meta_present", []))

    paper_anchors = scenario.get("paper_anchors", [])
    paper_figures = scenario.get("paper_figures", [])
    malformed_anchors = list(scenario.get("malformed_anchors", []))

    unresolved_claims = []
    unresolved_derivations = []
    figures_without_meta = []

    for anchor in paper_anchors:
        kind = anchor.get("kind")
        target = anchor.get("target")
        if kind in {"claim", "claim-table"}:
            if target not in registry_claim_ids:
                unresolved_claims.append(target)
        elif kind == "derivation":
            if target not in derivation_targets:
                unresolved_derivations.append(target)
        else:
            malformed_anchors.append(f"unknown anchor kind: {kind}")

    for figure_path in paper_figures:
        if figure_path not in figure_meta_present:
            figures_without_meta.append(figure_path)

    blocked = bool(
        unresolved_claims
        or unresolved_derivations
        or figures_without_meta
        or malformed_anchors
    )

    return {
        "status": "BLOCKED" if blocked else "PASS",
        "unresolved_claims": unresolved_claims,
        "unresolved_derivations": unresolved_derivations,
        "figures_without_meta": figures_without_meta,
        "blocked_anchors": malformed_anchors,
    }
