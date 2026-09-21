# 💼 Topic 10 Interview Question Bank: 2D Arrays & Matrices

> **Curated FAANG Question Bank:** Cache effects, staircase search invariants, and spiral matrix pointer management.

---

## 📌 Conceptual & Architectural Questions

### Q1: Why does Staircase Search start at the Top-Right corner `(0, C-1)` or Bottom-Left `(R-1, 0)`?
- **Answer:** At `(0, C-1)`, moving Left strictly decreases values and moving Down strictly increases values. This provides a deterministic decision: if target is smaller, move Left; if larger, move Down. At `(0, 0)` or `(R-1, C-1)`, both available directions either increase or decrease, giving no directional choice.

---

### Q2: How do you rotate an $N \times N$ matrix by 90 degrees clockwise in-place?
- **Answer:**
  1. **Transpose the matrix:** Swap `matrix[i][j]` with `matrix[j][i]` for all $i < j$.
  2. **Reverse each row:** Reverse `matrix[i]` from left to right.
  Both steps are completely in-place, achieving $O(N^2)$ time and $O(1)$ auxiliary space.
