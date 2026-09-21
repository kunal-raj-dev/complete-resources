# Lecture 100: Validate Binary Search Tree (LeetCode 98)

> **One-Line Purpose:** Validate BST correctness via range propagation `(minAllowed, maxAllowed)` with 64-bit boundaries.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #100  
> **Video ID:** `dSBcCynP1nA`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=dSBcCynP1nA)  
> **Duration:** 12:41  
> **Status:** AUDITED  

---

## 🔵 Complete C++ Implementation

```cpp
#include <climits>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionValidateBST {
private:
    bool validate(TreeNode* root, long long minVal, long long maxVal) {
        if (!root) return true;

        if (root->val <= minVal || root->val >= maxVal) {
            return false;
        }

        return validate(root->left, minVal, root->val) &&
               validate(root->right, root->val, maxVal);
    }

public:
    bool isValidBST(TreeNode* root) {
        return validate(root, LLONG_MIN, LLONG_MAX);
    }
};
```
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(H)$.
