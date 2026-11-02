# Agent Instructions

- Preserve observation/interpretation separation.
- Every relationship must reference at least one evidence record.
- Never treat a graph edge, confidence value, or schema-valid record as proof of truth.
- Keep deterministic serialization and bounded graph traversal.
- Do not add network collection, scraping, external API clients, identity resolution, or automated inference to this repository.
- Use synthetic fixtures only; avoid real personal data.
- Run `python -m unittest discover -s tests -v` and `python tools/validate_graph.py examples/graph.json`.
