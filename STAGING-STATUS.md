# Publication and Verification Status

The initial reference implementation is published in the standalone public repository. The remote tree was checked against the master staging packet: all 29 expected files were present and their Git blob hashes matched before the dependency-order fix. The fix is mirrored in the master staging copy.

- [x] Provenance-aware graph contract and threat model.
- [x] Standard-library node, edge, graph, and bounded query implementation.
- [x] Deterministic graph serialization and referential-integrity checks.
- [x] Synthetic fixture and unit tests for models, graph integrity, provenance, and queries.
- [x] Strict versioned JSON graph schema, validation CLI, and Python 3.10–3.12 CI workflow.
- [x] Metadata and AI discovery entrypoints.
- [x] Capability and compatibility metadata normalized to contract v1.1.0; master starter-build validation passed against the live remote metadata.
- [x] Public remote created: `PCakes303/intelligence-knowledge-graph`.
- [x] Initial 29-file publication and file-hash comparison.
- [x] Dependency-order loading correction committed and mirrored to master staging.
- [x] CI matrix green on Python 3.10, 3.11, and 3.12 (run recorded separately).
- [x] Final portfolio registry/checkpoint reconciliation recorded in [the master portfolio audit checkpoint](https://github.com/PCakes303/agent-intelligence-ecosystem/blob/main/checkpoints/2026-11-02-portfolio-integrity-audit.md).

Upstream dependencies: `osint-evidence` and `entity-resolution`. Their contracts must be checked before adding adapters. Current graph edges require evidence references and explicit uncertainty; the prototype does not collect, scrape, resolve identities, infer facts, or verify truth. License selection remains pending portfolio review.
