# Lecture 106: Recover BST (LeetCode 99)

> **One-Line Purpose:** Restore a corrupted BST where two nodes were swapped by locating inorder inversion anomalies.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #106  
> **Video ID:** `0KGzfij_SCk`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=0KGzfij_SCk)  
> **Duration:** 24:03  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Identify anomalies in a sorted sequence (inorder traversal of a BST).
- Distinguish between adjacent swapped nodes and non-adjacent swapped nodes.
- Recover the tree by swapping the values of the two identified nodes without altering the tree structure.

## 🧠 Core Intuition — Why This Works
The defining property of a BST is that its **inorder traversal is strictly increasing**.
If two nodes are swapped, this sorted order is violated.
There are two cases for the swapped nodes:
1. **Adjacent Swap:** `[1, 2, 3, 4, 5]` becomes `[1, 3, 2, 4, 5]`. 
   - There is ONE violation: `3 > 2`.
   - The swapped nodes are `3` and `2`.
2. **Non-Adjacent Swap:** `[1, 2, 3, 4, 5]` becomes `[1, 5, 3, 4, 2]`.
   - There are TWO violations: `5 > 3` and `4 > 2`.
   - The swapped nodes are the **first node of the first violation** (`5`) and the **second node of the second violation** (`2`).

By maintaining a `prev` pointer during an inorder traversal, we can detect these violations (`prev->val > curr->val`). We track the `first`, `middle` (second node of first violation), and `last` (second node of second violation) anomalous nodes.

**Visualization:**
```text
Tree:
      3
     / \
    1   4
       /
      2
Inorder: 1 -> 3 -> 2 -> 4 (Swapped 2 and 3)
Violations: 3 > 2 (first=3, middle=2).
Since there are no more violations, we swap first (3) and middle (2).

Corrected:
      2
     / \
    1   4
       /
      3
```

## 🎯 Pattern Recognition — When to Use This
**Trigger cues:**
- "Recover BST"
- "Two nodes swapped by mistake"
- "Fix binary search tree"
→ **Action:** Inorder traversal with `prev` pointer. Look for `prev->val > curr->val`.

## 📐 Algorithm Walk-Through
1. Initialize pointers `first`, `middle`, `last`, and `prev` to `nullptr`.
2. Perform Inorder Traversal:
   - Recurse left.
   - **Process Node:** 
     - If `prev != nullptr` and `root->val < prev->val`, a violation occurred.
     - If it's the **first violation** (`first == nullptr`), set `first = prev` and `middle = root`.
     - If it's the **second violation**, set `last = root`.
     - Set `prev = root`.
   - Recurse right.
3. Swap values:
   - If `last` is not null (non-adjacent swap), swap `first->val` and `last->val`.
   - Else (adjacent swap), swap `first->val` and `middle->val`.

## 💻 Complete C++ Implementation

```cpp
#include <algorithm>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionRecoverBST {
private:
    TreeNode* first = nullptr;
    TreeNode* middle = nullptr;
    TreeNode* last = nullptr;
    TreeNode* prev = nullptr;

    void inorder(TreeNode* root) {
        if (!root) return;

        inorder(root->left);

        if (prev && root->val < prev->val) {
            // First violation
            if (!first) {
                first = prev;
                middle = root;
            } else {
                // Second violation
                last = root;
            }
        }
        prev = root;

        inorder(root->right);
    }

public:
    void recoverTree(TreeNode* root) {
        first = middle = last = prev = nullptr;
        inorder(root);

        if (first && last) {
            swap(first->val, last->val);
        } else if (first && middle) {
            swap(first->val, middle->val);
        }
    }
};
```

## 🔍 Dry Run Trace
**Tree:** `[1, 3, null, null, 2]`
- `prev = null`.
- `inorder(1)` $\rightarrow$ no left. `prev = 1`.
- `inorder(3)` $\rightarrow$ no left. `3 > 1` (no violation). `prev = 3`.
- `inorder(2)` $\rightarrow$ no left. `2 < 3`! (Violation).
  - `first` is null, so `first = 3`, `middle = 2`.
  - `prev = 2`.
- End of traversal.
- `first` and `middle` are non-null. `last` is null.
- Swap `first->val` (3) and `middle->val` (2).
- Tree is fixed: `[1, 2, null, null, 3]`.

## ⚠️ Common Interview Mistakes
- **Confusing adjacent vs non-adjacent swaps:** Only tracking two nodes (e.g., `first` and `second`) and assuming every swap creates two violations. Adjacent swaps only create ONE violation! You must track `first`, `middle`, and `last`.
- **Using an explicit array:** Dumping the tree to an array, sorting the array, and then traversing the tree again to overwrite values works, but uses $O(N)$ space. Interviewers expect the $O(H)$ or $O(1)$ space pointer method.
- **Swapping node pointers instead of values:** Trying to rewire the actual `left` and `right` child pointers is incredibly difficult and error-prone. Swapping the integer `val` inside the nodes achieves the exact same result instantly.

## 📊 Complexity Analysis
- **Time Complexity:** $O(N)$ as we visit every node exactly once during inorder traversal.
- **Space Complexity:** $O(H)$ for the recursive call stack (where $H$ is the tree height). 

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: [Optimization] Can this be solved in strictly $O(1)$ space?
**Answer:** Yes. We can use Morris Inorder Traversal instead of recursion. Morris Traversal creates temporary links from predecessor leaves back to their roots, allowing traversal without a stack. We embed the anomaly detection logic inside the Morris processing block. The space complexity drops to exactly $O(1)$.

### Q2: [Logic] Why do we check `if (first && last)` before `if (first && middle)`?
**Answer:** If the swapped nodes were non-adjacent, there will be two violations. The first violation initializes `first` and `middle`. The second violation initializes `last`. The actual swapped nodes in this case are `first` and `last`. If we checked `first && middle` first, it would evaluate to true and perform the wrong swap.

### Q3: [Variant] What if the tree was a Min-Heap instead of a BST?
**Answer:** A Min-Heap's property is just that parents are smaller than children (no left/right ordering). An inorder traversal wouldn't help. We'd have to traverse the tree, checking every node against its parent and its children to find the swapped nodes.

## 🏆 Related Problems (Leetcode)
- **Leetcode 98:** Validate Binary Search Tree (Same anomaly detection)
- **Leetcode 530:** Minimum Absolute Difference in BST (Same `prev` pointer usage)

## 🔗 Cross-Topic Connections
- **Array Sorting Anomaly:** This problem is identical to: "You have a sorted array, but two elements are swapped. Find them."

## ⚡ 2-Minute Revision Flash Card
- **Pattern:** Find anomalies in sorted order $\rightarrow$ Inorder traversal with `prev`.
- **Adjacent Swap:** 1 Violation (`prev > curr`). Track `first = prev`, `middle = curr`. Swap `first` & `middle`.
- **Non-Adjacent Swap:** 2 Violations. Track `last = curr` on 2nd violation. Swap `first` & `last`.
- **Space trick:** Swap node values (`val`), don't rewire pointers.
- **Complexity:** $O(N)$ Time, $O(H)$ Space. (Use Morris traversal for $O(1)$ space).
