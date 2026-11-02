# ADR 0001: Evidence-Backed Graph Edges

- **Status:** Accepted for experimental v0.1.0.
- **Decision:** Every relationship edge must reference at least one evidence node and include confidence plus an uncertainty note.
- **Context:** Graphs can launder weak interpretations into apparently authoritative facts if provenance and uncertainty are optional.
- **Consequences:** Consumers can trace relationships to evidence records. Graphs without evidence-backed edges are rejected. This does not establish that evidence is authentic or conclusions are correct.
