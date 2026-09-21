# Lecture 98: Binary Search Trees (BSTs): Search, Insert & Delete

> **One-Line Purpose:** Master the Binary Search Tree invariant ($\text{Left} < \text{Root} < \text{Right}$), Inorder sorted property, and 3-case node deletion.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #98  
> **Video ID:** `RuF7dPfj27Q`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=RuF7dPfj27Q)  
> **Duration:** 43:16  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Understand the core property of a Binary Search Tree (BST).
- Master the `search`, `insert`, and `delete` operations in a BST.
- Learn the three specific cases for node deletion (leaf, one child, two children).
- Analyze the time and space complexity in both balanced and skewed scenarios.

## 🧠 Core Intuition — Why This Works
A Binary Search Tree (BST) is like a **dictionary** or a **phone book**. 
- If you are looking for "Smith", and you open the book to "Miller", you know instantly that "Smith" must be in the right half of the remaining pages. You completely discard the left half.
- In a BST, for any given node, **all elements in the left subtree are strictly smaller**, and **all elements in the right subtree are strictly larger**.
- This property ($\text{Left} < \text{Root} < \text{Right}$) must hold true for *every* node in the tree, not just the root.

**Visualization (Valid BST):**
```text
       8
     /   \
    3     10
   / \      \
  1   6      14
     / \    /
    4   7  13
```
*Notice: An **Inorder Traversal** (Left, Root, Right) of a valid BST always yields a strictly sorted sequence (1, 3, 4, 6, 7, 8, 10, 13, 14).*

## 🎯 Pattern Recognition — When to Use This
**Trigger cues for BST:**
- "Find the closest element / minimum / maximum in a dynamic dataset" → **BST**
- "Inorder successor / predecessor" → **BST**
- "Maintain a sorted stream of numbers and support rapid insertion/deletion" → **BST (balanced)**
- "Is this tree valid?" → **BST property check (min/max bounds)**

## 📐 Algorithm Walk-Through
**1. Search (Key = 6):**
- Start at root (8). $6 < 8$, go left.
- Current node (3). $6 > 3$, go right.
- Current node (6). Match found! Return node.

**2. Insert (Key = 5):**
- Start at root (8). $5 < 8$, go left.
- Current node (3). $5 > 3$, go right.
- Current node (6). $5 < 6$, go left.
- Current node (4). $5 > 4$, go right.
- Right of 4 is `nullptr`. Insert 5 there.

**3. Delete (Key = 3):**
- Find the node (3). It has two children (1 and 6).
- **Case 3 (Two Children):** Find the *Inorder Successor* (smallest value in the right subtree). 
  - Go to right child (6), then all the way left to (4). The successor is 4.
- Copy successor's value (4) to the node to be deleted (replace 3 with 4).
- Recursively call `delete` on the right subtree (6) to remove the successor node (4), which will fall into Case 1 or 2.

## 🔵 Complete C++ Implementation

```cpp
#include <iostream>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

// 1. Search in BST
TreeNode* searchBST(TreeNode* root, int val) {
    if (!root || root->val == val) return root;
    if (val < root->val) return searchBST(root->left, val);
    return searchBST(root->right, val);
}

// 2. Insert into BST
TreeNode* insertIntoBST(TreeNode* root, int val) {
    if (!root) return new TreeNode(val);
    if (val < root->val) root->left = insertIntoBST(root->left, val);
    else root->right = insertIntoBST(root->right, val);
    return root;
}

// Helper: Find Minimum Node (Inorder Successor)
TreeNode* findMin(TreeNode* root) {
    while (root->left) root = root->left;
    return root;
}

// 3. Delete from BST
TreeNode* deleteNode(TreeNode* root, int key) {
    if (!root) return nullptr;

    if (key < root->val) {
        root->left = deleteNode(root->left, key);
    } else if (key > root->val) {
        root->right = deleteNode(root->right, key);
    } else {
        // Case 1: Leaf node
        if (!root->left && !root->right) {
            delete root;
            return nullptr;
        }
        // Case 2: One child
        else if (!root->left) {
            TreeNode* temp = root->right;
            delete root;
            return temp;
        } else if (!root->right) {
            TreeNode* temp = root->left;
            delete root;
            return temp;
        }
        // Case 3: Two children
        else {
            TreeNode* successor = findMin(root->right);
            root->val = successor->val;
            root->right = deleteNode(root->right, successor->val);
        }
    }
    return root;
}
```

## 🔍 Dry Run Trace
**Deleting Node '3' from the tree above:**
1. Call `deleteNode(root=8, key=3)`.
2. $3 < 8$, call `deleteNode(root->left (3), 3)`.
3. Node `3` found. It has two children (1 and 6).
4. `successor = findMin(3->right)`. Starts at 6, left child is 4, left child is null. Returns 4.
5. `root->val = successor->val`. Node 3 becomes 4.
6. `root->right = deleteNode(root->right (6), 4)`.
7. $4 < 6$, call `deleteNode(root->left (4), 4)`.
8. Node `4` found. It has no children (Case 1).
9. Delete node 4, return `nullptr`.
10. Node 6's left becomes `nullptr`.
11. Return to root (originally 3, now 4). Its right child is updated to the modified subtree (6).

## ⚠️ Common Interview Mistakes
- **Ignoring the Global Property:** Checking only `left < root < right` for immediate children, forgetting that *every* node in the left subtree must be less than the root.
- **Incorrect Deletion (Two Children):** Not correctly linking the tree back up after deleting the successor node.
- **Memory Leaks:** Forgetting to actually `delete` the node in C++ when returning the new child in Cases 1 and 2.
- **Assuming $O(\log N)$ always:** Forgetting that a badly formed BST (inserted in sorted order) devolves into a linked list, making operations $O(N)$.

## 📊 Complexity Analysis
- **Time Complexity:** 
  - **Balanced BST:** $O(\log N)$ for Search, Insert, and Delete. At each step, we eliminate half the tree.
  - **Skewed BST (Worst Case):** $O(N)$ for Search, Insert, and Delete. The tree is essentially a linked list.
- **Space Complexity:** 
  - $O(H)$ auxiliary stack space for recursion, where $H$ is the height of the tree. $O(\log N)$ in best/average case, $O(N)$ in worst case.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: [Conceptual] Why do we replace a node having two children with its Inorder Successor (or Predecessor) when deleting?
**Answer:** The inorder successor is the smallest element that is strictly greater than the node. Replacing the node with its successor guarantees that the BST property is maintained: the new value will still be strictly greater than everything in the left subtree, and strictly less than or equal to everything remaining in the right subtree. The same logic applies to the inorder predecessor.

### Q2: [Output Prediction] What happens if we insert a sorted array into a standard BST?
**Answer:** The BST will become entirely right-skewed (a linked list), because every newly inserted element will be greater than the root and placed as a right child continuously. Operations will degrade from $O(\log N)$ to $O(N)$. This is why self-balancing trees like AVL or Red-Black trees are needed.

### Q3: [Variant] How would you find the inorder successor without a parent pointer?
**Answer:** Start at the root. If the target node has a right subtree, the successor is the minimum value in that right subtree. If it does not, the successor is the lowest ancestor whose left child is also an ancestor of the target node. We can find this by traversing from the root and keeping track of the last node where we took a left turn to reach the target.

### Q4: [Conceptual] Can you build a unique BST from just its Inorder traversal?
**Answer:** No. An inorder traversal of any BST yields a sorted sequence. Multiple structurally different BSTs can produce the same sorted sequence (e.g., a balanced tree vs. a skewed tree). You need at least one more traversal (like Preorder or Postorder) to uniquely reconstruct it.

### Q5: [Complexity] In a BST, how many nodes does the inorder successor of a node (with two children) have in its left subtree?
**Answer:** Zero. If the inorder successor had a left child, that left child would be strictly smaller than the successor, making the left child the actual successor instead. Thus, the inorder successor (when found in the right subtree) can never have a left child.

### Q6: [Conceptual] Why is an Inorder Traversal of a BST sorted?
**Answer:** By definition, a BST places smaller elements to the left and larger elements to the right. The Inorder traversal specifically visits the Left subtree (all smaller elements), then the Root (the middle element), then the Right subtree (all larger elements). Recursively, this mathematically guarantees ascending order.

## 🏆 Related Problems (Leetcode)
- **Leetcode 700:** Search in a Binary Search Tree (Easy)
- **Leetcode 701:** Insert into a Binary Search Tree (Medium)
- **Leetcode 450:** Delete Node in a BST (Medium) - *Direct application of the 3-case deletion logic*
- **Leetcode 285:** Inorder Successor in BST (Medium)

## 🔗 Cross-Topic Connections
- **Binary Search:** Searching in a BST is exactly the tree-equivalent of Binary Search on a sorted array.
- **Sorting:** Inorder traversal of a BST is basically Tree Sort ($O(N \log N)$ time if balanced).
- **Heaps:** While both are trees, a BST is globally sorted horizontally, whereas a Heap is only sorted vertically (parent > child). A BST supports $O(\log N)$ search for *any* element, a Heap only supports $O(1)$ search for the min/max element.

## ⚡ 2-Minute Revision Flash Card
- **Invariant:** Left subtree < Root < Right subtree (holds for all nodes).
- **Search/Insert:** Follow the property down the tree. $O(\log N)$ average, $O(N)$ worst.
- **Delete Case 1:** No children. Delete the node, return null.
- **Delete Case 2:** One child. Return the non-null child to the parent.
- **Delete Case 3:** Two children. Find `min(root->right)`, swap values, recursively delete the successor from the right subtree.
- **Traversal:** Inorder traversal *always* gives a sorted array.
