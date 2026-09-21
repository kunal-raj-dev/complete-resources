# Lecture 69: Valid Parentheses (LeetCode 20)

> **One-Line Purpose:** Validate bracket nesting and balance using stack LIFO matching in linear $O(N)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #69  
> **Video ID:** `NlHupEeDXzY`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=NlHupEeDXzY)  
> **Duration:** 16:25  
> **Status:** AUDITED  

---

## 🔵 Lecture Content & Implementation

```cpp
#include <string>
#include <stack>
#include <iostream>
using namespace std;

class SolutionValidParentheses {
public:
    bool isValid(string s) {
        stack<char> st;

        for (char ch : s) {
            if (ch == '(' || ch == '{' || ch == '[') {
                st.push(ch);
            } else {
                if (st.empty()) return false; // Closing bracket with no opening counterpart

                char topChar = st.top();
                if ((ch == ')' && topChar == '(') ||
                    (ch == '}' && topChar == '{') ||
                    (ch == ']' && topChar == '[')) {
                    st.pop();
                } else {
                    return false; // Mismatched bracket types
                }
            }
        }

        return st.empty(); // True only if all opened brackets were closed
    }
};
```
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(N)$ worst-case stack space.
