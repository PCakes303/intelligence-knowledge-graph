#!/usr/bin/env python3
"""Validate a graph JSON document against schema and reference implementation."""
import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from intelligence_knowledge_graph import KnowledgeGraph


def _reject_constant(value):
    raise ValueError('non-standard JSON number: ' + value)


def _reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON object key: ' + key)
        result[key] = value
    return result

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.document.stat().st_size > 64 * 1024 * 1024:
            raise ValueError('graph document exceeds 64 MiB validation limit')
        text = args.document.read_bytes().decode('utf-8', errors='strict')
        raw = json.loads(text, parse_constant=_reject_constant,
                         object_pairs_hook=_reject_duplicate_keys)
        schema = json.loads((ROOT / "schemas" / "graph.schema.json").read_text(encoding="utf-8"))
        errors = sorted(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(raw),
            key=lambda error: list(error.absolute_path),
        )
        if errors:
            for error in errors:
                print(f"schema error: {list(error.absolute_path)}: {error.message}", file=sys.stderr)
            return 1
        graph = KnowledgeGraph.from_dict(raw)
        print(json.dumps({"status": "valid", "graph_id": graph.graph_id,
                          "nodes": len(graph.nodes), "edges": len(graph.edges)}, sort_keys=True))
        return 0
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError, TypeError, RecursionError) as exc:
        print(f"graph validation error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
