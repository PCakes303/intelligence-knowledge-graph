"""In-memory graph with referential integrity."""
from .models import Edge, Node, valid_time

class KnowledgeGraph:
    def __init__(self, graph_id, created_at):
        if not isinstance(graph_id, str) or not graph_id.strip():
            raise ValueError("graph_id required")
        if not valid_time(created_at):
            raise ValueError("created_at must be timezone-aware")
        self.graph_id = graph_id
        self.created_at = created_at
        self.nodes = {}
        self.edges = {}

    def add_node(self, node):
        if not isinstance(node, Node):
            raise TypeError("node must be a validated Node")
        if node.id in self.nodes:
            raise ValueError("duplicate node id")
        if node.type == "evidence":
            source_id = node.data["source_node_id"]
            if source_id not in self.nodes or self.nodes[source_id].type != "source":
                raise ValueError("evidence must reference an existing source node")
        self.nodes[node.id] = node
        return node

    def add_edge(self, edge):
        if not isinstance(edge, Edge):
            raise TypeError("edge must be a validated Edge")
        if edge.id in self.edges:
            raise ValueError("duplicate edge id")
        if edge.from_id not in self.nodes or edge.to_id not in self.nodes:
            raise ValueError("edge endpoints must exist")
        for ref in edge.evidence_refs:
            if ref not in self.nodes or self.nodes[ref].type != "evidence":
                raise ValueError("edge evidence_refs must point to evidence nodes")
        self.edges[edge.id] = edge
        return edge

    def to_dict(self):
        return {"graph_id": self.graph_id, "contract_version": "0.1.0",
                "created_at": self.created_at,
                "nodes": [self.nodes[k].to_dict() for k in sorted(self.nodes)],
                "edges": [self.edges[k].to_dict() for k in sorted(self.edges)]}

    @classmethod
    def from_dict(cls, raw):
        if not isinstance(raw, dict) or set(raw) != {"graph_id", "contract_version", "created_at", "nodes", "edges"}:
            raise ValueError("invalid graph document fields")
        if raw["contract_version"] != "0.1.0":
            raise ValueError("unsupported contract version")
        if not isinstance(raw["nodes"], list) or not isinstance(raw["edges"], list):
            raise ValueError("nodes and edges must be arrays")
        from .models import Node, Edge
        graph = cls(raw["graph_id"], raw["created_at"])
        for item in raw["nodes"]:
            graph.add_node(Node.from_dict(item))
        for item in raw["edges"]:
            graph.add_edge(Edge.from_dict(item))
        return graph
