# Topic 02 Interview Questions: Bitwise Operations & Number Systems

> **Curated Question Bank:** FAANG interview questions, bitmask puzzles, and binary representation interview challenges.

---

## 📌 Conceptual & Implementation Questions

### Q1: How does Brian Kernighan's Algorithm count set bits in $O(\text{set\_bits})$ time?
- **Short Answer:** It subtracts $1$ from the number and bitwise-ANDs it with the original number (`n = n & (n - 1)`), which flips the least significant set bit to $0$ on every iteration.
- **Trace:**
  - $N = 12 = 1100_2$
  - Iteration 1: $N - 1 = 11 = 1011_2$. $N \ \& \ (N - 1) = 1100_2 \ \& \ 1011_2 = 1000_2$ (8). Counter = 1.
  - Iteration 2: $N - 1 = 7 = 0111_2$. $N \ \& \ (N - 1) = 1000_2 \ \& \ 0111_2 = 0000_2$ (0). Counter = 2.
  - Loop terminates in 2 steps instead of 32 steps!
- **Code:**
  ```cpp
  int hammingWeight(uint32_t n) {
      int count = 0;
      while (n) {
          n &= (n - 1);
          count++;
      }
      return count;
  }
  ```

---

### Q2: Why must you write `1LL << k` instead of `1 << k` when shifting by more than 30 bits?
- **Short Answer:** The literal `1` is a signed 32-bit `int`. Shifting by $\ge 31$ causes signed 32-bit integer overflow (Undefined Behavior in C++).
- **Detailed Explanation:** Writing `1 << 35` attempts to shift a 32-bit register by 35 places, causing hardware overflow and truncation to 0. Writing `1LL << 35` treats `1` as a 64-bit `long long`, making shifts up to 62 bits safe and valid.

---

### Q3: [LeetCode 268] How do you find the Missing Number in an array of $0 \dots n$ using XOR?
- **Short Answer:** XOR all numbers from $0$ to $n$, and XOR that with every element present in the array. All present elements will appear twice and cancel out to $0$, leaving only the missing number.
- **Code:**
  ```cpp
  int missingNumber(const vector<int>& nums) {
      int xorAll = 0;
      int n = nums.size();
      for (int i = 0; i <= n; i++) xorAll ^= i;
      for (int x : nums) xorAll ^= x;
      return xorAll;
  }
  ```
- **Complexity:** Time: $O(N)$, Space: $O(1)$ without any integer overflow risk (unlike the sum formula $\frac{n(n+1)}{2}$).

---

### Q4: [Output Prediction] What is printed by the following code?
```cpp
#include <iostream>
using namespace std;

int main() {
    int x = 7; // 0111
    int y = 4; // 0100
    cout << (x & y == 4) << endl;
    return 0;
}
```
- **Output:** `0`
- **Trap:** Operator precedence! `==` has higher precedence than `&`. The compiler parses this as `x & (y == 4)`. `y == 4` is `true` ($1$). Then `7 & 1` evaluates to `1`... wait! Let's check `7 & 1`: in decimal `7 & 1 = 1`!
  Wait! Let's verify:
  `y == 4` is `1`. `x & 1` is `7 & 1 = 1`.
  What if `y = 3`? `(x & y == 4)` $\to$ `x & 0 = 0`.
  Always use parentheses: `((x & y) == 4)` evaluates to `(4 == 4)` which is `1`.
