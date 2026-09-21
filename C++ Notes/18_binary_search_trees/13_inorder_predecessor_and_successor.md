# Lecture 110: Inorder Predecessor & Successor in BST

> **One-Line Purpose:** Find the immediate predecessor and successor of a given key in a BST in optimal $O(H)$ time and $O(1)$ auxiliary memory.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #110  
> **Video ID:** `IHNkql1tAnk`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=IHNkql1tAnk)  
> **Duration:** 19:50  
> **Status:** AUDITED  

---

## 1. 🧱 Prerequisite Concepts
- **BST Properties:** Left is smaller, Right is larger.
- **Inorder Successor:** The node that appears immediately *after* a given node in an inorder traversal (the smallest value that is strictly greater than the target).
- **Inorder Predecessor:** The node that appears immediately *before* a given node in an inorder traversal (the largest value that is strictly smaller than the target).

## 2. 🧠 Core Concept & Explanation
A naive approach is to perform an Inorder Traversal and keep tracking previous elements. But this takes $O(N)$ time. We must utilize the BST property to do this in $O(H)$ time.

**Finding the Successor (Just Greater):**
If we stand at a node and its value is greater than the target `key`, it is a potential successor! We save it, but since we want the *smallest* possible greater value, we must move to the `left` subtree to see if we can find an even tighter fit. 
If the node's value is $\le$ the target `key`, it cannot be the successor. So we move `right` to look for larger values.

**Finding the Predecessor (Just Smaller):**
It’s the exact opposite! If a node's value is less than the target `key`, it is a potential predecessor! We save it, and then move to the `right` subtree to see if we can find a tighter fit (a larger value that is still less than the key).
If the node's value is $\ge$ the target `key`, it cannot be the predecessor, so we move `left`.

## 3. 🚶‍♂️ Step-by-step Approach (Algorithm)
1. Initialize `pre = nullptr` and `suc = nullptr`.
2. **For Successor:**
   - Start `curr = root`.
   - While `curr != nullptr`:
     - If `curr->val > key`: It's a valid candidate for successor. Record it (`suc = curr`) and search left (`curr = curr->left`) for a smaller candidate.
     - Else (`curr->val <= key`): Search right (`curr = curr->right`).
3. **For Predecessor:**
   - Reset `curr = root`.
   - While `curr != nullptr`:
     - If `curr->val < key`: It's a valid candidate for predecessor. Record it (`pre = curr`) and search right (`curr = curr->right`) for a larger candidate.
     - Else (`curr->val >= key`): Search left (`curr = curr->left`).

## 4. 🔍 Dry Run / Execution Trace
Tree:
```text
       10
      /  \
     5    15
    / \
   2   8
```
**Find Pre/Suc for Key = `6`**

*Successor Loop:*
1. `curr = 10`. `10 > 6`. Record `suc = 10`. Move `curr = 5`.
2. `curr = 5`. `5 <= 6`. Move `curr = 8`.
3. `curr = 8`. `8 > 6`. Record `suc = 8`. Move `curr = left of 8 (null)`.
4. Loop ends. Final Successor = `8`.

*Predecessor Loop:*
1. `curr = 10`. `10 >= 6`. Move `curr = 5`.
2. `curr = 5`. `5 < 6`. Record `pre = 5`. Move `curr = 8`.
3. `curr = 8`. `8 >= 6`. Move `curr = left of 8 (null)`.
4. Loop ends. Final Predecessor = `5`.

## 5. 💻 Complete C++ Implementation

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

void findPreSuc(TreeNode* root, TreeNode*& pre, TreeNode*& suc, int key) {
    TreeNode* curr = root;

    // Find Successor: smallest key strictly greater than key
    while (curr) {
        if (curr->val > key) {
            suc = curr;
            curr = curr->left; // Try to find a smaller one that is still > key
        } else {
            curr = curr->right;
        }
    }

    curr = root;
    // Find Predecessor: largest key strictly smaller than key
    while (curr) {
        if (curr->val < key) {
            pre = curr;
            curr = curr->right; // Try to find a larger one that is still < key
        } else {
            curr = curr->left;
        }
    }
}
```

## 6. ⏱️ Complexity Analysis
- **Time Complexity:** $O(H)$ for successor + $O(H)$ for predecessor = $O(H)$ total, where $H$ is the height of the BST. In the worst-case (skewed), this is $O(N)$.
- **Space Complexity:** $O(1)$. We use iterative while loops entirely, without any recursive stack frames.

## 7. ⚠️ Edge Cases to Consider
- **Key does not exist in the BST:** The logic still works flawlessly. It acts as if the key was virtually there.
- **Key is the Maximum Element:** Successor remains `nullptr`.
- **Key is the Minimum Element:** Predecessor remains `nullptr`.
- **Root is `nullptr`:** Safely handles it without entering the loops.

## 8. ❌ Common Pitfalls & Mistakes
- **Doing a standard recursive search:** Many folks memorize the "find min in right subtree" logic for successor, but that logic ONLY works if the node actually exists in the tree AND has a right child. If the node has no right child, the successor is one of its ancestors. The iterative record-and-move approach solves all cases cleanly!
- **Getting inequalities wrong:** Using `>=` instead of `>` for successor. Remember, successor is strictly greater, and predecessor is strictly smaller.

## 🎯 Pattern Recognition — When to Use This
- **Trigger Cues:** "Next larger element in BST", "Previous smaller element in BST", "Find the closest values".
- **Why Iterative Traversal?** Whenever you need to find an element in a BST relative to a target value, keeping track of the "best valid candidate seen so far" while iteratively walking down the tree ensures $O(H)$ time and $O(1)$ space. It elegantly avoids handling the complex edge cases of "no right child" that plague recursive implementations.

## 🏆 Related Problems (Leetcode)
- **Leetcode 285. Inorder Successor in BST (Premium):** The direct implementation of the successor half of this logic.
- **Leetcode 510. Inorder Successor in BST II (Premium):** You are given a node with a parent pointer but no root. Requires traversing upwards if no right child exists.
- **Leetcode 270. Closest Binary Search Tree Value:** Similar logic; as you traverse, you update the closest value seen so far.
- **Leetcode 450. Delete Node in a BST:** Finding the inorder successor (or predecessor) is a mandatory sub-step when deleting a node that has two children.

## 🔗 Cross-Topic Connections
- **Binary Search (Arrays):** The logic is identical to finding the `upper_bound` (successor) or `lower_bound - 1` (predecessor) in a sorted array!
- **BST Deletion:** Fundamental requirement for resolving two-child node deletions.

## 9. 💡 Expert Q&A / Interview Follow-ups
**Q1: Can we do this in a single traversal pass instead of two separate `while` loops?**  
*Answer:* Yes, you can combine the logic into one recursive function or a single loop, but practically two sequential $O(H)$ loops run sequentially and are still asymptotic $O(H)$ time. Code readability usually favors keeping them separated as they track orthogonal constraints.

**Q2: What if we have parent pointers in our `TreeNode` definition?**  
*Answer:* If you have parent pointers and are given the direct `TreeNode*` of the target (not just an `int` key), you can find the successor in $O(1)$ space without traversing from the root! If `node->right` exists, it's the minimum of the right subtree. If `node->right` is null, you crawl up the parent pointers until you find a node that is the *left* child of its parent. That parent is the successor.

**Q3: How does this logic change if the BST contains duplicate values?**
*Answer:* If the BST has duplicates, the inorder successor is strictly defined as the node with the smallest value strictly greater than the target. The logic `curr->val > key` natively handles duplicates perfectly because it only records candidates that are *strictly greater*.

**Q4: Why does the recursive definition "min value in the right subtree" fail for some cases?**
*Answer:* The recursive definition assumes the node actually *has* a right child. If you ask for the successor of `8` in a tree where `8` is a left child of `10` and has no right child, the recursive method on `8` panics. The successor is actually `10`. The iterative approach tracks `10` as a candidate before stepping left to `8`, so it naturally handles this.

**Q5: Can we use this logic to validate a BST?**
*Answer:* No. Finding the predecessor and successor assumes the tree is already a valid BST. Validating a BST requires checking global min/max constraints, not just finding relative neighbors.

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Find Inorder Predecessor (just smaller) and Successor (just larger) in $O(H)$ time, $O(1)$ space.
- **Successor Logic:** If `curr > key`, record it as candidate, go `left`. Else go `right`.
- **Predecessor Logic:** If `curr < key`, record it as candidate, go `right`. Else go `left`.
- **Trap:** Do not use the $O(N)$ Inorder Traversal array approach in interviews. Always use the $O(1)$ space iterative walk.
