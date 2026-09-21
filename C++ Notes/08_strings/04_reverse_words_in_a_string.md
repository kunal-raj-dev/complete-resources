# Lecture 32: Reverse Words in a String (LeetCode 151)

> **One-Line Purpose:** Master two-pointer word reversal and in-place whitespace compaction to reverse sentence semantics in $O(N)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #32  
> **Video ID:** `RitppzIdMCo`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=RitppzIdMCo)  
> **Duration:** 14:42  
> **Status:** AUDITED  

---

## 🔵 Lecture Content & Implementation

```cpp
#include <string>
#include <algorithm>
#include <iostream>
using namespace std;

class SolutionReverseWords {
public:
    string reverseWords(string s) {
        // Step 1: Reverse entire string
        reverse(s.begin(), s.end());

        int n = s.size();
        int writeIdx = 0;

        // Step 2: Traverse words and reverse each word individually
        for (int start = 0; start < n; start++) {
            if (s[start] == ' ') continue;

            if (writeIdx != 0) s[writeIdx++] = ' '; // add single separating space

            int end = start;
            while (end < n && s[end] != ' ') end++;

            int wordStart = writeIdx;
            while (start < end) {
                s[writeIdx++] = s[start++];
            }

            reverse(s.begin() + wordStart, s.begin() + writeIdx);
        }

        s.resize(writeIdx); // Trim trailing whitespace
        return s;
    }
};
```
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(1)$ auxiliary (in-place modification).

## 🧠 Core Intuition — Why This Works
Reversing words in a string involves two separate operations: word order reversal and word character order. If you reverse the *entire string* first, the words are now in the correct order (last word is first), but each word's characters are backwards (`"blue sky" -> "yks eulb"`). The second step is to iterate through this new string, isolate each word, and reverse it back to normal (`"yks eulb" -> "sky blue"`). The `writeIdx` pointer ensures we compress any multiple spaces into a single space in-place without needing extra arrays.

## 🎯 Pattern Recognition — When to Use This
- **Trigger cues:** "Reverse the words in a string", "Modify string in-place with multiple spaces".
- **Keywords:** Double Reverse Technique, In-place compression, Write pointer (`writeIdx`).

## 📐 Algorithm Walk-Through
1. **Global Reverse:** Reverse the whole string `s`.
2. **Setup Pointers:** `writeIdx = 0` (where to place next valid char), `start = 0` (scan pointer).
3. **Scan and Compress:** Loop `start` from 0 to `n`:
   - If `s[start]` is a space, skip it.
   - If we've already written a word (`writeIdx != 0`), add exactly one space: `s[writeIdx++] = ' '`.
4. **Isolate and Shift Word:** Let `end = start`. While `s[end]` is not a space, shift characters to `writeIdx` (`s[writeIdx++] = s[end++]`).
5. **Local Reverse:** Reverse the newly placed word from its start index to `writeIdx`.
6. **Trim:** Resize string to `writeIdx` to remove trailing junk.

## 🔍 Dry Run Trace
`s = "  hello world  "`
1. Global Reverse: `s = "  dlrow olleh  "`
2. `start` skips spaces until index 2 (`d`). `writeIdx = 0`.
3. Shift word `"dlrow"`: `s[0..4] = "dlrow"`. `writeIdx = 5`.
4. Local reverse `s[0..4]`: `"world"`. Array is now `"world olleh  "`.
5. `start` skips space at index 7, lands at 8 (`o`). `writeIdx = 5`.
6. Add single space: `s[5] = ' '`. `writeIdx = 6`.
7. Shift word `"olleh"`: `s[6..10] = "olleh"`. `writeIdx = 11`.
8. Local reverse `s[6..10]`: `"hello"`. Array is `"world hello  "`.
9. `resize(11)` drops trailing spaces. Result: `"world hello"`.

## ⚠️ Common Interview Mistakes
- **Using extra space:** Splitting by spaces into an array of strings is easy but takes $O(N)$ extra space, which often violates interview constraints for C/C++ developers.
- **Handling multiple spaces:** Forgetting to compress multiple spaces into a single space.
- **Trailing/Leading spaces:** Failing to remove edge spaces after reversal.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: Can this be solved using a Stack?
**Answer:** Yes, you can push words onto a stack and pop them to reverse the order, but this takes $O(N)$ extra space. The double-reverse technique strictly takes $O(1)$ auxiliary space.

### Q2: Why do we reverse the whole string first instead of finding words and swapping them?
**Answer:** Swapping variable-length words directly is extremely complex because it requires shifting all characters between them. By reversing the entire string, we move the characters to their approximate final locations in one pass, requiring only local reversals afterward.

### Q3: What if the string is immutable, like in Java or Python?
**Answer:** In Java or Python, strings are immutable, so an $O(1)$ space solution is impossible. You *must* allocate a `StringBuilder` or character array of size $O(N)$. The double-reverse logic can still be applied to the char array.

## 🏆 Related Problems (Leetcode)
- **LeetCode 186:** Reverse Words in a String II (Character array given, $O(1)$ space guaranteed)
- **LeetCode 344:** Reverse String (The basic building block)
- **LeetCode 557:** Reverse Words in a String III (Preserve word order, reverse characters)

## 🔗 Cross-Topic Connections
- **Two Pointers:** The exact same `writeIdx` and `readIdx` logic is used to remove duplicates from sorted arrays (LeetCode 26).

## ⚡ 2-Minute Revision Flash Card
- **Problem:** Reverse word order, collapse spaces.
- **Method:** Double Reverse.
- **Step 1:** Reverse entire string.
- **Step 2:** Use `writeIdx` to skip spaces, append 1 space, shift word characters left.
- **Step 3:** Reverse the specific word just shifted.
- **Step 4:** `s.resize(writeIdx)`.
