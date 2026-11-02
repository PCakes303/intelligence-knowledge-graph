# Provenance and Uncertainty

Every evidence node identifies an upstream evidence record and content digest. The graph stores references; it does not fetch evidence bytes or claim a digest proves origin or truth.

Every relationship edge includes one or more evidence node references, a relationship predicate, confidence in [0,1], a non-empty uncertainty note, observed and recorded timestamps, and an optional method reference.

Confidence is an upstream assessment, not an independently calibrated probability. Missing, contradictory, stale, or unknown provenance must remain visible. Do not collapse multiple assertions into a single unqualified fact.

The graph library verifies structure and referential integrity only. It does not evaluate source credibility, infer causality, adjudicate contradictions, or certify legal permission.
