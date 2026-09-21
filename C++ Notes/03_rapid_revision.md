# ⚡ 03: Rapid Revision Cheat Sheet (Last-Minute FAANG Prep)

> **High-Density Review:** The ultimate high-yield summary designed for 24-hour pre-interview review, formula recall, complexity tables, and boundary trap checklists.

---

## 1. Syntax & Core Language Cheat Sheet
- **Fast I/O:**
  ```cpp
  void fastIO() {
      ios_base::sync_with_stdio(false);
      cin.tie(nullptr);
  }
  ```
- **Line break:** Use `'\n'` instead of `endl` (avoids buffer flushing).
- **Safe Mid:** `mid = start + (end - start) / 2`.
- **Signed Integer Boundaries:**
  - 32-bit `int`: $[-2.14 \times 10^9, +2.14 \times 10^9]$ ($\approx 2^{31}-1$).
  - 64-bit `long long`: $\approx \pm 9 \times 10^{18}$ ($\approx 2^{63}-1$).
  - Literal suffix: Always append `LL` to avoid intermediate 32-bit truncation: `1LL << 40`.

---

## 2. Bitwise Manipulation Master Formulas

```
Check Odd / Even:         (n & 1) != 0
Check Power of 2:         (n > 0) && ((n & (n - 1)) == 0)
Clear Lowest Set Bit:     n = n & (n - 1)
Isolate Lowest Set Bit:   lowest = n & (-n)
Check k-th Bit:           (n & (1 << k)) != 0
Set k-th Bit:             n |= (1 << k)
Clear k-th Bit:           n &= ~(1 << k)
Toggle k-th Bit:          n ^= (1 << k)
XOR Cancellation:         X ^ X = 0, X ^ 0 = X
Two's Complement:         -X = ~X + 1
```

---

## 3. Algorithm Complexity Matrix

| Problem / Algorithm | Best Case Time | Worst Case Time | Auxiliary Space | Key Invariant |
|---|---|---|---|---|
| **Linear Search** | $O(1)$ | $O(N)$ | $O(1)$ | Sequential scan |
| **Binary Search** | $O(1)$ | $O(\log N)$ | $O(1)$ | Monotonic search space |
| **Kadane's Algorithm** | $O(N)$ | $O(N)$ | $O(1)$ | Discard negative prefix sums |
| **Boyer-Moore Voting** | $O(N)$ | $O(N)$ | $O(1)$ | Pairwise distinct cancellation |
| **Container With Most Water** | $O(N)$ | $O(N)$ | $O(1)$ | Always move the shorter line |
| **Product Except Self** | $O(N)$ | $O(N)$ | $O(1)$ | `ans = prefix[i-1] * suffix[i+1]` |
| **Binary Exponentiation** | $O(1)$ | $O(\log N)$ | $O(1)$ | Square base, halve exponent |
| **Rotated Sorted Search** | $O(1)$ | $O(\log N)$ | $O(1)$ | At least one half is always sorted |
| **Peak in Mountain Array** | $O(1)$ | $O(\log N)$ | $O(1)$ | Follow positive slope gradient |
| **Merge Sort** | $O(N \log N)$ | $O(N \log N)$ | $O(N)$ | Stable divide and conquer |
| **Quick Sort** | $O(N \log N)$ | $O(N^2)$ | $O(\log N)$ | In-place partitioning around pivot |
| **Floyd's Cycle Finding** | $O(1)$ | $O(N)$ | $O(1)$ | Fast travels 2x speed of slow |
| **LRU Cache** | $O(1)$ | $O(1)$ | $O(\text{Capacity})$ | Doubly Linked List + Hash Map |

---

## 4. The 5 Must-Remember Code Templates

### Template 1: Kadane's Algorithm
```cpp
int maxSubArray(const vector<int>& nums) {
    int maxSum = INT_MIN, currSum = 0;
    for (int x : nums) {
        currSum += x;
        maxSum = max(maxSum, currSum);
        if (currSum < 0) currSum = 0;
    }
    return maxSum;
}
```

### Template 2: Binary Exponentiation
```cpp
double myPow(double x, int n) {
    long long p = n;
    if (p < 0) { x = 1.0 / x; p = -p; }
    double ans = 1.0;
    while (p > 0) {
        if (p & 1) ans *= x;
        x *= x;
        p >>= 1;
    }
    return ans;
}
```

### Template 3: Reverse Linked List In-Place
```cpp
struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(nullptr) {}
};

ListNode* reverseList(ListNode* head) {
    ListNode *prev = nullptr, *curr = head;
    while (curr) {
        ListNode* nextNode = curr->next;
        curr->next = prev;
        prev = curr;
        curr = nextNode;
    }
    return prev;
}
```

### Template 4: Floyd's Cycle Entry Point
```cpp
ListNode *detectCycle(ListNode *head) {
    ListNode *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            slow = head;
            while (slow != fast) {
                slow = slow->next;
                fast = fast->next;
            }
            return slow; // Cycle start
        }
    }
    return nullptr;
}
```

### Template 5: Backtracking Template (Subsets II)
```cpp
void backtrack(int idx, vector<int>& nums, vector<int>& curr, vector<vector<int>>& res) {
    res.push_back(curr);
    for (int i = idx; i < nums.size(); i++) {
        if (i > idx && nums[i] == nums[i-1]) continue; // Skip duplicates
        curr.push_back(nums[i]);
        backtrack(i + 1, nums, curr, res);
        curr.pop_back(); // Undo choice
    }
}
```

---

## 5. Critical Interview Traps Checklist
1. **Integer Division:** `5 / 2 == 2`. Write `(double)5 / 2` for `2.5`.
2. **Modulo on Negative Numbers:** In C++, `-7 % 3 == -1`. To get a positive mathematical modulo, use `((a % m) + m) % m`.
3. **Vectors by Reference:** Always declare function arguments as `const vector<int>& vec` to prevent an $O(N)$ deep copy.
4. **All-Negative Subarrays:** Initialize `maxSum = INT_MIN` rather than `0` in Kadane's algorithm.
5. **Dangling Local Pointers:** Never return a pointer or reference to a local stack variable.
6. **Bit Shift Overflow:** Shifting a 32-bit `int` by $\ge 31$ bits is Undefined Behavior. Use `1LL << k`.
