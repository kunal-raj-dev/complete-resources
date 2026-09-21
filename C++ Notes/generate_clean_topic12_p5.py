import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t12_dir = os.path.join(root, "12_recursion_and_backtracking")

notes = {}

# 07: Rat in a Maze
notes["07_rat_in_a_maze.md"] = r"""# Lecture 48: Rat in a Maze: Grid Pathfinding & Visited State (GFG Classical)

> **One-Line Purpose:** Master 4-directional 2D matrix pathfinding using recursive backtracking, establishing in-place visited cell marking and generating lexicographically sorted traversal paths.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #48  
> **Video ID:** `D8Yze9CDDAw`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=D8Yze9CDDAw)  
> **Duration:** 32:45  
> **Transcript:** `.transcripts/12_recursion_and_backtracking/048_Rat_in_a_Maze_Problem___Backtracking.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- How to model 2D grid pathfinding from source `(0, 0)` to destination `(n-1, n-1)` as a state-space search tree.
- Why cyclic loops occur in grid exploration and how **Visited Tracking** prevents infinite recursion.
- How to mark cells in-place (`maze[r][c] = 0`) to achieve $O(1)$ auxiliary state memory without an extra boolean matrix.
- How to generate all valid paths in strict **lexicographical order**: Down ('D'), Left ('L'), Right ('R'), Up ('U').
- How state un-marking (`maze[r][c] = 1`) during backtracking preserves valid alternative routes.

---

## 🔵 Lecture Context

Rat in a Maze is the foundational grid backtracking problem. It directly prepares you for Word Search (LeetCode 79), Number of Islands (LeetCode 200), and Robot Room Cleaner.

---

## 1. Problem Statement

A rat is positioned at `(0, 0)` in an $N \times N$ binary grid `maze` and wants to reach the destination `(N-1, N-1)`.
- `maze[i][j] == 1`: Open cell (the rat can walk here).
- `maze[i][j] == 0`: Blocked cell (wall / obstacle).

The rat can move in 4 directions:
- Down: `(r + 1, c)` with move label `'D'`
- Left: `(r, c - 1)` with move label `'L'`
- Right: `(r, c + 1)` with move label `'R'`
- Up: `(r - 1, c)` with move label `'U'`

**Goal:** Return all unique paths the rat can take in lexicographical order. If no path exists, return an empty list.

---

## 2. Core Idea: Exploration with Cycle Prevention

If the rat moves Down to `(1, 0)` and then immediately moves Up back to `(0, 0)`, it enters an infinite cycle.
To prevent this:
1. When entering cell `(r, c)`, mark it visited (set `maze[r][c] = 0` or `visited[r][c] = true`).
2. Explore moves in exact alphabetical order: `'D'`, `'L'`, `'R'`, `'U'`.
3. When backtracking out of `(r, c)`, unmark it (restore `maze[r][c] = 1`).

---

## 3. Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <string>
using namespace std;

class Solution {
public:
    void solve(vector<vector<int>>& maze, int r, int c, int n, string& path, vector<string>& result) {
        // Base Case: Destination reached
        if (r == n - 1 && c == n - 1) {
            result.push_back(path);
            return;
        }

        // Mark current cell as visited (temporarily block it)
        maze[r][c] = 0;

        // 1. Down ('D'): (r + 1, c)
        if (r + 1 < n && maze[r + 1][c] == 1) {
            path.push_back('D');
            solve(maze, r + 1, c, n, path, result);
            path.pop_back(); // Backtrack
        }

        // 2. Left ('L'): (r, c - 1)
        if (c - 1 >= 0 && maze[r][c - 1] == 1) {
            path.push_back('L');
            solve(maze, r, c - 1, n, path, result);
            path.pop_back(); // Backtrack
        }

        // 3. Right ('R'): (r, c + 1)
        if (c + 1 < n && maze[r][c + 1] == 1) {
            path.push_back('R');
            solve(maze, r, c + 1, n, path, result);
            path.pop_back(); // Backtrack
        }

        // 4. Up ('U'): (r - 1, c)
        if (r - 1 >= 0 && maze[r - 1][c] == 1) {
            path.push_back('U');
            solve(maze, r - 1, c, n, path, result);
            path.pop_back(); // Backtrack
        }

        // Un-mark current cell (restore open state for sibling search paths)
        maze[r][c] = 1;
    }

    vector<string> findPath(vector<vector<int>>& maze, int n) {
        vector<string> result;
        // Edge cases: start or destination blocked
        if (maze[0][0] == 0 || maze[n - 1][n - 1] == 0) {
            return result;
        }

        string path = "";
        solve(maze, 0, 0, n, path, result);
        return result;
    }
};

int main() {
    Solution solver;
    vector<vector<int>> maze = {
        {1, 0, 0, 0},
        {1, 1, 0, 1},
        {1, 1, 0, 0},
        {0, 1, 1, 1}
    };

    vector<string> paths = solver.findPath(maze, 4);
    cout << "Valid Paths:\n";
    for (const string& p : paths) {
        cout << p << "\n";
    }
    return 0;
}
```

---

## 🔍 Detailed Trace: Grid `4x4`

```
Start at (0, 0).
- Move Down -> (1, 0)
- Move Down -> (2, 0)
- Move Right -> (2, 1) [Down to (3,0) is blocked!]
- Move Down -> (3, 1)
- Move Right -> (3, 2)
- Move Right -> (3, 3) [Destination reached!]
Path recorded: "DDRDRR"
```

---

## 🧠 Mental Model: Breadcrumbs

Think of marking `maze[r][c] = 0` as dropping a breadcrumb that blocks you from walking in circles. When the rat finishes exploring every possibility from that room and retreats, it picks the breadcrumb back up (`maze[r][c] = 1`) so that a different path may pass through that room if needed.

---

## ⚠️ Common Mistakes

1. **Forgetting to check Start and End:** If `maze[0][0] == 0` or `maze[n-1][n-1] == 0`, the rat cannot move at all.
2. **Missing Boundary Checks:** Accessing `maze[r+1][c]` without verifying `r + 1 < n` triggers memory access violations.
3. **Wrong Direction Order:** Exploring in non-alphabetical order (e.g. `R, D, L, U`) causes test-case failures on platforms requiring strict lexicographical output (`D, L, R, U`).

---

## 🖥️ System-Specific Notes

- **Max Path Length:** In an $N \times N$ grid, a simple path cannot exceed $N^2$ cells. For $N = 4$, the maximum recursion depth is $16$ frames, consuming negligible memory.

---

## 🟡 Additional Essential Context

Using coordinate delta arrays simplifies 4-directional code:
```cpp
const int dr[] = {1, 0, 0, -1};
const int dc[] = {0, -1, 1, 0};
const char dir[] = {'D', 'L', 'R', 'U'};
```

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Why must we restore `maze[r][c] = 1` when returning?  
**A:** Because a cell might be part of multiple distinct paths! If we left it as `0`, subsequent search paths would falsely believe that cell was permanently blocked.

---

### 🔥 Interview Questions

#### Q1: What is the worst-case time complexity of Rat in a Maze?
- **Short Answer:** $O(4^{N^2})$.
- **Detailed Explanation:** At each of the $N^2$ cells, the rat can branch in up to 4 directions. In an empty grid ($N \times N$ filled with 1s), the state-space tree depth is bounded by $N^2$, leading to $O(4^{N^2})$ paths in the worst case.

---

## 💻 Output / Debugging Questions

### Output Prediction
For `maze = {{1, 1}, {1, 1}}`:  
**Output:** `"DR" "RD"`  
**Explanation:** Both paths reach `(1, 1)` from `(0, 0)`.

---

## Edge Cases

1. **$1 \times 1$ Maze:** `maze = {{1}}` $\to$ Returns `[""]`.
2. **No Path:** Returns empty list `[]`.

---

## Complexity Analysis

- **Time Complexity:** $O(4^{N^2})$ worst-case branching.
- **Auxiliary Space Complexity:** $O(N^2)$ for recursion call stack.

---

## Key Takeaways

1. **In-place marking:** Avoids extra $O(N^2)$ boolean matrix allocation.
2. **Alphabetical order:** Guarantees lexicographically sorted results.
3. **Symmetric backtrack:** Always reset cell state before function return.

---

## ⚡ 2-Minute Revision

- Order: Down ('D'), Left ('L'), Right ('R'), Up ('U').
- In-place mark: `maze[r][c] = 0`; backtrack: `maze[r][c] = 1`.
- Bounds: `0 <= r < n` and `0 <= c < n`.
"""

# 08: Combination Sum
notes["08_combination_sum.md"] = r"""# Lecture 49: Combination Sum: Unbounded Choice Backtracking (LeetCode 39)

> **One-Line Purpose:** Master the Unbounded Knapsack-style backtracking paradigm by picking elements with unlimited reuse, implementing arithmetic pruning to avoid negative target states.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #49  
> **Video ID:** `jkgZw2WEaqA`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=jkgZw2WEaqA)  
> **Duration:** 23:35  
> **Transcript:** `.transcripts/12_recursion_and_backtracking/049_Combination_Sum_Problem___Recursion___Backtracking.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The requirements of LeetCode 39 (Combination Sum): finding all unique combinations of distinct integers summing to `target`.
- Why elements can be chosen **unlimited times**, and how this modifies the recursive transition (staying at index `i` vs advancing to `i + 1`).
- The Include / Skip decision logic and base-case termination when `target == 0` or `target < 0`.
- How sorting the candidate array allows **early break pruning** to eliminate unpromising branches.

---

## 🔵 Lecture Context

Combination Sum introduces unbounded element selection, bridging combinatorial backtracking with Unbounded Knapsack and Coin Change in Dynamic Programming.

---

## 1. Problem Statement

Given an array of **distinct** integers `candidates` and a target integer `target`, return a list of all **unique combinations** where the chosen numbers sum to `target`.
- The same number may be chosen from `candidates` an **unlimited number of times**.
- Two combinations are unique if the frequency of at least one chosen number is different.

```
Input: candidates = [2, 3, 6, 7], target = 7
Output: [[2, 2, 3], [7]]
```

---

## 2. Core Idea: The Unbounded Pick Decision Tree

At each candidate index `i`:
1. **Option 1 (Pick):** If `candidates[i] <= target`:
   - Subtract `candidates[i]` from `target`.
   - Add `candidates[i]` to `current`.
   - **Crucial Invariant:** Recurse with the **SAME index `i`** (not `i + 1`), because we are allowed to pick `candidates[i]` again!
   - Backtrack: pop `candidates[i]` and restore `target`.
2. **Option 2 (Skip):**
   - Advance to index `i + 1` to consider subsequent candidates without picking `candidates[i]`.

---

## 3. Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    void backtrack(const vector<int>& candidates, int target, int i, vector<int>& current, vector<vector<int>>& result) {
        // Base Case 1: Target reached
        if (target == 0) {
            result.push_back(current);
            return;
        }

        // Base Case 2: Exceeded target or exhausted candidates
        if (target < 0 || i == candidates.size()) {
            return;
        }

        // Option 1: Include candidates[i] (stay at index i for unbounded reuse)
        if (candidates[i] <= target) {
            current.push_back(candidates[i]);
            backtrack(candidates, target - candidates[i], i, current, result);
            current.pop_back(); // Backtrack
        }

        // Option 2: Skip candidates[i] (advance to i + 1)
        backtrack(candidates, target, i + 1, current, result);
    }

    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
        sort(candidates.begin(), candidates.end()); // Sorting allows early pruning
        vector<vector<int>> result;
        vector<int> current;
        backtrack(candidates, target, 0, current, result);
        return result;
    }
};

int main() {
    Solution solver;
    vector<int> candidates = {2, 3, 6, 7};
    int target = 7;
    vector<vector<int>> ans = solver.combinationSum(candidates, target);

    cout << "Combinations for target " << target << ":\n";
    for (const auto& comb : ans) {
        cout << "[ ";
        for (int x : comb) cout << x << " ";
        cout << "]\n";
    }
    return 0;
}
```

---

## 🔍 Detailed Trace: `candidates = [2, 3]`, `target = 5`

```
(i=0, val=2, target=5)
- Pick 2 -> target=3. Path: [2]
  - Pick 2 -> target=1. Path: [2, 2]
    - Pick 2 -> target=-1 (target < 0 -> Prune & backtrack)
    - Skip 2 -> (i=1, val=3, target=1)
      - Pick 3 -> target=-2 (Prune)
      - Skip 3 -> exhausted.
  - Skip 2 -> (i=1, val=3, target=3). Path: [2]
    - Pick 3 -> target=0 -> MATCH! Record [2, 3]
    - Skip 3 -> exhausted.
- Skip 2 -> (i=1, val=3, target=5). Path: []
  - Pick 3 -> target=2. Path: [3]
    ...
```

---

## 🧠 Mental Model: Coin Dispenser

Imagine a coin dispenser with infinite coins of denominations $2, 3, 6, 7$. You repeatedly push the coin 2 button until total exceeds target. Then you take back one coin and push the coin 3 button.

---

## ⚠️ Common Mistakes

1. **Advancing `i + 1` on Pick:** Passing `i + 1` after picking `candidates[i]` restricts each number to single use (solving 0/1 Knapsack instead of Unbounded Knapsack).
2. **Infinite Loops from Zero Values:** If candidates could contain `0`, picking `0` without reducing target causes infinite recursion. (LeetCode 39 guarantees candidates $\ge 2$).

---

## 🖥️ System-Specific Notes

- **Max Tree Depth:** Since the minimum candidate value is $2$, the maximum recursion depth is bounded by $\frac{\text{target}}{2}$. For `target = 40`, depth $\le 20$ frames ($\approx 1\text{ KB}$).

---

## 🟡 Additional Essential Context

In LeetCode 40 (Combination Sum II):
- Each candidate can only be used **once** (advance `i + 1`).
- The array may contain **duplicates**, requiring the duplicate skipping check: `if (j > i && candidates[j] == candidates[j-1]) continue;`.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Why does this generate unique combinations without duplicates like `[2, 3, 2]` and `[3, 2, 2]`?  
**A:** Because we only consider elements at or after index `i`. Once we skip `candidates[0]` (2) to move to `candidates[1]` (3), we can never pick `2` again! This directional invariant guarantees uniqueness.

---

### 🔥 Interview Questions

#### Q1: What is the time complexity bound for Combination Sum?
- **Short Answer:** $O(2^T \cdot K)$ where $T = \text{target} / \text{min\_val}$ and $K$ is average combination length.
- **Detailed Explanation:** In the worst case (e.g. `candidates = [1]`), the tree branches up to $T$ levels deep. Loose upper bound is exponential in target value.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
// candidates = [2], target = 3
// Output: [] (No solution possible)
```

---

## Edge Cases

1. **Target Smaller Than Smallest Candidate:** `candidates = [5, 10], target = 3` $\to$ Returns `[]`.
2. **Exact Single Match:** `candidates = [7], target = 7` $\to$ Returns `[[7]]`.

---

## Complexity Analysis

- **Time Complexity:** $O(2^T \cdot K)$ where $T = \text{target} / \text{min(candidates)}$.
- **Auxiliary Space Complexity:** $O(T)$ stack frames.

---

## Key Takeaways

1. **Unbounded selection:** Recurse with index `i` on pick; advance to `i + 1` on skip.
2. **Target reduction:** `target - candidates[i]`.
3. **Directional order:** Eliminates permutation duplicates automatically.

---

## ⚡ 2-Minute Revision

- Pick: `backtrack(target - candidates[i], i)`.
- Skip: `backtrack(target, i + 1)`.
- Stop when `target == 0` or `target < 0`.
"""

# 09: Palindrome Partitioning
notes["09_palindrome_partitioning.md"] = r"""# Lecture 50: Palindrome Partitioning: Substring Backtracking (LeetCode 131)

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
"""

print("Writing batch 3 notes...")
for fn, content in notes.items():
    with open(os.path.join(t12_dir, fn), "w", encoding="utf-8") as f:
        f.write(content)
print("Updated 07, 08, 09.")
