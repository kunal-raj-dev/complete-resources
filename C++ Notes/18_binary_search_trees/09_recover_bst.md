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

## 🔵 Complete C++ Implementation

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
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(H)$ stack space ($O(1)$ if Morris traversal is used).
