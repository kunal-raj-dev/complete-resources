# Lecture 77: The Celebrity Problem

> **One-Line Purpose:** Identify the unique celebrity who knows nobody and is known by everybody at a party of $N$ people using 2-pointer elimination in $O(N)$ time and $O(1)$ space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #77  
> **Video ID:** `OZPmEA_8FM8`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=OZPmEA_8FM8)  
> **Duration:** 15:11  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Formulate the logical elimination invariant for `knows(A, B)`.
- Understand why this problem is commonly taught with Stacks, but optimally solved with Two Pointers.
- Master the mandatory "Verification Step" for potential candidates.

---

## 🧠 Core Intuition — Why This Works

A Celebrity has two strict properties:
1. They know **nobody**. (Row is all 0s, except possibly `M[i][i]`).
2. **Everybody** knows them. (Column is all 1s, except possibly `M[i][i]`).

If we ask the question: "Does person $A$ know person $B$?" (`M[A][B] == 1`):
- If **Yes**, $A$ knows someone. A Celebrity knows nobody! Therefore, **$A$ is NOT the celebrity.**
- If **No**, $B$ is not known by $A$. A Celebrity is known by everybody! Therefore, **$B$ is NOT the celebrity.**

**The Elimination Tournament:**
Every single question we ask eliminates exactly one person from consideration. 
If we have $N$ people, asking $N-1$ questions will eliminate $N-1$ people, leaving exactly 1 "Potential Candidate".

**The Verification:**
The survivor of the tournament is the *only* person who *could* be the celebrity. But they might just be a regular person in a room where no actual celebrity exists! We must run a final $O(N)$ loop to verify their row and column.

---

## 🎯 Pattern Recognition — When to Use This
Trigger cues: "if you see X in a problem, think Y"
- **"Find the sink in a directed graph"**: A vertex with out-degree 0 and in-degree $N-1$. This is the exact same problem!
- **"Matrix where $M[i][j]$ denotes a relationship"**: Directed relation elimination.
- **"Find a unique element that fits a global criteria"**: Tournament elimination.

---

## 📐 Algorithm Walk-Through

**The Stack Method (Suboptimal Space $O(N)$):**
1. Push all people $0$ to $N-1$ into a Stack.
2. Pop top two elements, $A$ and $B$.
3. If $A$ knows $B$, discard $A$, push $B$ back.
4. If $A$ doesn't know $B$, discard $B$, push $A$ back.
5. The last remaining element is the candidate. Verify them.

**The Two-Pointer Method (Optimal Space $O(1)$):**
1. Pointer `i = 0`, `j = N - 1`.
2. While `i < j`:
   - If `M[i][j] == 1`, `i` knows `j`, so `i` is out. `i++`.
   - Else, `i` does not know `j`, so `j` is out. `j--`.
3. The loop stops when `i == j`. This `i` is our candidate.
4. Verify candidate: loop `k` from $0$ to $N-1$.
   - If `k != i`:
     - If candidate knows `k` (`M[i][k] == 1`), return `-1`.
     - If `k` doesn't know candidate (`M[k][i] == 0`), return `-1`.
5. Return `i`.

---

## 💻 Complete C++ Implementation: Optimal Two-Pointer

```cpp
#include <vector>
#include <iostream>

using namespace std;

class CelebritySolver {
public:
    // M[i][j] = 1 means i knows j
    static int findCelebrity(int n, const vector<vector<int>>& M) {
        int i = 0, j = n - 1;

        // Step 1: Elimination Tournament
        while (i < j) {
            if (M[i][j] == 1) {
                // i knows j -> i cannot be celebrity. Next!
                i++; 
            } else {
                // i does NOT know j -> j cannot be celebrity. Next!
                j--; 
            }
        }

        int candidate = i; // The sole survivor

        // Step 2: Verification
        for (int k = 0; k < n; ++k) {
            if (k != candidate) {
                // The candidate must NOT know k, AND k MUST know the candidate
                if (M[candidate][k] == 1 || M[k][candidate] == 0) {
                    return -1; // Not a true celebrity
                }
            }
        }

        return candidate;
    }
};

int main() {
    // 1 is the celebrity (knows no one, 0 and 2 know 1)
    vector<vector<int>> M = {
        {0, 1, 0},
        {0, 0, 0},
        {0, 1, 0}
    };
    
    cout << "Celebrity: " << CelebritySolver::findCelebrity(3, M) << endl; 
    // Output: 1
    
    return 0;
}
```

---

## 🔍 Dry Run Trace

**Input:** 
```text
  0 1 2
0 0 1 0
1 0 0 0
2 0 1 0
```
- `i = 0, j = 2`.
- `M[0][2] == 0`. (0 does NOT know 2). 2 cannot be celebrity. `j--`.
- `i = 0, j = 1`.
- `M[0][1] == 1`. (0 knows 1). 0 cannot be celebrity. `i++`.
- `i = 1, j = 1`. Loop ends. Candidate is `1`.

**Verification for Candidate 1:**
- `k = 0`: Does 1 know 0? `M[1][0] == 0` (No, good). Does 0 know 1? `M[0][1] == 1` (Yes, good).
- `k = 2`: Does 1 know 2? `M[1][2] == 0` (No, good). Does 2 know 1? `M[2][1] == 1` (Yes, good).
**Result:** 1 is the celebrity.

---

## ⚠️ Common Interview Mistakes

1. **Forgetting the Verification Step**: The elimination tournament ONLY guarantees that IF a celebrity exists, it must be the survivor. It does NOT guarantee a celebrity actually exists. You MUST verify the survivor. If you skip this, you fail the interview.
2. **Checking the Diagonal**: When verifying, make sure to skip `k == candidate` (or ensure `M[k][k]` doesn't falsely fail the logic). Usually, a person is assumed to know themselves, but sometimes `M[k][k] = 0`. Skipping it is safest.
3. **Using $O(N^2)$ brute force**: Iterating every row and counting 1s is trivial but highly inefficient. $O(N)$ is strictly expected.

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(N)$. $N-1$ checks in the tournament, $2N$ checks in verification. Total $\approx 3N$ operations.
- **Space Complexity:** $O(1)$ strictly for the Two-Pointer approach. ($O(N)$ if using the Stack).

---

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: Why is this categorized under Stack problems when Two-Pointers is better space?
**Answer:** Historically, it's taught with Stacks because the tournament structure closely matches pushing and popping candidates. It's a stepping stone to teach algorithmic optimization. Interviewers often *want* you to mention the Stack approach first, and then say "But I can optimize the space to $O(1)$ by using Two Pointers."

### Q2: What if the API gives you a function `bool knows(a, b)` instead of a matrix? Does anything change?
**Answer:** No. LeetCode 277 actually provides this exact API. The logic remains identical. You just replace `M[i][j] == 1` with `knows(i, j)`. The matrix is just a visual representation.

### Q3: Can there be TWO celebrities in the room?
**Answer:** Logically impossible. If there were two celebrities, A and B. For A to be a celebrity, A must know NO ONE (so A doesn't know B). For B to be a celebrity, EVERYONE must know B (so A must know B). Contradiction. There is a maximum of 1 celebrity.

### Q4: How is this related to Graph Theory?
**Answer:** As mentioned, it's the problem of finding a "Universal Sink" in a Directed Graph. A node with in-degree $V-1$ and out-degree $0$.

---

## 🏆 Related Problems (Leetcode)
1. **[Leetcode 277: Find the Celebrity](https://leetcode.com/problems/find-the-celebrity/)** — Premium problem. The exact algorithm using the `knows(a, b)` API.
2. **[Leetcode 997: Find the Town Judge](https://leetcode.com/problems/find-the-town-judge/)** — A variation where you are given edges instead of a matrix or API, requiring you to count in-degrees and out-degrees in $O(E)$ time.

---

## 🔗 Cross-Topic Connections
- **Graphs:** Universal Sink in a Directed Graph.
- **Two Pointers:** The optimal reduction technique from $O(N)$ Stack to $O(1)$ auxiliary space.

---

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Find person who knows no one, but everyone knows them.
- **Tournament Invariant:** If `A` knows `B`, `A` is out. If `A` doesn't know `B`, `B` is out.
- **Optimal Approach:** Two-pointers `i=0, j=N-1`. Shrink window until `i==j`.
- **CRITICAL STEP:** Verify the sole survivor `i`. Ensure row is all 0s, col is all 1s.
- **Time/Space:** $O(N)$ Time | $O(1)$ Space.
