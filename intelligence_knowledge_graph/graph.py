"""Bounded in-memory graph with immutable public mappings and referential integrity."""
from types import MappingProxyType

from .models import Edge, Node, valid_time


class KnowledgeGraph:
    def __init__(self, graph_id, created_at, *, max_nodes=10_000, max_edges=50_000):
        if not isinstance(graph_id, str) or not graph_id.strip() or len(graph_id) > 128:
            raise ValueError("graph_id must contain 1..128 characters")
        if not valid_time(created_at):
            raise ValueError("created_at must be timezone-aware")
        if isinstance(max_nodes, bool) or not isinstance(max_nodes, int) or not 1 <= max_nodes <= 100_000:
            raise ValueError("max_nodes must be an integer in [1, 100000]")
        if isinstance(max_edges, bool) or not isinstance(max_edges, int) or not 1 <= max_edges <= 500_000:
            raise ValueError("max_edges must be an integer in [1, 500000]")
        self._graph_id = graph_id
        self._created_at = created_at
        self._max_nodes = max_nodes
        self._max_edges = max_edges
        self._nodes = {}
        self._edges = {}

    @property
    def graph_id(self):
        return self._graph_id

    @property
    def created_at(self):
        return self._created_at

    @property
    def max_nodes(self):
        return self._max_nodes

    @property
    def max_edges(self):
        return self._max_edges

    @property
    def nodes(self):
        return MappingProxyType(self._nodes)

    @property
    def edges(self):
        return MappingProxyType(self._edges)

    def add_node(self, node):
        if not isinstance(node, Node):
            raise TypeError("node must be a Node")
        try:
            node = Node.from_dict(node.to_dict())
        except Exception as exc:
            raise ValueError("node does not satisfy the validated record contract") from exc
        if node.id in self._nodes:
            raise ValueError("duplicate node id")
        if len(self._nodes) >= self._max_nodes:
            raise ValueError("graph node capacity reached")
        if node.type == "evidence":
            source_id = node.data["source_node_id"]
            if source_id not in self._nodes or self._nodes[source_id].type != "source":
                raise ValueError("evidence must reference an existing source node")
        self._nodes[node.id] = node
        return node

    def add_edge(self, edge):
        if not isinstance(edge, Edge):
            raise TypeError("edge must be an Edge")
        try:
            edge = Edge.from_dict(edge.to_dict())
        except Exception as exc:
            raise ValueError("edge does not satisfy the validated record contract") from exc
        if edge.id in self._edges:
            raise ValueError("duplicate edge id")
        if len(self._edges) >= self._max_edges:
            raise ValueError("graph edge capacity reached")
        if edge.from_id not in self._nodes or edge.to_id not in self._nodes:
            raise ValueError("edge endpoints must exist")
        for ref in edge.evidence_refs:
            if ref not in self._nodes or self._nodes[ref].type != "evidence":
                raise ValueError("edge evidence_refs must point to evidence nodes")
        self._edges[edge.id] = edge
        return edge

    def to_dict(self):
        return {"graph_id": self.graph_id, "contract_version": "0.1.0",
                "created_at": self.created_at,
                "nodes": [self._nodes[k].to_dict() for k in sorted(self._nodes)],
                "edges": [self._edges[k].to_dict() for k in sorted(self._edges)]}

    @classmethod
    def from_dict(cls, raw):
        if not isinstance(raw, dict) or set(raw) != {"graph_id", "contract_version", "created_at", "nodes", "edges"}:
            raise ValueError("invalid graph document fields")
        if raw["contract_version"] != "0.1.0":
            raise ValueError("unsupported contract version")
        if not isinstance(raw["nodes"], list) or not isinstance(raw["edges"], list):
            raise ValueError("nodes and edges must be arrays")
        graph = cls(raw["graph_id"], raw["created_at"])
        if len(raw["nodes"]) > graph.max_nodes or len(raw["edges"]) > graph.max_edges:
            raise ValueError("graph document exceeds node or edge capacity")
        parsed_nodes = [Node.from_dict(item) for item in raw["nodes"]]
        priority = {"source": 0, "entity": 1, "evidence": 2}
        for node in sorted(parsed_nodes, key=lambda item: priority[item.type]):
            graph.add_node(node)
        for item in raw["edges"]:
            graph.add_edge(Edge.from_dict(item))
        return graph
