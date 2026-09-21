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

## 🔵 Complete $O(1)$ Space Implementation

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
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(1)$ auxiliary memory.
