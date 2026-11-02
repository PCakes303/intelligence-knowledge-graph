"""Provenance-aware knowledge graph reference implementation."""
from .graph import KnowledgeGraph
from .models import Edge, Node
from .query import find_paths, neighbors

__version__ = "0.1.0"
__all__ = ["KnowledgeGraph", "Node", "Edge", "find_paths", "neighbors"]
