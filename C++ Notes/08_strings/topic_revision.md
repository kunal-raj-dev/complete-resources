# ⚡ Topic 08 Revision: Strings & Sliding Window Manipulation

> **High-Density Review:** String representations, sliding window frequencies, two-pointer palindrome techniques, and in-place reversals.

---

## 1. Core String Patterns

| Problem | Optimal Approach | Time Complexity | Auxiliary Space | Key Mechanics |
|---|---|---|---|---|
| **Valid Palindrome** | Two Pointers | $O(N)$ | $O(1)$ | Skip non-alphanumeric `isalnum()` |
| **Permutation in String** | Fixed Sliding Window | $O(N)$ | $O(1)$ (26 ints) | Compare frequency arrays of size 26 |
| **Reverse Words in String**| In-place 3-pass reverse | $O(N)$ | $O(1)$ | Reverse whole string $\to$ reverse each word $\to$ trim spaces |
| **String Compression** | Read/Write Pointers | $O(N)$ | $O(1)$ | Write count digits only if `count > 1` |

---

## 2. Sliding Window Frequency Matching Blueprint
```cpp
vector<int> freq1(26, 0), freq2(26, 0);
for (char c : s1) freq1[c - 'a']++;

int k = s1.length();
for (int i = 0; i < s2.length(); ++i) {
    freq2[s2[i] - 'a']++;
    if (i >= k) freq2[s2[i - k] - 'a']--; // Maintain window of size k

    if (freq1 == freq2) return true; // Found anagram match!
}
```
