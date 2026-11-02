import unittest
from intelligence_knowledge_graph.models import Edge

T = "2026-01-01T00:00:00Z"

class ProvenanceTests(unittest.TestCase):
    def test_edge_requires_evidence_reference(self):
        raw = {"id":"r","from":"a","to":"b","predicate":"related","evidence_refs":[],"confidence":0.4,"uncertainty":"unknown","observed_at":T,"recorded_at":T}
        with self.assertRaises(ValueError):
            Edge.from_dict(raw)
    def test_uncertainty_is_required(self):
        raw = {"id":"r","from":"a","to":"b","predicate":"related","evidence_refs":["ev"],"confidence":0.4,"uncertainty":" ","observed_at":T,"recorded_at":T}
        with self.assertRaises(ValueError):
            Edge.from_dict(raw)

if __name__ == "__main__":
    unittest.main()
