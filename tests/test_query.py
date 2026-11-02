import unittest
from types import SimpleNamespace
from test_graph import graph_fixture
from intelligence_knowledge_graph.query import neighbors, find_paths

class QueryTests(unittest.TestCase):

    def test_malformed_direction_and_node_id_fail_cleanly(self):
        graph = graph_fixture()
        with self.assertRaises(ValueError):
            neighbors(graph, "ev", direction=[])
        with self.assertRaises(KeyError):
            neighbors(graph, ["ev"])
        with self.assertRaises(KeyError):
            find_paths(graph, ["ev"], "e")

    def test_neighbors(self):
        graph = graph_fixture()
        self.assertEqual(len(neighbors(graph, "ev", direction="out")), 1)
    def test_bounded_path(self):
        graph = graph_fixture()
        self.assertEqual(find_paths(graph, "ev", "e", max_depth=1), [["ev", "e"]])
        self.assertEqual(find_paths(graph, "ev", "e", max_depth=0), [])
    def test_depth_limit(self):
        with self.assertRaises(ValueError):
            find_paths(graph_fixture(), "ev", "e", max_depth=99)
    def test_direction_validation(self):
        with self.assertRaises(ValueError):
            neighbors(graph_fixture(), "ev", direction="sideways")

    def test_path_query_expansion_budget_is_enforced(self):
        graph = SimpleNamespace(
            nodes={name: SimpleNamespace(id=name) for name in ("a", "b", "c", "d")},
            edges={
                "ab": SimpleNamespace(id="ab", from_id="a", to_id="b", predicate="rel"),
                "ac": SimpleNamespace(id="ac", from_id="a", to_id="c", predicate="rel"),
                "bd": SimpleNamespace(id="bd", from_id="b", to_id="d", predicate="rel"),
                "cd": SimpleNamespace(id="cd", from_id="c", to_id="d", predicate="rel"),
            },
        )
        with self.assertRaisesRegex(ValueError, "expansion budget"):
            find_paths(graph, "a", "d", max_expansions=1)

    def test_path_query_queue_budget_is_enforced(self):
        graph = SimpleNamespace(
            nodes={name: SimpleNamespace(id=name) for name in ("a", "b", "c", "d")},
            edges={
                "ab": SimpleNamespace(id="ab", from_id="a", to_id="b", predicate="rel"),
                "ac": SimpleNamespace(id="ac", from_id="a", to_id="c", predicate="rel"),
                "bd": SimpleNamespace(id="bd", from_id="b", to_id="d", predicate="rel"),
                "cd": SimpleNamespace(id="cd", from_id="c", to_id="d", predicate="rel"),
            },
        )
        with self.assertRaisesRegex(ValueError, "queue budget"):
            find_paths(graph, "a", "d", max_queue=1)

    def test_path_query_edge_scan_budget_is_enforced(self):
        graph = SimpleNamespace(
            nodes={name: SimpleNamespace(id=name) for name in ("a", "b", "c", "d")},
            edges={
                "ab": SimpleNamespace(id="ab", from_id="a", to_id="b", predicate="rel"),
                "ac": SimpleNamespace(id="ac", from_id="a", to_id="c", predicate="rel"),
                "bd": SimpleNamespace(id="bd", from_id="b", to_id="d", predicate="rel"),
                "cd": SimpleNamespace(id="cd", from_id="c", to_id="d", predicate="rel"),
            },
        )
        with self.assertRaisesRegex(ValueError, "edge-scan budget"):
            find_paths(graph, "a", "d", max_edge_scans=1)

    def test_path_query_work_limits_reject_invalid_values(self):
        graph = graph_fixture()
        for name in ("max_expansions", "max_queue", "max_edge_scans"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                find_paths(graph, "ev", "e", **{name: True})

if __name__ == "__main__":
    unittest.main()
