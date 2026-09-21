# Lecture 81: Queue using Stacks & Stack using Queues (LeetCode 232 & 225)

> **One-Line Purpose:** Implement ADT adaptations: two-stack amortized $O(1)$ queue and single-queue cyclical rotation stack.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #81  
> **Video ID:** `sFvP5Ois0CE`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=sFvP5Ois0CE)  
> **Duration:** 15:47  
> **Status:** AUDITED  

---

## 🔵 Implement Queue using 2 Stacks (Amortized $O(1)$)

```cpp
#include <stack>
using namespace std;

class MyQueue {
private:
    stack<int> inStack;
    stack<int> outStack;

    void transferIfEmpty() {
        if (outStack.empty()) {
            while (!inStack.empty()) {
                outStack.push(inStack.top());
                inStack.pop();
            }
        }
    }

public:
    void push(int x) {
        inStack.push(x);
    }

    int pop() {
        transferIfEmpty();
        int val = outStack.top();
        outStack.pop();
        return val;
    }

    int peek() {
        transferIfEmpty();
        return outStack.top();
    }

    bool empty() {
        return inStack.empty() && outStack.empty();
    }
};
```
