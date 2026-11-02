"""Read-only, bounded graph queries."""
from collections import deque

def neighbors(graph, node_id, direction="both", predicate=None):
    if not isinstance(node_id, str) or node_id not in graph.nodes:
        raise KeyError(node_id)
    if not isinstance(direction, str) or direction not in {"both", "in", "out"}:
        raise ValueError("direction must be both, in, or out")
    found = []
    for edge in graph.edges.values():
        if predicate is not None and edge.predicate != predicate:
            continue
        if direction in {"both", "out"} and edge.from_id == node_id:
            found.append((graph.nodes[edge.to_id], edge))
        if direction in {"both", "in"} and edge.to_id == node_id:
            found.append((graph.nodes[edge.from_id], edge))
    return sorted(found, key=lambda pair: (pair[1].id, pair[0].id))

def find_paths(graph, start_id, target_id, max_depth=4, max_paths=100):
    if not isinstance(start_id, str) or not isinstance(target_id, str) or start_id not in graph.nodes or target_id not in graph.nodes:
        raise KeyError("start or target node not found")
    if isinstance(max_depth, bool) or not isinstance(max_depth, int) or not 0 <= max_depth <= 12:
        raise ValueError("max_depth must be an integer from 0 to 12")
    if isinstance(max_paths, bool) or not isinstance(max_paths, int) or not 1 <= max_paths <= 1000:
        raise ValueError("max_paths must be an integer from 1 to 1000")
    if start_id == target_id:
        return [[start_id]]
    queue = deque([(start_id, [start_id])])
    paths = []
    while queue and len(paths) < max_paths:
        current, path = queue.popleft()
        if len(path) - 1 >= max_depth:
            continue
        for node, edge in neighbors(graph, current, "out"):
            if node.id in path:
                continue
            candidate = path + [node.id]
            if node.id == target_id:
                paths.append(candidate)
            else:
                queue.append((node.id, candidate))
            if len(paths) >= max_paths:
                break
    return paths
