# Lecture 96: Morris Inorder Traversal: $O(1)$ Auxiliary Space

> **One-Line Purpose:** Perform complete Inorder tree traversal in $O(N)$ time and strict $O(1)$ auxiliary memory by constructing temporary predecessor threads.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #96  
> **Video ID:** `PUfADhkq1LI`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=PUfADhkq1LI)  
> **Duration:** 17:52  
> **Status:** AUDITED  

---

## 🔵 Complete C++ Implementation

```cpp
#include <vector>
#include <iostream>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

vector<int> morrisInorder(TreeNode* root) {
    vector<int> inorder;
    TreeNode* curr = root;

    while (curr) {
        if (!curr->left) {
            inorder.push_back(curr->val);
            curr = curr->right;
        } else {
            // Find inorder predecessor (rightmost node in left subtree)
            TreeNode* prev = curr->left;
            while (prev->right && prev->right != curr) {
                prev = prev->right;
            }

            if (!prev->right) {
                // Thread creation: Link predecessor back to current
                prev->right = curr;
                curr = curr->left;
            } else {
                // Thread removal: Thread already exists, sever it
                prev->right = nullptr;
                inorder.push_back(curr->val);
                curr = curr->right;
            }
        }
    }

    return inorder;
}
```
- **Time Complexity:** $O(N)$ amortized (each edge traversed at most 3 times).
- **Space Complexity:** $O(1)$ strictly — No recursion call stack, no queue, no explicit stack!
