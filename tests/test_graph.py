import unittest
from intelligence_knowledge_graph import KnowledgeGraph, Node, Edge

T = "2026-01-01T00:00:00Z"

def graph_fixture():
    graph = KnowledgeGraph("g", T)
    graph.add_node(Node.from_dict({"id":"s","type":"source","label":"Source","recorded_at":T,"source_record_id":"src","canonical_url":"https://example.org"}))
    graph.add_node(Node.from_dict({"id":"ev","type":"evidence","label":"Evidence","recorded_at":T,"evidence_record_id":"evr","sha256":"a"*64,"observed_at":T,"source_node_id":"s"}))
    graph.add_node(Node.from_dict({"id":"e","type":"entity","label":"Entity","recorded_at":T,"entity_record_id":"ent","entity_kind":"organization","resolution_status":"provisional"}))
    graph.add_edge(Edge.from_dict({"id":"r","from":"ev","to":"e","predicate":"mentions","evidence_refs":["ev"],"confidence":0.6,"uncertainty":"synthetic only","observed_at":T,"recorded_at":T}))
    return graph

class GraphTests(unittest.TestCase):

    def test_graph_node_and_edge_mappings_are_immutable(self):
        graph = graph_fixture()
        with self.assertRaises(TypeError):
            graph.nodes["other"] = graph.nodes["s"]
        with self.assertRaises(TypeError):
            graph.edges["other"] = graph.edges["r"]

    def test_graph_node_capacity_is_enforced(self):
        graph = KnowledgeGraph("g", T, max_nodes=1)
        graph.add_node(Node.from_dict({"id":"s","type":"source","label":"Source","recorded_at":T,"source_record_id":"src","canonical_url":"https://example.org"}))
        entity = Node.from_dict({"id":"e","type":"entity","label":"Entity","recorded_at":T,"entity_record_id":"ent","entity_kind":"organization","resolution_status":"provisional"})
        with self.assertRaises(ValueError):
            graph.add_node(entity)

    def test_graph_edge_capacity_is_enforced(self):
        graph = graph_fixture()
        graph.max_edges = 1
        second = Edge.from_dict({"id":"r2","from":"ev","to":"e","predicate":"supports","evidence_refs":["ev"],"confidence":0.5,"uncertainty":"synthetic","observed_at":T,"recorded_at":T})
        with self.assertRaises(ValueError):
            graph.add_edge(second)

    def test_graph_configuration_is_bounded(self):
        with self.assertRaises(ValueError):
            KnowledgeGraph("g", T, max_nodes=100001)
        with self.assertRaises(ValueError):
            KnowledgeGraph("g", T, max_edges=500001)

    def test_round_trip(self):
        graph = graph_fixture()
        self.assertEqual(KnowledgeGraph.from_dict(graph.to_dict()).to_dict(), graph.to_dict())
    def test_evidence_requires_source(self):
        graph = KnowledgeGraph("g", T)
        raw = {"id":"ev","type":"evidence","label":"Evidence","recorded_at":T,"evidence_record_id":"evr","sha256":"a"*64,"observed_at":T,"source_node_id":"missing"}
        with self.assertRaises(ValueError):
            graph.add_node(Node.from_dict(raw))
    def test_edge_requires_evidence_node(self):
        graph = graph_fixture()
        bad = Edge.from_dict({"id":"bad","from":"s","to":"e","predicate":"related","evidence_refs":["s"],"confidence":0.5,"uncertainty":"unknown","observed_at":T,"recorded_at":T})
        with self.assertRaises(ValueError):
            graph.add_edge(bad)
    def test_duplicate_node_rejected(self):
        graph = graph_fixture()
        with self.assertRaises(ValueError):
            graph.add_node(graph.nodes["s"])

if __name__ == "__main__":
    unittest.main()
