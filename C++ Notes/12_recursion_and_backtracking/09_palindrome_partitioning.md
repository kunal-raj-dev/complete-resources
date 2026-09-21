# Lecture 50: Palindrome Partitioning: Substring Backtracking (LeetCode 131)

> **One-Line Purpose:** Master multi-cut string partitioning using recursive prefix validation, generating all possible decompositions of a string into palindromic substrings in $O(N \cdot 2^N)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #50  
> **Video ID:** `aZ0B1eWkSVU`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=aZ0B1eWkSVU)  
> **Duration:** 20:44  
> **Transcript:** `.transcripts/12_recursion_and_backtracking/050_Palindrome_Partitioning_Problem___Recursion___Backtracking.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The definition of Palindrome Partitioning: splitting string $s$ such that every contiguous partition substring reads identically forward and backward.
- How to model string partitioning as choosing cut positions $i$ between indices.
- The prefix validation backtracking template: if prefix $s[\text{start} \dots i]$ is a palindrome, recurse on suffix $s[i+1 \dots n-1]$.
- Two-pointer palindrome checking in $O(\text{length})$ time.

---

## 🔵 Lecture Context

Palindrome Partitioning is a Tier-1 interview problem that tests string slicing, symmetric checking, and multi-branch backtracking. It serves as the bridge between backtracking and Dynamic Programming (LeetCode 132: Palindrome Partitioning II).

---

## 1. Problem Statement

Given a string `s`, partition `s` such that every substring of the partition is a **palindrome**. Return all possible palindrome partitionings of `s`.

```
Input: s = "aab"
Output: [["a", "a", "b"], ["aa", "b"]]
```
Notice that `["a", "ab"]` is invalid because `"ab"` is not a palindrome.

---

## 2. Algorithmic Logic

At each step with starting index `start`:
1. Loop over possible partition cut points $i$ from `start` to $n - 1$.
2. Squeeze candidate prefix: substring $s[\text{start} \dots i]$.
3. **Is $s[\text{start} \dots i]$ a palindrome?**
   - **Yes:** Add substring to `path`, recurse on `i + 1`, and then backtrack (`path.pop_back()`).
   - **No:** Skip this cut point because an invalid prefix cannot form a valid partition!

---

## 3. Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <string>
using namespace std;

class Solution {
public:
    bool isPalindrome(const string& s, int l, int r) {
        while (l < r) {
            if (s[l++] != s[r--]) return false;
        }
        return true;
    }

    void dfs(const string& s, int start, vector<string>& path, vector<vector<string>>& result) {
        // Base Case: Consumed the entire string
        if (start == s.length()) {
            result.push_back(path);
            return;
        }

        for (int i = start; i < s.length(); i++) {
            // Check if current slice is a palindrome
            if (isPalindrome(s, start, i)) {
                // Choose
                path.push_back(s.substr(start, i - start + 1));

                // Explore remaining suffix
                dfs(s, i + 1, path, result);

                // Backtrack
                path.pop_back();
            }
        }
    }

    vector<vector<string>> partition(string s) {
        vector<vector<string>> result;
        vector<string> path;
        dfs(s, 0, path, result);
        return result;
    }
};

int main() {
    Solution solver;
    string s = "aab";
    vector<vector<string>> partitions = solver.partition(s);

    cout << "Palindrome partitions of " << s << ":\n";
    for (const auto& part : partitions) {
        cout << "[ ";
        for (const string& str : part) cout << "\"" << str << "\" ";
        cout << "]\n";
    }
    return 0;
}
```

---

## 🔍 Detailed Trace: `s = "aab"`

```
dfs(start = 0):
- i = 0: "a" is palindrome! path = ["a"]
  dfs(start = 1):
  - i = 1: "a" is palindrome! path = ["a", "a"]
    dfs(start = 2):
    - i = 2: "b" is palindrome! path = ["a", "a", "b"]
      dfs(start = 3): Base case reached -> Record [["a", "a", "b"]]
  - i = 2: "ab" is NOT palindrome -> Skip!

- i = 1: "aa" is palindrome! path = ["aa"]
  dfs(start = 2):
  - i = 2: "b" is palindrome! path = ["aa", "b"]
    dfs(start = 3): Base case reached -> Record [["aa", "b"]]

- i = 2: "aab" is NOT palindrome -> Skip!
```

---

## 🧠 Mental Model: Cutting a Ribbon

Think of string $s$ as a ribbon. At each step, you snip off a piece from the front. If the piece is symmetrical (a palindrome), you save it and look at the remaining ribbon. If the piece is asymmetrical, you throw that snip away and try cutting a longer piece.

---

## ⚠️ Common Mistakes

1. **Incorrect `substr()` parameters:** In C++, `s.substr(pos, count)`. The second argument is the **length** of the substring (`i - start + 1`), not the ending index! Passing `i` produces corrupted slices.
2. **Missing Palindrome Memoization:** For strings of length $\ge 16$, precomputing palindrome truth values in a 2D boolean DP table `dp[l][r]` speeds up `isPalindrome()` queries from $O(N)$ to $O(1)$.

---

## 🖥️ System-Specific Notes

- A string of length $N$ has $N - 1$ potential cut slots. There are $2^{N-1}$ total possible partitions. For $N = 16$, $2^{15} = 32,768$ partitions, which runs well within $50\text{ ms}$.

---

## 🟡 Additional Essential Context

In LeetCode 132 (Palindrome Partitioning II), the goal is to find the **minimum cuts** needed for a palindromic partition. While LeetCode 131 uses backtracking to output all paths, LeetCode 132 requires $O(N^2)$ Dynamic Programming to compute the optimal cut count.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Why is the time complexity $O(N \cdot 2^N)$?  
**A:** In the worst case (e.g. `s = "aaaa"`), every substring is a palindrome. There are $2^{N-1}$ possible partitions, and each partition takes $O(N)$ time to copy substrings and verify palindromes.

---

### 🔥 Interview Questions

#### Q1: How do you optimize `isPalindrome()` checks using Dynamic Programming?
- **Short Answer:** Precompute a 2D table `isPal[i][j]` where `isPal[i][j] = (s[i] == s[j]) && (j - i <= 2 || isPal[i+1][j-1])`.
- **Detailed Explanation:** This reduces the palindrome check from an $O(N)$ two-pointer scan to an $O(1)$ table lookup during backtracking.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
// s = "efe"
// Output: [["e", "f", "e"], ["efe"]]
```

---

## Edge Cases

1. **Single Character String:** `s = "a"` $\to$ Returns `[["a"]]`.
2. **String with No Palindromes $>1$:** `s = "abc"` $\to$ Returns `[["a", "b", "c"]]`.

---

## Complexity Analysis

- **Time Complexity:** $O(N \cdot 2^N)$ (Upper bounded by all possible cuts).
- **Auxiliary Space Complexity:** $O(N)$ (Maximum recursion depth is $N$).

---

## Key Takeaways

1. **Prefix Cut Model:** Check prefix validity before recursing into suffix.
2. **Substr Length:** Always use `i - start + 1`.
3. **DP Precomputation:** Accelerates palindrome checks in tight runtime constraints.

---

## ⚡ 2-Minute Revision

- Cut loop: `for (int i = start; i < s.length(); i++)`.
- Check: `if (isPalindrome(s, start, i)) { path.push_back(); dfs(i + 1); path.pop_back(); }`.
