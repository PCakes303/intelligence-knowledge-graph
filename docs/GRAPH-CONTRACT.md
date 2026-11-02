# Graph Contract v0.1.0

A graph document contains a stable graph ID, contract version, creation timestamp, nodes, and directed edges. Node types are source (catalog reference, not source content), evidence (preserved artifact reference and digest), and entity (upstream resolved or provisional entity). Edges are typed relationships between existing nodes.

Every edge MUST reference one or more evidence nodes and include a confidence value in [0,1], an uncertainty note, and observed/recorded timestamps. Confidence is an upstream assessment, not a probability unless its producer defines it as such.

Evidence records describe observations and preserved artifacts. Edges describe interpretations or assertions derived from evidence. Implementations MUST NOT silently convert interpretations into observations or represent an edge as verified truth.

All timestamps MUST be timezone-aware ISO-8601. Node IDs and edge IDs are unique within a graph. Every edge endpoint and evidence reference MUST resolve to a node in the same graph. Queries are read-only and path traversal is bounded by a caller-supplied maximum depth.

Breaking semantic changes require a major contract version and migration guidance. A schema-valid graph is not necessarily accurate, lawful, authorized, or safe.
