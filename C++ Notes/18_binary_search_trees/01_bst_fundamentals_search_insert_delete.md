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
- **Time Complexity:** $O(H)$ for search, insert, and delete ($O(\log N)$ balanced, $O(N)$ skewed).
