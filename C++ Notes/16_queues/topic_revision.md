# ⚡ Rapid Revision — Topic 16: Queues & Deques

> **Target:** 5-minute pre-interview refresher on FIFO structures and Deque invariants.

---

## 🔑 Key Takeaways
- **Circular Queue:** `rear = (rear + 1) % K`, `front = (front + 1) % K`.
- **Sliding Window Max:** Deque stores indices with values in decreasing order. Front is always maximum.
- **Gas Station:** If `sum(gas) >= sum(cost)`, a solution is guaranteed to exist. Reset start whenever `currTank < 0`.
