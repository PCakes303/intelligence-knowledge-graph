import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from intelligence_knowledge_graph import KnowledgeGraph, Node
from test_graph import graph_fixture

ROOT = Path(__file__).resolve().parents[1]


class GraphSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads((ROOT / "schemas" / "graph.schema.json").read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())

    def test_reference_graph_matches_schema_and_model(self):
        document = graph_fixture().to_dict()
        self.assertEqual(list(self.validator.iter_errors(document)), [])
        self.assertEqual(KnowledgeGraph.from_dict(document).to_dict(), document)

    def test_scalar_metadata_matches_schema_and_model(self):
        document = graph_fixture().to_dict()
        document["nodes"][0]["metadata"] = {"source_class": "synthetic", "rank": 2, "verified": False}
        self.assertEqual(list(self.validator.iter_errors(document)), [])
        KnowledgeGraph.from_dict(document)

    def test_nested_metadata_rejected_by_schema_and_model(self):
        document = graph_fixture().to_dict()
        document["nodes"][0]["metadata"] = {"nested": {"unsafe": "unbounded"}}
        self.assertTrue(list(self.validator.iter_errors(document)))
        with self.assertRaises(ValueError):
            Node.from_dict(document["nodes"][0])

    def test_unknown_graph_field_rejected_by_schema_and_model(self):
        document = graph_fixture().to_dict()
        document["fetch_url"] = "https://example.org"
        self.assertTrue(list(self.validator.iter_errors(document)))
        with self.assertRaises(ValueError):
            KnowledgeGraph.from_dict(document)

    def test_excessive_evidence_refs_rejected_by_schema_and_model(self):
        edge = graph_fixture().to_dict()["edges"][0]
        edge["evidence_refs"] = [f"ev{i}" for i in range(101)]
        self.assertTrue(list(self.validator.iter_errors(edge)))
        with self.assertRaises(ValueError):
            from intelligence_knowledge_graph import Edge
            Edge.from_dict(edge)


if __name__ == "__main__":
    unittest.main()
