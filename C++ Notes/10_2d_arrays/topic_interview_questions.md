# 💼 Topic Interview Question Bank — Topic 10: 2D Arrays

---

### Q1: Why can't we start Staircase Search at (0, 0) or (R - 1, C - 1)?
**Answer:**
At `(0, 0)`, moving right increases value, and moving down *also* increases value. If target is greater than `matrix[0][0]`, we cannot know whether to proceed right or down (non-deterministic branching).
At `(0, C - 1)` (or `(R - 1, 0)`), one direction strictly decreases value (left) while the other strictly increases value (down). This eliminates an entire row or column deterministically in $O(1)$.
