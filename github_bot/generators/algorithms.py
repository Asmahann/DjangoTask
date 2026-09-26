"""
Algorithms & Data Structures Generator for GitHub Activity Bot.
Generates clean algorithm and data structure implementations in Python.
"""
import random
import os

TEMPLATES = [
    {
        "filename": "trie_autocomplete.py",
        "commit": "feat(algo): implement Trie data structure with prefix autocomplete",
        "content": '''"""
Trie (Prefix Tree) Data Structure with Autocomplete functionality.
"""
from typing import List, Dict, Optional


class TrieNode:
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word: bool = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Inserts a word into the Trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """Returns True if the exact word is in the Trie."""
        node = self._find_node(word)
        return node is not None and node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """Returns True if there is any word in the Trie that starts with prefix."""
        return self._find_node(prefix) is not None

    def autocomplete(self, prefix: str) -> List[str]:
        """Returns all words stored in the Trie starting with the given prefix."""
        results: List[str] = []
        node = self._find_node(prefix)
        if node:
            self._dfs(node, prefix, results)
        return results

    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _dfs(self, node: TrieNode, current_prefix: str, results: List[str]) -> None:
        if node.is_end_of_word:
            results.append(current_prefix)
        for char, child in node.children.items():
            self._dfs(child, current_prefix + char, results)


if __name__ == "__main__":
    trie = Trie()
    words = ["algorithm", "algorithmic", "algebra", "python", "pyramid", "pytest"]
    for w in words:
        trie.insert(w)

    print("Autocomplete for 'alg':", trie.autocomplete("alg"))
    print("Autocomplete for 'py':", trie.autocomplete("py"))
'''
    },
    {
        "filename": "graph_dijkstra.py",
        "commit": "feat(algo): implement Dijkstra shortest path algorithm with priority queue",
        "content": '''"""
Dijkstra Shortest Path Algorithm implementation using min-heap priority queue.
"""
import heapq
from typing import Dict, List, Tuple


def dijkstra(graph: Dict[str, List[Tuple[str, int]]], start: str) -> Tuple[Dict[str, int], Dict[str, str]]:
    """
    Computes shortest distances from start node to all reachable nodes in weighted graph.
    Returns (distances, previous_nodes).
    """
    distances: Dict[str, int] = {node: float('inf') for node in graph}
    previous: Dict[str, str] = {node: None for node in graph}
    distances[start] = 0

    # Priority queue storing (distance, node)
    pq: List[Tuple[int, str]] = [(0, start)]

    while pq:
        current_dist, current_node = heapq.heappop(pq)

        if current_dist > distances[current_node]:
            continue

        for neighbor, weight in graph.get(current_node, []):
            distance = current_dist + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    return distances, previous


def reconstruct_path(previous: Dict[str, str], start: str, end: str) -> List[str]:
    """Reconstructs path from start to end using previous nodes mapping."""
    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        if curr == start:
            break
        curr = previous.get(curr)
    return path[::-1] if path and path[-1] == start else []


if __name__ == "__main__":
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('A', 4), ('C', 1), ('D', 5)],
        'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
        'D': [('B', 5), ('C', 8), ('E', 2)],
        'E': [('C', 10), ('D', 2)]
    }
    dists, prevs = dijkstra(graph, 'A')
    print("Distances from A:", dists)
    print("Shortest path A -> E:", reconstruct_path(prevs, 'A', 'E'))
'''
    },
    {
        "filename": "avl_tree_balance.py",
        "commit": "feat(algo): implement self-balancing AVL Binary Search Tree",
        "content": '''"""
AVL Tree Implementation (Self-Balancing Binary Search Tree).
Supports insertion with LL, RR, LR, RL node rotations.
"""

class Node:
    def __init__(self, key: int):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def get_height(self, node: Node) -> int:
        return node.height if node else 0

    def get_balance(self, node: Node) -> int:
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def right_rotate(self, z: Node) -> Node:
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def left_rotate(self, z: Node) -> Node:
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, root: Node, key: int) -> Node:
        if not root:
            return Node(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Left Left Case
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)
        # Right Right Case
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)
        # Left Right Case
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        # Right Left Case
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def inorder(self, root: Node, res: list):
        if root:
            self.inorder(root.left, res)
            res.append(root.key)
            self.inorder(root.right, res)


if __name__ == "__main__":
    tree = AVLTree()
    root = None
    for key in [10, 20, 30, 40, 50, 25]:
        root = tree.insert(root, key)
    res = []
    tree.inorder(root, res)
    print("Inorder traversal of balanced AVL tree:", res)
'''
    }
]


def generate_algorithm(target_dir: str) -> tuple[str, str, str]:
    """Generates an algorithm file in target_dir and returns (rel_filepath, content, commit_message)."""
    template = random.choice(TEMPLATES)
    dest_path = os.path.join(target_dir, template["filename"])
    return dest_path, template["content"], template["commit"]
