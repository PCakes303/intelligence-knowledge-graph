# Threat Model

## Assets
Graph integrity, evidence references, provenance metadata, privacy, and consumer interpretation.

## Threats
- Forged graph records or substituted evidence references.
- Confidence laundering or interpretation presented as fact.
- Maliciously large graphs or traversal requests.
- Personal or sensitive data exposure through labels and metadata.
- Stale or contradictory evidence presented without qualification.

## Prototype controls
- Strict field allowlists and bounded values.
- Unique identifiers and endpoint/evidence referential checks.
- Mandatory evidence references, confidence bounds, and uncertainty notes.
- Deterministic serialization and bounded path traversal.
- Synthetic fixtures only; no network access or collection.

## Limitations
No authentication, authorization, encryption, signatures, trusted timestamps, persistent-store transaction isolation, privacy classification engine, or truth verification. Deployers must supply these controls. A SHA-256 reference digest alone does not prove provenance.
