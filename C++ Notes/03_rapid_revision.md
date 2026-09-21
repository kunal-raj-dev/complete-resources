# ⚡ 03: Rapid Revision Cheat Sheet (Last-Minute FAANG Prep)

> **High-Density Review:** The ultimate high-yield summary designed for 24-hour pre-interview review, formula recall, complexity tables, and boundary trap checklists across all 144 lectures.

---

## 1. Syntax & Core Language Cheat Sheet
- **Fast I/O:** `ios_base::sync_with_stdio(false); cin.tie(nullptr);`
- **Safe Midpoint:** `mid = low + (high - low) / 2;`
- **64-bit Suffix:** Always append `LL` to avoid 32-bit truncation: `1LL << 40`.

---

## 2. Universal Bitwise Formulas
```
Check Odd:                (n & 1) != 0
Check Power of 2:         (n > 0) && ((n & (n - 1)) == 0)
Clear Lowest Set Bit:     n &= (n - 1)
Isolate Lowest Set Bit:   n & (-n)
XOR Cancellation:         X ^ X = 0, X ^ 0 = X
Two's Complement:         -X = ~X + 1
```

---

## 3. Algorithm Complexity & Invariant Matrix

| Domain | Problem / Pattern | Time (Worst) | Space | Key Invariant / Formula |
|---|---|---|---|---|
| **Arrays** | Kadane's Algorithm | $O(N)$ | $O(1)$ | Reset `currSum = 0` when negative |
| **Arrays** | Boyer-Moore Voting | $O(N)$ | $O(1)$ | Pairwise distinct cancellation |
| **Binary Search** | Rotated Search | $O(\log N)$ | $O(1)$ | One half is always sorted (`nums[l] <= nums[m]`) |
| **Binary Search** | Search on Answer | $O(N \log(\text{Range}))$ | $O(1)$ | Monotonic feasibility predicate |
| **Sorting** | DNF 3-Way Partition | $O(N)$ | $O(1)$ | 4 regions; do not increment `mid` on swap with `high` |
| **Sorting** | Next Permutation | $O(N)$ | $O(1)$ | Pivot from right $\to$ swap with successor $\to$ reverse suffix |
| **Maths** | Sieve of Eratosthenes| $O(N \log \log N)$ | $O(N)$ | Inner loop starts at $i \times i$ |
| **Maths** | Euclidean GCD | $O(\log(\min(a, b)))$| $O(1)$ | `gcd(a, b) = b == 0 ? a : gcd(b, a % b)` |
| **Matrix** | Staircase Search | $O(R + C)$ | $O(1)$ | Top-Right: `val > target ? c-- : r++` |
| **Hashing** | Subarray Sum = K | $O(N)$ | $O(N)$ | Prefix sum frequency: `count += mp[curr - K]` |
| **Strings** | Sliding Window Perm | $O(N)$ | $O(1)$ | 26-char frequency matching |
| **Trees** | Diameter of BT | $O(N)$ | $O(H)$ | Bottom-up height + diameter combination |
| **Trees** | Morris Traversal | $O(N)$ | $O(1)$ | Temporary predecessor threading |
| **BST** | Validate BST | $O(N)$ | $O(H)$ | Propagate `(minVal, maxVal)` bounds |
| **Stacks** | Monotonic Stack | $O(N)$ | $O(N)$ | Aggregate amortized $O(1)$ per push/pop |
| **Stacks** | Trapping Rainwater | $O(N)$ | $O(1)$ | Two-pointer inward boundary scan |
| **Queues** | Sliding Window Max | $O(N)$ | $O(k)$ | Monotonic decreasing deque storing indices |
| **Graphs** | Dijkstra's Algorithm| $O((V + E) \log V)$ | $O(V)$ | Min-heap greedy relaxation |
| **Graphs** | Tarjan's Bridges | $O(V + E)$ | $O(V)$ | Bridge condition: `low[v] > tin[u]` |
| **Graphs** | Kosaraju SCC | $O(V + E)$ | $O(V)$ | Finish stack $\to$ Transpose $\to$ DFS components |
| **DP** | 0/1 Knapsack 1D | $O(N \times W)$ | $O(W)$ | Reverse capacity loop: `for (w = W; w >= wt[i]; w--)` |

---

## 4. Universal Code Templates

### Template 1: DNF Sort 0s, 1s, 2s
```cpp
void sortColors(vector<int>& nums) {
    int low = 0, mid = 0, high = nums.size() - 1;
    while (mid <= high) {
        if (nums[mid] == 0) swap(nums[low++], nums[mid++]);
        else if (nums[mid] == 1) mid++;
        else swap(nums[mid], nums[high--]);
    }
}
```

### Template 2: 0/1 Knapsack Space-Optimized
```cpp
int knapSack(int W, const vector<int>& wt, const vector<int>& val, int n) {
    vector<int> dp(W + 1, 0);
    for (int i = 0; i < n; i++) {
        for (int w = W; w >= wt[i]; w--) {
            dp[w] = max(dp[w], val[i] + dp[w - wt[i]]);
        }
    }
    return dp[W];
}
```
