# Intelligence Knowledge Graph — staging and deployment status

**Repository:** [PCakes303/intelligence-knowledge-graph](https://github.com/PCakes303/intelligence-knowledge-graph)  
**Maturity:** Experimental reference implementation  
**License:** Pending portfolio review; no license is asserted.

## Deployment and parity

- The public repository contains 29 product files; this deployment-status file is administrative evidence and is excluded from the product-file parity count.
- The retained master staging packet was refreshed from the live remote after the audit found drift in the CI workflow, security policy, graph implementation, query implementation, requirements, schema, validator and tests.
- Current parity verification: **29 staged product files vs 29 remote product files; zero missing, extra or differing Git blob hashes.**
- The parity comparison was performed against the live `main` trees after synchronization on 2026-11-02.
- CI: [Run 41497020106](https://github.com/PCakes303/intelligence-knowledge-graph/actions/runs/41497020106) passed on Python 3.10, 3.11 and 3.12 after input/model hardening. README/security documentation changes are undergoing their own CI runs.

## Scope

Provenance-aware in-memory graph model for source, evidence, entity and evidence-backed relationship records. It preserves observation/interpretation separation and explicit uncertainty. It does not collect sources, preserve evidence bytes, resolve identities, infer facts, establish truth, or make decisions.

## Remaining gates

- Bound path-query work/queue expansion in addition to depth and result count.
- Expand schema/model parity tests, especially direct library API validation versus CLI schema validation.
- Apply and verify GitHub About metadata and repository administration/security settings.
- Keep licensing pending until an explicit repository/artifact decision is approved.
- Preserve synthetic examples and avoid real personal data.
