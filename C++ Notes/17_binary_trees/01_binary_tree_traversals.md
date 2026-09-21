# Lecture 85: Binary Trees Traversal: Preorder, Inorder, Postorder & Level Order

> **One-Line Purpose:** Master binary tree representations and foundational traversal orders (DFS: Preorder, Inorder, Postorder; BFS: Level Order) with stack and queue mechanics.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #85  
> **Video ID:** `eKJrXBCRuNQ`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=eKJrXBCRuNQ)  
> **Duration:** 01:14:15  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

- Binary tree node anatomy in C++ (`data`, `left`, `right`).
- Recursive DFS Traversals:
  - **Preorder:** `Root -> Left -> Right`
  - **Inorder:** `Left -> Root -> Right`
  - **Postorder:** `Left -> Right -> Root`
- Breadth-First Search (BFS) / Level Order Traversal using `std::queue`.

---

## 🔵 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <queue>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

// 1. Preorder Traversal (Root, Left, Right)
void preorder(TreeNode* root) {
    if (!root) return;
    cout << root->val << " ";
    preorder(root->left);
    preorder(root->right);
}

// 2. Inorder Traversal (Left, Root, Right)
void inorder(TreeNode* root) {
    if (!root) return;
    inorder(root->left);
    cout << root->val << " ";
    inorder(root->right);
}

// 3. Postorder Traversal (Left, Right, Root)
void postorder(TreeNode* root) {
    if (!root) return;
    postorder(root->left);
    postorder(root->right);
    cout << root->val << " ";
}

// 4. Level Order Traversal (BFS)
vector<vector<int>> levelOrder(TreeNode* root) {
    vector<vector<int>> result;
    if (!root) return result;

    queue<TreeNode*> q;
    q.push(root);

    while (!q.empty()) {
        int levelSize = q.size();
        vector<int> currentLevel;

        for (int i = 0; i < levelSize; i++) {
            TreeNode* curr = q.front();
            q.pop();
            currentLevel.push_back(curr->val);

            if (curr->left) q.push(curr->left);
            if (curr->right) q.push(curr->right);
        }
        result.push_back(currentLevel);
    }
    return result;
}
```
- **Time Complexity:** $O(N)$ for all traversals.
- **Space Complexity:** $O(H)$ call stack for DFS ($O(N)$ worst, $O(\log N)$ balanced); $O(W)$ queue for BFS ($W \le N/2$ leaf level).
