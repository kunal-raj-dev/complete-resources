# Lecture 82: First Unique Character in String & Stream (LeetCode 387)

> **One-Line Purpose:** Locate the first non-repeating character in static strings using frequency arrays ($O(N)$), and in continuous data streams using a FIFO queue tracking arrival sequence in $O(1)$ amortized per character.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #82  
> **Video ID:** `sqyCBvEQN9c`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=sqyCBvEQN9c)  
> **Duration:** 13:23  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Understanding static string lookup vs real-time continuous character streams.
- The Queue invariant for streaming: The front of the queue is always the first non-repeating character seen so far.
- Discarding duplicates via while-loop queue eviction: `while (!q.empty() && freq[q.front()] > 1) q.pop();`.

---

## 🔵 The Queue Stream Architecture
```
Stream: "a", "a", "b", "c", "b"
Input 'a': freq['a']=1, q=['a']            -> First non-repeating: 'a'
Input 'a': freq['a']=2, q=['a','a'] -> pop -> First non-repeating: '#' (None)
Input 'b': freq['b']=1, q=['b']            -> First non-repeating: 'b'
Input 'c': freq['c']=1, q=['b','c']        -> First non-repeating: 'b'
Input 'b': freq['b']=2, q=['b','c'] -> pop -> First non-repeating: 'c'
```

---

## 💻 Complete C++ Implementation: Both Static & Streaming

```cpp
#include <string>
#include <vector>
#include <queue>
#include <iostream>

using namespace std;

class SolutionFirstUnique {
public:
    // 1. Static String: LeetCode 387 - O(N) Time, O(1) Space
    int firstUniqChar(string s) {
        vector<int> freq(26, 0);
        for (char ch : s) freq[ch - 'a']++;

        for (int i = 0; i < (int)s.length(); ++i) {
            if (freq[s[i] - 'a'] == 1) return i;
        }
        return -1;
    }

    // 2. Continuous Stream Processing via Queue - O(1) Amortized Time
    static string firstNonRepeatingInStream(string stream) {
        vector<int> freq(26, 0);
        queue<char> q;
        string result = "";

        for (char ch : stream) {
            freq[ch - 'a']++;
            q.push(ch);

            // Evict repeated characters from queue front
            while (!q.empty() && freq[q.front() - 'a'] > 1) {
                q.pop();
            }

            if (q.empty()) {
                result += '#';
            } else {
                result += q.front();
            }
        }
        return result;
    }
};

int main() {
    SolutionFirstUnique solver;
    cout << "Index in 'loveleetcode': " << solver.firstUniqChar("loveleetcode") << endl; // Output: 2 ('v')
    cout << "Stream 'aabc': " << SolutionFirstUnique::firstNonRepeatingInStream("aabc") << endl; // Output: "a#bb"
    return 0;
}
```

---

## ⏱️ Complexity Analysis
- **Static Array:** Time $O(N)$, Auxiliary Space $O(1)$ (26 integers).
- **Stream Queue:** Time $O(N)$ total (each character is pushed and popped at most once, amortized $O(1)$ per stream item), Space $O(26) = O(1)$.

## 🧠 Core Intuition — Why This Works
For a static string, a two-pass algorithm is simple: Pass 1 to count frequencies, Pass 2 to find the first character with frequency 1.
For a *continuous stream*, you cannot do a two-pass algorithm because the data is infinite and arriving in real-time. We need to remember the order of arrival. A **Queue (FIFO)** perfectly models "order of arrival". As characters arrive, we push them into the queue. When asked for the "first unique", we just look at the `front()` of the queue. If the `front()` character has appeared more than once (tracked via a frequency array), it is no longer unique, so we `pop()` it and check the next one in line.

## 🎯 Pattern Recognition — When to Use This
- **"First non-repeating character in a stream"**: Direct trigger for the Queue + Frequency Map pattern. 
- **"Real-time processing with historical order"**: Any problem requiring you to find the "oldest valid" item in a stream implies a Queue where you lazily pop invalid items from the front.

## 🔍 Dry Run Trace
**Example Stream:** `"a", "a", "b", "c"`
`freq[26] = {0}`, `q = []`

- **Read 'a'**: `freq['a'] = 1`. `q.push('a')`. 
  - `q.front() = 'a'`. `freq['a'] == 1`. Not > 1, so no pop. 
  - **Result: 'a'**
- **Read 'a'**: `freq['a'] = 2`. `q.push('a')`.
  - `q.front() = 'a'`. `freq['a'] == 2`. POP 'a'. 
  - `q.front() = 'a'`. `freq['a'] == 2`. POP 'a'.
  - `q` is now empty.
  - **Result: '#' (None)**
- **Read 'b'**: `freq['b'] = 1`. `q.push('b')`.
  - `q.front() = 'b'`. `freq['b'] == 1`. No pop.
  - **Result: 'b'**
- **Read 'c'**: `freq['c'] = 1`. `q.push('c')`.
  - `q.front() = 'b'`. `freq['b'] == 1`. No pop.
  - **Result: 'b'**

## ⚠️ Common Interview Mistakes
1. **Using nested loops for the stream problem:** Checking all previous characters in the stream takes $O(N^2)$ time and is an instant rejection for stream problems.
2. **Forgetting to push to the queue:** Even if a character is already repeated (`freq > 1`), you might still push it to the queue (though it's optimal not to). But if it's the first time, you MUST push it.
3. **Eager removal vs Lazy removal:** A queue doesn't allow removing elements from the middle. If a character in the middle of the queue becomes repeated, we do NOTHING. We only pop elements when they reach the `front()` of the queue. This is called **Lazy Deletion**.

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: What is the maximum size the queue can reach?
Since the English alphabet has 26 lowercase letters, the queue will contain at most 26 unique characters at any given time if we don't push known duplicates. If we push blindly, the queue could grow to size $N$, which is bad. In our optimal implementation, the queue size is effectively bounded by the character set size $O(K)$.

### Q2: Why is the time complexity $O(1)$ amortized per character?
While there is a `while` loop that pops elements, each character is pushed into the queue exactly once and popped exactly once. Over a stream of length $N$, there are at most $N$ pushes and $N$ pops. Total time for queue operations is $O(N)$, which averages to $O(1)$ per character.

### Q3: What if the character set is unicode (millions of characters)?
Instead of a fixed size array `vector<int> freq(26, 0)`, you must use a Hash Map (`unordered_map<char, int>`). The time complexity remains $O(1)$ on average per character, but the space complexity scales with the number of unique characters encountered.

### Q4: Can we solve this using a Doubly Linked List?
Yes! Maintain a Doubly Linked List of unique characters and a Hash Map storing pointers to the DLL nodes. When a character arrives for the first time, append to the DLL. If it arrives again, use the Hash Map pointer to remove it from the middle of the DLL in $O(1)$ time. This is "Eager Deletion" and is exactly how an LRU Cache is implemented.

## 🏆 Related Problems (Leetcode)
- **[387. First Unique Character in a String](https://leetcode.com/problems/first-unique-character-in-a-string/)**: The static string version.
- **[146. LRU Cache](https://leetcode.com/problems/lru-cache/)**: Similar DLL + HashMap structure if eager deletion is required.
- **[346. Moving Average from Data Stream](https://leetcode.com/problems/moving-average-from-data-stream/)**: Another classic queue-based stream problem.

## 🔗 Cross-Topic Connections
- **Sliding Window / Two Pointers**: Can be seen as a dynamically expanding window where the left pointer (queue front) moves forward whenever it hits an invalid (repeated) state.
- **LRU Cache**: The DLL approach to eager deletion links directly to caching algorithms.

## ⚡ 2-Minute Revision Flash Card
- **Static String:** 2 passes. Pass 1: count freq. Pass 2: find first char with freq == 1.
- **Stream Approach:** Use a Queue + Freq Array.
- **Invariant:** `front()` of queue must be the first unique character.
- **Lazy Deletion:** `while(!q.empty() && freq[q.front()] > 1) q.pop();`
- **Time/Space:** $O(1)$ amortized time per character, $O(1)$ space (26 letters).
