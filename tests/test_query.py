import unittest
from test_graph import graph_fixture
from intelligence_knowledge_graph.query import neighbors, find_paths

class QueryTests(unittest.TestCase):
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

if __name__ == "__main__":
    unittest.main()
