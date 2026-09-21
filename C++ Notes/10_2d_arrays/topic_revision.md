# ⚡ Rapid Revision — Topic 10: 2D Arrays

> **Target:** 5-minute pre-interview refresher on 2D array coordinates and matrix algorithms.

---

## 🔑 Key Matrix Formulas
- **Virtual 1D to 2D:** `row = idx / cols`, `col = idx % cols`.
- **Search Matrix I:** Flattened binary search in $O(\log(R \times C))$.
- **Search Matrix II:** Start at `(0, C - 1)`. If `val > target` $\implies \text{col}--$; if `val < target` $\implies \text{row}++$.
- **Spiral Invariant:** Must guard bottom and left passes with `if (top <= bottom)` and `if (left <= right)`.
