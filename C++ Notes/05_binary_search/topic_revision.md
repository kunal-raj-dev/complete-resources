# ⚡ Rapid Revision — Topic 05: Binary Search & Answer Spaces

> **Target:** 5-minute pre-interview refresher on all Binary Search patterns, formulas, invariants, and edge cases.

---

## 🔑 Core Invariants Summary

| Pattern | Search Space | Key Decision Formula | Direction Rule |
|---|---|---|---|
| **Classical Binary Search** | Monotonic array | `nums[mid] == target` | `nums[mid] < target ? low = mid + 1 : high = mid - 1` |
| **Rotated Sorted Array** | Half-sorted array | Identify sorted half: `nums[low] <= nums[mid]` | Target inside sorted half? Search it; else search unsorted half |
| **Peak in Mountain** | Bitonic array | `nums[mid] < nums[mid + 1]` | Ascending slope: `low = mid + 1`; Descending slope: `high = mid` |
| **Single Element** | Sorted pairs | `nums[mid] == nums[mid ^ 1]` | True: left side clean $\to$ `low = mid + 1`; False: `high = mid - 1` |
| **Book Allocation** | Answer $[\max(arr), \sum arr]$ | `isValid(mid)` checks if student count $\le M$ | Feasible: `ans = mid, high = mid - 1`; Infeasible: `low = mid + 1` |
| **Aggressive Cows** | Answer $[1, \text{stall}_{max} - \text{stall}_{min}]$ | `canPlace(mid)` checks if cow count $\ge K$ | Feasible: `ans = mid, low = mid + 1`; Infeasible: `high = mid - 1` |

---

## ⚠️ High-Risk Traps
1. **Integer Overflow:** Always use `mid = low + (high - low) / 2`. Never `(low + high) / 2`.
2. **Rotated Search Invariant:** Must use `<=` when checking `nums[low] <= nums[mid]` to handle 2-element subproblems.
3. **Answer Space Boundaries:**
   - Min-Max partition: `low = max(arr)`, `high = sum(arr)`.
   - Max-Min separation: `low = 1`, `high = arr[n-1] - arr[0]` (array must be sorted!).
