# 💼 Topic Interview Question Bank — Topic 11: Hashing

---

### Q1: Why does Sliding Window fail for "Subarray Sum Equals K" when negative numbers are present?
**Answer:**
The two-pointer sliding window technique relies on monotonicity: expanding the window increases the window sum, and contracting the window decreases the window sum. When negative integers exist, adding an element can decrease the sum, and removing an element can increase it. Monotonicity is violated; thus, Prefix Sum + Hash Map is strictly required.
