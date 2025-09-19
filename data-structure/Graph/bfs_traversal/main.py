from collections import deque

def bfs(graph, s):
    n = len(graph)
    prev = [None] * n
    visited = [False] * n
    visited[s] = True
    q = deque()
    q.append(s)
    while q:
        node = q.popleft()
        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                prev[neighbor] = node
                q.append(neighbor)
    return prev

def reconstruct_path(s, e, prev):
    path = []
    at = e
    while at is not None:
        path.append(at)
        at = prev[at]
    path.reverse()
    if path[0] == s:
        return path
    return []

# Example graph as adjacency list:
graph = {
    0: [9,7,11],
    1: [10],
    2: [3],
    3: [4],
    4: [],
    5: [],
    6: [5],
    7: [6,3,11],
    8: [1,12],
    9: [8,10],
    10: [1],
    11: [],
    12: [2],
}

prev = bfs(graph, 0)
print(prev)
print(reconstruct_path(0, 4, prev))  # Output: [0, 7, 3, 4]
