#!/usr/bin/env python3
"""Validate a graph JSON document with the reference implementation."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from intelligence_knowledge_graph import KnowledgeGraph

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path)
    args = parser.parse_args(argv)
    try:
        raw = json.loads(args.document.read_text(encoding="utf-8"))
        graph = KnowledgeGraph.from_dict(raw)
        print(json.dumps({"status":"valid","graph_id":graph.graph_id,
                          "nodes":len(graph.nodes),"edges":len(graph.edges)}, sort_keys=True))
        return 0
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
        print(f"graph validation error: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
