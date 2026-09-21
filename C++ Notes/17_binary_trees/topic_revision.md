# ⚡ Rapid Revision — Topic 17: Binary Trees

> **Target:** 5-minute pre-interview refresher on Binary Tree traversal patterns and algorithms.

---

## 🔑 Key Patterns & Formulas
- **Height:** `1 + max(h(left), h(right))`.
- **Diameter:** `maxDiameter = max(maxDiameter, leftH + rightH)` during height computation ($O(N)$).
- **LCA:** If `left && right` return `root`; else return whichever is non-null.
- **Top View:** BFS with horizontal coordinate `hd`. Record first node encountered at each `hd`.
- **Morris Traversal:** Link predecessor's right to current node. Sever link on second visit. $O(1)$ space.
