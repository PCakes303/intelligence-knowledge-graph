# Staging Status

The initial reference implementation is staged in the master repository. The standalone GitHub remote has not yet been created; no remote deployment or CI success is claimed.

- [x] Provenance-aware graph contract and threat model.
- [x] Standard-library node, edge, graph, and bounded query implementation.
- [x] Deterministic graph serialization and referential-integrity checks.
- [x] Synthetic fixture and unit tests for models, graph integrity, provenance, and queries.
- [x] JSON graph schema, validation CLI, and Python 3.10–3.12 CI workflow.
- [x] Metadata and AI discovery entrypoints.
- [ ] Create public remote `PCakes303/intelligence-knowledge-graph`.
- [ ] Publish staged files to `main` and compare every file.
- [ ] Observe green CI matrix on Python 3.10, 3.11, and 3.12.
- [ ] Reconcile remote verification in the master portfolio.

Upstream dependencies: `osint-evidence` and `entity-resolution`. Their contracts must be checked before adding adapters. Current graph edges require evidence references and explicit uncertainty; the prototype does not collect, scrape, resolve identities, infer facts, or verify truth.
