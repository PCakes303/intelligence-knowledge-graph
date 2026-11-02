import unittest
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from intelligence_knowledge_graph import KnowledgeGraph
from intelligence_knowledge_graph.models import Node, Edge, valid_time

T = "2026-01-01T00:00:00Z"

class ModelTests(unittest.TestCase):

    def test_node_metadata_is_snapshotted_and_immutable(self):
        raw = {"id":"s","type":"source","label":"Source","recorded_at":T,
               "source_record_id":"src","canonical_url":"https://example.org",
               "metadata":{"classification":"public"}}
        node = Node.from_dict(raw)
        raw["metadata"]["classification"] = "secret"
        self.assertEqual(node.data["metadata"]["classification"], "public")
        with self.assertRaises(TypeError):
            node.data["metadata"]["classification"] = "changed"

    def test_nested_metadata_is_rejected(self):
        raw = {"id":"s","type":"source","label":"Source","recorded_at":T,
               "source_record_id":"src","canonical_url":"https://example.org",
               "metadata":{"nested":{"value":"not bounded"}}}
        with self.assertRaises(ValueError):
            Node.from_dict(raw)

    def test_malformed_node_type_is_rejected_cleanly(self):
        raw = {"id":"s","type":[],"label":"Source","recorded_at":T}
        with self.assertRaises(ValueError):
            Node.from_dict(raw)

    def test_source_url_credentials_and_invalid_port_are_rejected(self):
        base = {"id":"s","type":"source","label":"Source","recorded_at":T,"source_record_id":"src"}
        for url in ("https://user:pass@example.org", "https://example.org:invalid/"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                Node.from_dict({**base, "canonical_url":url})

    def test_invalid_entity_status_type_is_rejected_cleanly(self):
        raw = {"id":"e","type":"entity","label":"Entity","recorded_at":T,
               "entity_record_id":"ent","entity_kind":"organization","resolution_status":[]}
        with self.assertRaises(ValueError):
            Node.from_dict(raw)

    def test_unhashable_evidence_reference_is_rejected_cleanly(self):
        raw = {"id":"r","from":"a","to":"b","predicate":"mentions","evidence_refs":[{}],
               "confidence":0.5,"uncertainty":"unknown","observed_at":T,"recorded_at":T}
        with self.assertRaises(ValueError):
            Edge.from_dict(raw)

    def test_edge_reference_count_is_bounded(self):
        raw = {"id":"r","from":"a","to":"b","predicate":"mentions",
               "evidence_refs":[f"ev{i}" for i in range(101)],
               "confidence":0.5,"uncertainty":"unknown","observed_at":T,"recorded_at":T}
        with self.assertRaises(ValueError):
            Edge.from_dict(raw)

    def test_source_requires_https(self):
        raw = {"id":"s","type":"source","label":"Source","recorded_at":T,"source_record_id":"src","canonical_url":"http://example.org"}
        with self.assertRaises(ValueError):
            Node.from_dict(raw)
    def test_evidence_digest_format(self):
        raw = {"id":"ev","type":"evidence","label":"Evidence","recorded_at":T,"evidence_record_id":"evr","sha256":"bad","observed_at":T,"source_node_id":"s"}
        with self.assertRaises(ValueError):
            Node.from_dict(raw)
    def test_entity_status_enum(self):
        raw = {"id":"e","type":"entity","label":"Entity","recorded_at":T,"entity_record_id":"ent","entity_kind":"organization","resolution_status":"guessed"}
        with self.assertRaises(ValueError):
            Node.from_dict(raw)
    def test_confidence_bounds(self):
        raw = {"id":"r","from":"a","to":"b","predicate":"mentions","evidence_refs":["ev"],"confidence":1.2,"uncertainty":"uncertain","observed_at":T,"recorded_at":T}
        with self.assertRaises(ValueError):
            Edge.from_dict(raw)
    def test_timezone_required(self):
        self.assertFalse(valid_time("2026-01-01T00:00:00"))

    def test_graph_example_and_direct_models_match_normative_schema(self):
        root = Path(__file__).resolve().parents[1]
        schema = json.loads((root / "schemas" / "graph.schema.json").read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        example = json.loads((root / "examples" / "graph.json").read_text(encoding="utf-8"))
        self.assertEqual(list(validator.iter_errors(example)), [])
        graph = KnowledgeGraph.from_dict(example)
        self.assertEqual(list(validator.iter_errors(graph.to_dict())), [])

    def test_schema_and_model_both_reject_credentialed_source_url(self):
        root = Path(__file__).resolve().parents[1]
        schema = json.loads((root / "schemas" / "graph.schema.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        raw = json.loads((root / "examples" / "graph.json").read_text(encoding="utf-8"))
        source = next(node for node in raw["nodes"] if node["type"] == "source")
        source["canonical_url"] = "https://user:pass@example.org/source"
        self.assertTrue(list(validator.iter_errors(raw)))
        with self.assertRaises(ValueError):
            KnowledgeGraph.from_dict(raw)

    def test_schema_and_model_both_reject_whitespace_only_label(self):
        root = Path(__file__).resolve().parents[1]
        schema = json.loads((root / "schemas" / "graph.schema.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        raw = json.loads((root / "examples" / "graph.json").read_text(encoding="utf-8"))
        raw["nodes"][0]["label"] = "   "
        self.assertTrue(list(validator.iter_errors(raw)))
        with self.assertRaises(ValueError):
            KnowledgeGraph.from_dict(raw)

    def test_schema_and_model_both_reject_naive_graph_timestamp(self):
        root = Path(__file__).resolve().parents[1]
        schema = json.loads((root / "schemas" / "graph.schema.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        raw = json.loads((root / "examples" / "graph.json").read_text(encoding="utf-8"))
        raw["created_at"] = "2026-01-01T00:00:00"
        self.assertTrue(list(validator.iter_errors(raw)))
        with self.assertRaises(ValueError):
            KnowledgeGraph.from_dict(raw)

if __name__ == "__main__":
    unittest.main()
