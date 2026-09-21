# Lecture 97: Flatten Binary Tree to Linked List (LeetCode 114)

> **One-Line Purpose:** Flatten a binary tree into a right-spine linked list in-place in $O(1)$ space using Morris-style rightmost leaf linking.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #97  
> **Video ID:** `dU2Z5HWSGM0`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=dU2Z5HWSGM0)  
> **Duration:** 15:43  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Transform a binary tree into a "linked list" where every node's `left` is null, and `right` points to the next node in pre-order traversal.
- Achieve this in $O(1)$ auxiliary space without using recursion stacks or queues.
- Understand the logic of finding the predecessor (rightmost node of the left subtree) inspired by Morris Traversal.

## 🧠 Core Intuition — Why This Works
If we look at a Pre-order traversal (Root, Left, Right), the entire Left subtree comes *before* the entire Right subtree. 
To flatten the tree in-place so it forms a single rightward line, we need the very last node of the Left subtree (its rightmost leaf) to point to the start of the Right subtree.
Once we attach the Right subtree to the bottom of the Left subtree, we can safely move the whole Left subtree to become the new Right subtree, and set the Left child to null. We repeat this process moving downwards.

**Visualization:**
```text
Original:
    1
   / \
  2   5
 / \   \
3   4   6

Step 1: Current=1. Left subtree exists (2). Find its rightmost node (4).
Attach 1's right (5) to 4's right.
Move 1's left (2) to 1's right. Left becomes null.
    1
     \
      2
     / \
    3   4
         \
          5
           \
            6

Step 2: Move down to 2. Left exists (3). Rightmost is 3. 
Attach 2's right (4) to 3's right. Move 3 to right.
    1
     \
      2
       \
        3
         \
          4
           \
            5
             \
              6
```

## 🎯 Pattern Recognition — When to Use This
**Trigger cues:**
- "Flatten tree"
- "In-place modification of tree structure to list"
- "O(1) space traversal"
→ **Action:** Morris Traversal technique (wiring predecessors to successors).

## 📐 Algorithm Walk-Through
1. Start with a pointer `curr = root`.
2. While `curr` is not null:
   - Check if `curr->left` exists.
   - If it does, find the rightmost node in the left subtree. Call it `prev` (`prev = curr->left`, then `while(prev->right) prev = prev->right`).
   - Wire `prev->right` to `curr->right` (attaching the old right subtree).
   - Move the whole left subtree to the right: `curr->right = curr->left`.
   - Set the left subtree to null: `curr->left = nullptr`.
   - Now move `curr` to `curr->right` (which used to be the left subtree) and repeat.
   - If `curr->left` doesn't exist, just move `curr = curr->right`.

## 💻 Complete C++ Implementation

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionFlatten {
public:
    void flatten(TreeNode* root) {
        TreeNode* curr = root;

        while (curr) {
            if (curr->left) {
                // Find rightmost node of left subtree
                TreeNode* prev = curr->left;
                while (prev->right) {
                    prev = prev->right;
                }

                // Rewire: connect right subtree to rightmost node of left subtree
                prev->right = curr->right;
                curr->right = curr->left;
                curr->left = nullptr;
            }
            curr = curr->right;
        }
    }
};
```

## 🔍 Dry Run Trace
**Tree:** `[1, 2, 5, 3, 4, null, 6]`
- `curr = 1`. Has left (2).
  - Find rightmost of left (2): it is 4.
  - Wire: `4->right = 1->right` (5).
  - Move: `1->right = 1->left` (2). `1->left = null`.
  - Move: `curr = 1->right` (which is now 2).
- `curr = 2`. Has left (3).
  - Find rightmost of left (3): it is 3.
  - Wire: `3->right = 2->right` (4).
  - Move: `2->right = 2->left` (3). `2->left = null`.
  - Move: `curr = 2->right` (which is now 3).
- `curr = 3`. No left. `curr = curr->right` (4).
- `curr = 4`. No left. `curr = curr->right` (5).
- `curr = 5`. No left. `curr = curr->right` (6).
- `curr = 6`. No left. `curr = null`. Loop ends.

## ⚠️ Common Interview Mistakes
- **Using a Stack or Recursion:** Using an explicit stack or recursion makes the space complexity $O(N)$ or $O(H)$. The problem explicitly hints at finding an $O(1)$ space solution.
- **Losing the Right Subtree:** If you do `curr->right = curr->left` before attaching the old right subtree to the predecessor, you completely lose the reference to the right subtree.

## 📊 Complexity Analysis
- **Time Complexity:** $O(N)$. Even though there is a nested while loop to find the rightmost node, every edge is traversed at most twice (once during the rightmost search, once during the main `curr` iteration).
- **Space Complexity:** $O(1)$ auxiliary memory since we only use a couple of pointers (`curr`, `prev`).

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: [Concept] How is this related to Morris Traversal?
**Answer:** Morris Traversal also works in $O(1)$ space by linking the rightmost node of a left subtree (predecessor) to the current node to create a way back up. Here, instead of a temporary link to go back, we create a *permanent* link to the right subtree to flatten the structure.

### Q2: [Alternative] How would you solve this if $O(N)$ space was allowed?
**Answer:** I would do a standard Recursive Pre-order Traversal (Right, Left, Root -- wait, reversed pre-order). If we traverse Right, then Left, then Root, we can maintain a global `prev` pointer. At each step, `root->right = prev`, `root->left = nullptr`, and `prev = root`. This builds the flattened tree from bottom-up.

### Q3: [Variant] What if we wanted to flatten it based on In-order traversal?
**Answer:** To flatten based on In-order, the root's left subtree should end up before the root, and the right subtree after it. This transforms it into a doubly-linked list (which is a famous problem: Convert BST to Sorted Doubly Linked List). We would use an inorder traversal, keeping a `prev` pointer to wire `prev->right = curr` and `curr->left = prev`.

## 🏆 Related Problems (Leetcode)
- **Leetcode 426:** Convert Binary Search Tree to Sorted Doubly Linked List (Similar rewiring concept)
- **Leetcode 430:** Flatten a Multilevel Doubly Linked List

## 🔗 Cross-Topic Connections
- **Linked Lists:** The pointer rewiring operations here are exactly the same mental muscle used for Linked List reversal and manipulation.

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Pre-order flatten to right spine, $O(1)$ space.
- **Trick:** If left child exists, its rightmost leaf is the predecessor to the right child.
- **Wire:** `prev->right = curr->right`.
- **Shift:** `curr->right = curr->left`, `curr->left = null`.
- **Time/Space:** $O(N)$ Time, $O(1)$ Space.
