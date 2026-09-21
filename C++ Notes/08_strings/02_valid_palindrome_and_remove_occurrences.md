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
