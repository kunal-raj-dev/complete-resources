# Lecture 102: Kth Smallest Element in BST (LeetCode 230)

> **One-Line Purpose:** Retrieve the Kth smallest element in $O(H + K)$ time via early-terminating inorder traversal.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #102  
> **Video ID:** `Kq4BbvIhj44`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=Kq4BbvIhj44)  
> **Duration:** 12:43  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Use Inorder Traversal to visit BST nodes in ascending order.
- Implement early termination in recursive algorithms to save unnecessary computation.
- Maintain a running count to identify the K-th visited node.

## 🧠 Core Intuition — Why This Works
The defining property of a Binary Search Tree is that an **inorder traversal** (Left, Root, Right) visits the nodes in strictly increasing (sorted) order.
If we want the 1st smallest element, it's the very first node processed in the inorder traversal.
If we want the $K$-th smallest, we just keep a counter. Every time we process a node (after returning from its left child), we increment the counter. When `count == K`, we've found our answer.

**Visualization:**
```text
Find 3rd smallest (K=3)
Tree:
      5
     / \
    3   6
   / \
  2   4
 /
1

Inorder path: 
Visit 1 -> Count=1
Visit 2 -> Count=2
Visit 3 -> Count=3 (Match! Stop traversal)
```

## 🎯 Pattern Recognition — When to Use This
**Trigger cues:**
- "Kth smallest/largest in BST"
- "Rank of element in BST"
→ **Action:** Inorder traversal with a counter. Reverse inorder (Right, Root, Left) for Kth largest.

## 📐 Algorithm Walk-Through
1. Initialize class members: `count = 0` and `result = -1`.
2. Define `inorder(root, k)`:
   - **Base Case:** If `root` is null or `count >= k` (early termination), return.
   - **Left Subtree:** Call `inorder(root->left, k)`.
   - **Process Node:** Increment `count`. If `count == k`, set `result = root->val` and return immediately.
   - **Right Subtree:** Call `inorder(root->right, k)`.
3. In main function, reset variables and start traversal. Return `result`.

## 💻 Complete C++ Implementation

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionKthSmallest {
private:
    int result = -1;
    int count = 0;

    void inorder(TreeNode* root, int k) {
        if (!root || count >= k) return;

        inorder(root->left, k);

        count++;
        if (count == k) {
            result = root->val;
            return;
        }

        inorder(root->right, k);
    }

public:
    int kthSmallest(TreeNode* root, int k) {
        count = 0;
        inorder(root, k);
        return result;
    }
};
```

## 🔍 Dry Run Trace
**Tree:** `[3, 1, 4, null, 2]`, **K = 2**
- `inorder(3)` $\rightarrow$ calls `inorder(1)`.
- `inorder(1)` $\rightarrow$ calls `inorder(null)`.
- `inorder(null)` returns.
- Process node `1`: `count++` (count=1). `count != 2`.
- `inorder(1)` calls `inorder(2)` (right child).
- `inorder(2)` $\rightarrow$ calls `inorder(null)`.
- `inorder(null)` returns.
- Process node `2`: `count++` (count=2). `count == 2`!
  - `result = 2`. Return.
- All subsequent `count >= k` checks immediately return, pruning the rest of the tree.
- **Output:** `2`.

## ⚠️ Common Interview Mistakes
- **Forgetting early termination:** Continuing the traversal even after finding the Kth element. This turns an $O(H + K)$ solution into an $O(N)$ solution, which interviewers will penalize.
- **Global Variable Trap:** Using a global variable for `count` and `result` without resetting it inside `kthSmallest`. When Leetcode runs multiple test cases on the same object, the state carries over and fails. Always reset them!
- **Using an array:** Pushing all inorder elements to an array and then accessing `arr[k-1]`. This wastes $O(N)$ space and time.

## 📊 Complexity Analysis
- **Time Complexity:** $O(H + K)$, where $H$ is the tree height. We go down to the leftmost leaf ($O(H)$) and then visit $K$ nodes. Best case (K=1, skewed left): $O(N)$. Average balanced case: $O(\log N + K)$.
- **Space Complexity:** $O(H)$ for the recursive call stack.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: [Follow-up] What if the BST is modified (insert/delete) often and you need to find the Kth smallest frequently?
**Answer:** The current approach takes $O(H+K)$ each time. To optimize for frequent queries, we can modify the BST node structure to store the size of its left subtree (or the total nodes in the subtree). Finding the Kth smallest then becomes a binary search taking $O(H)$ time, bypassing the $K$ traversal. 

### Q2: [Optimization] How would you solve this iteratively?
**Answer:** I would use an explicit stack. Push all left children until `nullptr`, pop a node, increment `count`. If `count == k`, return the node's value. Otherwise, push its right child and repeat. This naturally supports early termination and avoids recursion overhead.

### Q3: [Variant] How do you find the Kth *largest* element?
**Answer:** Do a "Reverse Inorder Traversal" (Right, Root, Left). The Kth node visited will be the Kth largest element.

### Q4: [Edge Case] What if $K$ is larger than the number of nodes in the tree?
**Answer:** If this is possible based on constraints, the function will finish traversing without `count` ever reaching $K$. `result` would remain its initialized value (e.g., `-1`). We should check constraints or clarify with the interviewer if we need to throw an exception or return a sentinel value.

### Q5: [Memory constraints] Can you solve this in $O(1)$ space?
**Answer:** Yes, by using Morris Inorder Traversal. Morris traversal modifies the tree structure temporarily by creating links from predecessors to their successors to avoid the $O(H)$ stack space. However, modifying the tree structure is generally discouraged in concurrent environments.

## 🏆 Related Problems (Leetcode)
- **Leetcode 98:** Validate Binary Search Tree (Inorder property)
- **Leetcode 173:** Binary Search Tree Iterator (Next smallest element pattern)
- **Leetcode 703:** Kth Largest Element in a Stream (Min-heap vs BST approaches)

## 🔗 Cross-Topic Connections
- **Heaps:** Finding Kth smallest/largest in an *unsorted* array is typically done with a Max/Min Heap. In a BST, the structural properties give us this for "free" with traversal.

## ⚡ 2-Minute Revision Flash Card
- **Core Concept:** Inorder traversal of BST gives elements in sorted ascending order.
- **Implementation:** Recursively traverse Inorder. Keep a `count`. When `count == K`, save value and stop.
- **Crucial Optimization:** Pass `k` and use `if (count >= k) return;` to short-circuit and avoid visiting the entire tree.
- **Time/Space:** $O(H + K)$ Time, $O(H)$ Space.
- **Follow-up:** For frequent updates/queries, augment BST nodes with `subtree_size`.
