# Reviewer Profiles — Specialists

## Purpose

Define risk-triggered specialist reviewers for `math-modeling-v4`.

## Global Boundary

Specialists may return findings, risks, recommended actions, evidence references, and recommendations for decisions, gates, branches, rollbacks, or claim updates.

## Data-Audit Reviewer

Trigger when raw or processed data has unclear fields, missing values, outliers, version drift, schema ambiguity, inconsistent units, or relationship-data gaps.

## Code-Review Reviewer

Trigger when solver code, reproducibility checks, dependency issues, or implementation errors could affect results or claims.

## Figure-Review Reviewer

Trigger when figures, captions, source CSV files, metadata, readability, or visual claims need review.

## Evidence-Gate Reviewer

Trigger before Stage 10 export or whenever a paper-facing claim may exceed available evidence.

## Literature/Method Reviewer

Trigger when a method background or external reference is required and cannot be answered from local materials.
