# Intelligence Knowledge Graph

**Repository:** `PCakes303/intelligence-knowledge-graph`  
**Portfolio position:** 23 / 29 public repositories  
**Technical sequence:** Repository 20  
**Maturity:** reference implementation / experimental  
**License:** pending portfolio license review

## Purpose

A provenance-aware graph model connecting source records, preserved evidence, entities, and evidence-backed relationships. It preserves the distinction between observations and interpretations and makes uncertainty explicit.

## Initial implementation

- Strict, versioned JSON graph document schema.
- Typed Python models for source, evidence, and entity nodes plus directed relationships.
- In-memory graph with referential-integrity checks, deterministic serialization, adjacency lookup, and bounded path queries.
- Evidence/provenance references on interpreted relationships.
- Synthetic fixtures and unit tests; Python 3.10–3.12 CI.

## Quick start

Requires Python 3.10+; runtime has no third-party dependencies.

```bash
python -m unittest discover -s tests -v
python tools/validate_graph.py examples/graph.json
```

## Contract boundaries

This is a graph data model and reference library, not an intelligence collection or inference system. It does not crawl, scrape, identify real people, resolve identities, assert truth, score people, or make decisions. Entity resolution and evidence acquisition remain upstream responsibilities. A graph edge records a sourced assertion with uncertainty, not ground truth.

See [Graph Contract](docs/GRAPH-CONTRACT.md), [Provenance and Uncertainty](docs/PROVENANCE-AND-UNCERTAINTY.md), and [Threat Model](docs/THREAT-MODEL.md).
