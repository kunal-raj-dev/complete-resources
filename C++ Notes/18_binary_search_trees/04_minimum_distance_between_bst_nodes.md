# Lecture 101: Minimum Absolute Difference in BST (LeetCode 783)

> **One-Line Purpose:** Find minimum distance between any two BST nodes using state-preserving inorder traversal.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #101  
> **Video ID:** `WZmjRXF_Zi4`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=WZmjRXF_Zi4)  
> **Duration:** 14:16  
> **Status:** AUDITED  

---

## 🔵 Implementation

```cpp
#include <algorithm>
#include <climits>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionMinDiff {
private:
    int minDiff = INT_MAX;
    TreeNode* prev = nullptr;

    void inorder(TreeNode* root) {
        if (!root) return;

        inorder(root->left);

        if (prev) {
            minDiff = min(minDiff, root->val - prev->val);
        }
        prev = root;

        inorder(root->right);
    }

public:
    int minDiffInBST(TreeNode* root) {
        minDiff = INT_MAX;
        prev = nullptr;
        inorder(root);
        return minDiff;
    }
};
```
