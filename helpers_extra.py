import heapq
from collections import deque
from typing import (
    Callable,
    Optional,
    Set,
)
from pprint import pp


def bfs(
    graph,
    start,
    hook_fn: Optional[Callable] = None,
) -> Set[object]:
    visited = set()
    queue = deque([start])

    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            if callable(hook_fn):
                hook_fn(graph, vertex, visited)
            visited.add(vertex)
            queue.extend(set(graph[vertex]) - visited)

    return visited


def dfs(
    graph,
    start,
    visited=None,
    hook_fn: Optional[Callable] = None,
) -> Set[object]:
    if visited is None:
        visited = set()

    visited.add(start)
    if callable(hook_fn):
        hook_fn(graph, start, visited)

    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited, hook_fn=hook_fn)

    return visited


def dfs_topological_sort(graph, node, visited, stack):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_topological_sort(graph, neighbor, visited, stack)
    stack.append(node)


def topological_sort(graph):
    visited = set()
    stack = []
    for node in graph:
        if node not in visited:
            dfs_topological_sort(graph, node, visited, stack)
    return stack[::-1]


def find_connected_components(graph):
    visited = set()
    components = []

    def explore(node):
        if node in visited:
            return
        visited.add(node)
        component.append(node)
        for neighbor in graph[node]:
            explore(neighbor)

    for node in graph:
        if node not in visited:
            component = []
            explore(node)
            components.append(component)

    return components


def bfs_shortest_path(graph, start, end):
    visited = set()
    queue = deque([(start, [start])])

    while queue:
        vertex, path = queue.popleft()
        if vertex == end:
            return path
        for neighbor in set(graph[vertex]) - visited:
            visited.add(neighbor)
            queue.append((neighbor, path + [neighbor]))

    return None


def dfs_cycle_detection(graph, node, visited, rec_stack):
    visited.add(node)
    rec_stack.add(node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            if dfs_cycle_detection(graph, neighbor, visited, rec_stack):
                return True
        elif neighbor in rec_stack:
            return True

    rec_stack.remove(node)
    return False


def has_cycle(graph):
    visited = set()
    rec_stack = set()
    for node in graph:
        if node not in visited:
            if dfs_cycle_detection(graph, node, visited, rec_stack):
                return True
    return False


def dijkstra(graph, start):
    min_heap = [(0, start)]
    distances = {start: 0}
    while min_heap:
        current_distance, current_node = heapq.heappop(min_heap)
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if neighbor not in distances or distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(min_heap, (distance, neighbor))
    return distances


def bellman_ford(graph, start):
    distance = {node: float('inf') for node in graph}
    distance[start] = 0

    for _ in range(len(graph) - 1):
        for node in graph:
            for neighbor, weight in graph[node]:
                if distance[node] + weight < distance[neighbor]:
                    distance[neighbor] = distance[node] + weight

    for node in graph:
        for neighbor, weight in graph[node]:
            if distance[node] + weight < distance[neighbor]:
                return "Negative weight cycle detected"

    return distance


def floyd_warshall(graph):
    dist = {node: {neighbor: float('inf') for neighbor in graph} for node in graph}
    for node in graph:
        dist[node][node] = 0
        for neighbor, weight in graph[node].items():
            dist[node][neighbor] = weight

    for k in graph:
        for i in graph:
            for j in graph:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


def find(parent, i):
    if parent[i] == i:
        return i
    return find(parent, parent[i])


def union(parent, rank, x, y):
    xroot = find(parent, x)
    yroot = find(parent, y)

    if rank[xroot] < rank[yroot]:
        parent[xroot] = yroot
    elif rank[xroot] > rank[yroot]:
        parent[yroot] = xroot
    else:
        parent[yroot] = xroot
        rank[xroot] += 1


def kruskal(graph):
    result = []
    i, e = 0, 0
    graph = sorted(graph, key=lambda item: item[2])
    parent, rank = [], []
    for node in range(len(graph)):
        parent.append(node)
        rank.append(0)
    while e < len(graph) - 1:
        u, v, w = graph[i]
        i = i + 1
        x = find(parent, u)
        y = find(parent, v)
        if x != y:
            e = e + 1
            result.append((u, v, w))
            union(parent, rank, x, y)
    return result


class Node:
    def __init__(self, name, heuristic_value=0):
        self.name = name
        self.heuristic_value = heuristic_value

    def __lt__(self, other):
        return self.heuristic_value < other.heuristic_value


def a_star(graph, start, end, heuristic):
    open_set = []
    heapq.heappush(open_set, (0, start))

    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0

    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic[start]

    came_from = {}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for neighbor in graph[current]:
            tentative_g_score = g_score[current] + graph[current][neighbor]
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic[neighbor]
                if neighbor not in [item[1] for item in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None


def main():
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': []
    }
    print("Graph:")
    pp(graph, width=20)
    print()

    hook_fn = lambda g, s, v: print(s, end="")  # consecutive s == path

    for name, fn in [("Breadth", bfs), ("Depth", dfs)]:
        print(f"{name}-first search:")
        visited = fn(graph, "A", hook_fn=hook_fn)
        print()


if __name__ == '__main__':
    main()
