# Lecture 31: Permutation in String: Fixed-Length Sliding Window (LeetCode 567)

> **One-Line Purpose:** Master frequency-matching over a fixed-size sliding window to detect anagrams in linear $O(N)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #31  
> **Video ID:** `VXewy91P0S4`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=VXewy91P0S4)  
> **Duration:** 21:41  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

- Understand why a permutation of $s_1$ inside $s_2$ implies a contiguous substring of length $|s_1|$ with identical character frequency distribution.
- Implement the **Fixed Sliding Window** technique with 26-element integer arrays.
- Achieve $O(|s_2|)$ time complexity with $O(1)$ constant space (26 characters).

---

## 🔵 Lecture Content & Implementation

```cpp
#include <string>
#include <vector>
#include <iostream>
using namespace std;

class SolutionPermutation {
public:
    bool checkInclusion(string s1, string s2) {
        int n1 = s1.length();
        int n2 = s2.length();
        if (n1 > n2) return false;

        vector<int> freq1(26, 0);
        vector<int> freq2(26, 0);

        // Populate initial window of size n1
        for (int i = 0; i < n1; i++) {
            freq1[s1[i] - 'a']++;
            freq2[s2[i] - 'a']++;
        }

        if (freq1 == freq2) return true;

        // Slide the window across s2
        for (int i = n1; i < n2; i++) {
            freq2[s2[i] - 'a']++;          // Add newly included character
            freq2[s2[i - n1] - 'a']--;     // Remove character falling out of window

            if (freq1 == freq2) return true;
        }

        return false;
    }
};
```
- **Time Complexity:** $O(26 \times |s_2|) = O(|s_2|)$ time.
- **Space Complexity:** $O(1)$ space (fixed 26-size frequency arrays).

## 🧠 Core Intuition — Why This Works
A permutation of a string is just the same characters rearranged. This means the *frequency* of each character must be identical. If we need to find if a permutation of $s_1$ exists in $s_2$, we just need to find a substring in $s_2$ of length exactly $|s_1|$ that has the exact same character frequencies as $s_1$.
Instead of recalculating the frequency of every window of length $|s_1|$ from scratch ($O(|s_1| \times |s_2|)$), we use a **Sliding Window**. As the window moves right by one step, we simply add the new character entering the window to our frequency count, and remove the old character that fell out of the left side. Then we compare it to $s_1$'s frequency array.

## 🎯 Pattern Recognition — When to Use This
- **Trigger cues:** "Permutation in a string", "Anagrams in a string", "Contiguous substring with same characters".
- **Keywords:** Sliding Window (fixed size), Frequency Map / Array, $O(N)$ time.

## 📐 Algorithm Walk-Through
1. Check edge case: If $|s_1| > |s_2|$, return `false`.
2. Initialize two frequency arrays `freq1` and `freq2` of size 26 with zeros.
3. Traverse the first $|s_1|$ characters of both strings to populate `freq1` and the initial window of `freq2`.
4. If `freq1 == freq2`, return `true`.
5. Slide the window across $s_2$ from index $|s_1|$ to $|s_2| - 1$:
   - Increment the count of the new character entering the window: `freq2[s2[i] - 'a']++`.
   - Decrement the count of the old character leaving the window: `freq2[s2[i - |s_1|] - 'a']--`.
   - Compare `freq1` and `freq2`. If they match, return `true`.
6. Return `false` if the loop finishes without a match.

## 🔍 Dry Run Trace
`s1 = "ab", s2 = "eidbaooo"` (Lengths: $n_1=2, n_2=8$)
- Initial Window (i=0 to 1): `freq1` has `a:1, b:1`. `freq2` has `e:1, i:1`.
- Match? `freq1 != freq2`.
- Slide 1 (i=2): Add `d` (index 2), Remove `e` (index 0). `freq2` has `i:1, d:1`. Match? No.
- Slide 2 (i=3): Add `b` (index 3), Remove `i` (index 1). `freq2` has `d:1, b:1`. Match? No.
- Slide 3 (i=4): Add `a` (index 4), Remove `d` (index 2). `freq2` has `b:1, a:1`. Match? Yes! `freq1 == freq2`. Return `true`.

## ⚠️ Common Interview Mistakes
- **Recomputing the frequency map for every window:** This makes the time complexity $O(|s_1| \times |s_2|)$ which will TLE (Time Limit Exceeded) on LeetCode.
- **Incorrect removal index:** The character leaving the window is at index `i - n1`, not `i - n1 - 1`.
- **Using Hash Maps instead of arrays:** While `unordered_map` works, it adds significant overhead. For lowercase English letters, a size-26 `vector` or array is much faster and uses strictly $O(1)$ space.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: Comparing two arrays of size 26 takes $O(26)$. Can we optimize this comparison to $O(1)$?
**Answer:** Yes. Instead of comparing the full arrays, we can maintain a `matches` counter (from 0 to 26). When we update a character frequency, we check if that specific character's count now matches `freq1`. If it matches, `matches++`. If it used to match but now doesn't, `matches--`. If `matches == 26`, we return `true`. This reduces the window slide check from $O(26)$ to true $O(1)$.

### Q2: What if the string contains Unicode characters instead of just lowercase English letters?
**Answer:** We would have to use a Hash Map (`std::unordered_map`) to store frequencies because an array would be too large to allocate for all possible Unicode characters. The space complexity would become $O(U)$ where $U$ is the number of unique characters in the window.

### Q3: How is this different from a variable-size sliding window?
**Answer:** In variable-size sliding windows (e.g., "Longest Substring Without Repeating Characters"), the `left` and `right` pointers move independently based on a condition. Here, the window size is strictly fixed to $|s_1|$, so `left` and `right` move together in lockstep.

## 🏆 Related Problems (Leetcode)
- **LeetCode 438:** Find All Anagrams in a String (Exact same logic, just return start indices instead of boolean)
- **LeetCode 76:** Minimum Window Substring (Variable-size sliding window, harder version)
- **LeetCode 3:** Longest Substring Without Repeating Characters (Variable-size window)

## 🔗 Cross-Topic Connections
- **Hashing/Frequency Maps:** Fundamental use of arrays as ultra-fast hash maps for fixed character sets.
- **Two Pointers:** The sliding window is essentially a two-pointer technique where the distance between pointers is constant.

## ⚡ 2-Minute Revision Flash Card
- **Problem:** Find if permutation (anagram) of $s_1$ exists in $s_2$.
- **Method:** Fixed-Size Sliding Window + Frequency Array.
- **Array Size:** 26 (for 'a'-'z').
- **Update Rule:** As window shifts right, add new char `s2[i]`, remove old char `s2[i - s1.length()]`.
- **Match Check:** If `freq1 == freq2` (which is $O(26)$), return `true`.
