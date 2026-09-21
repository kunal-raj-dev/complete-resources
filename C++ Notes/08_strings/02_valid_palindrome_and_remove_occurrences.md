# Lecture 30: Valid Palindrome (LeetCode 125) & Remove All Occurrences (LeetCode 1910)

> **One-Line Purpose:** Master two-pointer inward scans with alphanumeric filtering and iterative substring eradication.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #30  
> **Video ID:** `dSRFgEs3a6A`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=dSRFgEs3a6A)  
> **Duration:** 24:02  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

- Solve **Valid Palindrome** in $O(N)$ time and $O(1)$ space using two pointers.
- Use standard C++ utility functions `isalnum()` and `tolower()`.
- Solve **Remove All Occurrences of a Substring** using `std::string::find` and `erase`.

---

## 🔵 Lecture Content

### 1. Valid Palindrome (LeetCode 125)

```cpp
#include <string>
#include <cctype>
#include <iostream>
using namespace std;

class SolutionPalindrome {
public:
    bool isPalindrome(string s) {
        int left = 0, right = s.size() - 1;

        while (left < right) {
            while (left < right && !isalnum(s[left])) left++;
            while (left < right && !isalnum(s[right])) right--;

            if (tolower(s[left]) != tolower(s[right])) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }
};
```
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(1)$ in-place without copying into a secondary string.

---

### 2. Remove All Occurrences of Substring (LeetCode 1910)

```cpp
class SolutionRemoveOccurrences {
public:
    string removeOccurrences(string s, string part) {
        while (s.length() > 0 && s.find(part) != string::npos) {
            s.erase(s.find(part), part.length());
        }
        return s;
    }
};
```
- **Time Complexity:** $O(N^2 / M)$ where $N = \text{length}(s)$ and $M = \text{length}(part)$.
- Can also be solved in $O(N)$ time using a stack or string builder.

## 🧠 Core Intuition — Why This Works
**Valid Palindrome:** A palindrome mirrors itself around its center. By placing one pointer at the start and one at the end, we can simultaneously check outer characters and shrink inwards. Skipping non-alphanumeric characters ensures we only compare the core text.
**Remove Occurrences:** Instead of trying to shift elements in an array manually, utilizing `std::string::find` and `std::string::erase` allows us to locate a substring and snip it out. If a new occurrence forms from the pieces clicking together (e.g., removing `b` from `aba`), the next iteration of `find` will catch it.

## 🎯 Pattern Recognition — When to Use This
- **Valid Palindrome:** "Ignore casing and punctuation", "Check symmetry", "Compare extremes". -> **Two Pointers (inwards)**.
- **Remove Occurrences:** "Repeatedly remove substring", "Collapsing string". -> **String find/erase (or Stack for $O(N)$)**.

## 📐 Algorithm Walk-Through
**Valid Palindrome:**
1. Setup `left = 0`, `right = s.length() - 1`.
2. While `left < right`:
   - Increment `left` if `s[left]` is not alphanumeric.
   - Decrement `right` if `s[right]` is not alphanumeric.
   - If `tolower(s[left]) != tolower(s[right])`, return `false`.
   - `left++`, `right--`.
3. If loop finishes, it's a palindrome.

## 🔍 Dry Run Trace
`s = "A man, a plan, a canal: Panama"`
- `left` stops at `'A'`, `right` stops at `'a'`. Both `tolower()` -> `'a'`. Match! `left++`, `right--`.
- `left` stops at `'m'`, `right` skips spaces and stops at `'m'`. Match!
- Middle matches...
- Eventually `left >= right`, returning `true`.

## ⚠️ Common Interview Mistakes
- **Valid Palindrome:** Forgetting to do `left < right` *inside* the inner `while` loops that skip non-alphanumeric chars. If a string has only punctuation `",,,,"`, `left` will run out of bounds and crash.
- **Remove Occurrences:** Doing `s.erase(part)` instead of `s.erase(index, length)`. The `erase()` function requires a start index and length.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: How does `isalnum()` work under the hood?
**Answer:** It usually checks if the character's ASCII value falls within the ranges for 'A'-'Z', 'a'-'z', or '0'-'9'. It's $O(1)$.

### Q2: Is recursion a good approach for Valid Palindrome?
**Answer:** No. While mathematically elegant, recursion requires $O(N)$ space on the call stack. The iterative two-pointer method takes $O(1)$ space.

### Q3: How can we solve Remove All Occurrences in $O(N)$ time?
**Answer:** By using a Stack (or string as a stack). We push characters one by one. After every push, if the top of the stack matches the last character of `part`, we check if the top `M` elements form `part`. If they do, we pop them all. This guarantees each character is processed in amortized $O(1)$ time.

### Q4: Why is `string::find` inside a loop considered $O(N^2)$?
**Answer:** In the worst case, `find` uses naive string matching taking $O(N \times M)$ time. Furthermore, `erase` shifts all trailing characters left, taking $O(N)$ time per deletion. Repeating this up to $N/M$ times yields $O(N^2 / M)$ complexity.

## 🏆 Related Problems (Leetcode)
- **LeetCode 680:** Valid Palindrome II (Can delete at most one character)
- **LeetCode 1047:** Remove All Adjacent Duplicates In String (Similar stack-based removal)
- **LeetCode 1209:** Remove All Adjacent Duplicates in String II (K-length duplicates)

## 🔗 Cross-Topic Connections
- **Stack:** Remove Occurrences is fundamentally a Stack problem masquerading as a string problem for optimal $O(N)$ time.
- **Two Pointers:** Valid Palindrome is the canonical introductory two-pointer problem.

## ⚡ 2-Minute Revision Flash Card
- **Valid Palindrome:** Two pointers (`left`, `right`). Use `while (left < right)`. Skip non-alnum using `!isalnum()`. Compare using `tolower()`.
- **Remove Occurrences:** `while(s.length() > 0 && s.find(part) != string::npos)`. Use `s.erase(startIndex, length)`.
- **Trap:** Forgetting bounds check `left < right` in the skipping loops.
