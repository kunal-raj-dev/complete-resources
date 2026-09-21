# Lecture 33: String Compression (LeetCode 443)

> **One-Line Purpose:** Implement in-place Run-Length Encoding (RLE) using two pointers to compress repeating character sequences into character-count pairs.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #33  
> **Video ID:** `cAB15h6-sWA`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=cAB15h6-sWA)  
> **Duration:** 19:29  
> **Status:** AUDITED  

---

## 🔵 Lecture Content & Implementation

```cpp
#include <vector>
#include <string>
#include <iostream>
using namespace std;

class SolutionStringCompression {
public:
    int compress(vector<char>& chars) {
        int n = chars.size();
        int writeIdx = 0;
        int i = 0;

        while (i < n) {
            char currChar = chars[i];
            int count = 0;

            // Count contiguous occurrences of currChar
            while (i < n && chars[i] == currChar) {
                count++;
                i++;
            }

            // Write character
            chars[writeIdx++] = currChar;

            // If count > 1, write count digits
            if (count > 1) {
                string countStr = to_string(count);
                for (char c : countStr) {
                    chars[writeIdx++] = c;
                }
            }
        }

        return writeIdx; // New length of compressed array
    }
};
```
- **Time Complexity:** $O(N)$ — Every character is read at most twice and written at most twice.
- **Space Complexity:** $O(1)$ auxiliary memory.

## 🧠 Core Intuition — Why This Works
String compression groups contiguous identical characters into a single character followed by its count. Since the compressed version is guaranteed to be shorter than or equal to the original string (e.g., `["a","a"] -> ["a","2"]`), we can safely overwrite the input array from left to right using a `writeIdx` pointer. A read pointer `i` scans forward to count occurrences. By the time `writeIdx` writes to a spot, `i` has already processed it, ensuring no data loss.

## 🎯 Pattern Recognition — When to Use This
- **Trigger cues:** "Compress string", "Run-Length Encoding (RLE)", "In-place modification of character arrays".
- **Keywords:** `writeIdx`, group counting, `to_string()`.

## 📐 Algorithm Walk-Through
1. Setup `writeIdx = 0`, `i = 0`.
2. While `i < n`:
   - Store `currChar = chars[i]`.
   - Setup `count = 0`.
   - While `chars[i] == currChar`, increment `count` and `i`.
   - Write `currChar` to `chars[writeIdx++]`.
   - If `count > 1`, convert `count` to string. Write each digit to `chars[writeIdx++]`.
3. Return `writeIdx` as the new length.

## 🔍 Dry Run Trace
`chars = ['a', 'a', 'b', 'b', 'c', 'c', 'c']`
1. `i = 0, currChar = 'a'`. Count loop: `i` reaches 2, `count = 2`.
2. Write: `chars[0] = 'a'`. `writeIdx = 1`.
3. Count > 1: String "2". `chars[1] = '2'`. `writeIdx = 2`.
4. `i = 2, currChar = 'b'`. Count loop: `i` reaches 4, `count = 2`.
5. Write: `chars[2] = 'b'`. `writeIdx = 3`.
6. Count > 1: String "2". `chars[3] = '2'`. `writeIdx = 4`.
7. `i = 4, currChar = 'c'`. Count loop: `i` reaches 7, `count = 3`.
8. Write: `chars[4] = 'c'`. `writeIdx = 5`.
9. Count > 1: String "3". `chars[5] = '3'`. `writeIdx = 6`.
10. Return 6. Array is `['a', '2', 'b', '2', 'c', '3']`.

## ⚠️ Common Interview Mistakes
- **Counts ≥ 10:** Forgetting that `count = 12` must be written as two separate characters `'1'` and `'2'`.
- **Count = 1:** Forgetting the edge case where the character appears only once (do not write "1").
- **Writing out of bounds:** Not a risk here since compressed size $\le$ original size, but candidates often doubt this and try to allocate extra arrays.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: Is it always guaranteed that the compressed array fits in the original array?
**Answer:** Yes. The worst-case is no repeating characters (e.g., `["a", "b", "c"]`). The algorithm dictates that we don't write counts for $1$, so the output is exactly `["a", "b", "c"]`, which takes the same space. Any count $\ge 2$ takes $1$ char for the letter and $\le K$ chars for digits. For instance, 10 'a's take 10 indices, but compress to `a`,`1`,`0` (3 indices).

### Q2: Can this algorithm handle decompression?
**Answer:** Decompression is inherently not $O(1)$ space unless the array has massive trailing whitespace, because `"a10"` expands to 10 characters, requiring more space than the input. 

### Q3: How do you extract digits from `count` without using `to_string()`?
**Answer:** You can repeatedly modulo and divide by 10 (`count % 10`, `count /= 10`) to extract digits from right to left, push them to a small temporary string/stack, and pop them to write left to right. Since count is at most the array size, this small stack is $O(1)$ space.

## 🏆 Related Problems (Leetcode)
- **LeetCode 38:** Count and Say (Similar grouping logic)
- **LeetCode 283:** Move Zeroes (Uses same `writeIdx` overwrite concept)

## 🔗 Cross-Topic Connections
- **Two Pointers:** `read/write` pointer patterns are universal for in-place array modifications (removing duplicates, shifting zeroes).

## ⚡ 2-Minute Revision Flash Card
- **Problem:** In-place string compression (RLE).
- **Technique:** Two pointers (`writeIdx` and `i`).
- **Inner Loop:** `while (i < n && chars[i] == currChar)`.
- **Digit Handling:** If `count > 1`, convert to string and iterate digits.
- **Safety:** Always guaranteed to fit in original array because length of `"X" + to_string(count)` is $\le$ `count`.
