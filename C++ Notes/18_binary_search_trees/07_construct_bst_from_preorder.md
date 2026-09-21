# Lecture 104: Construct BST from Preorder Traversal (LeetCode 1008)

> **One-Line Purpose:** Construct a BST from preorder values in linear $O(N)$ time by maintaining upper bounds.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #104  
> **Video ID:** `-n5Ur1wE5Jc`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=-n5Ur1wE5Jc)  
> **Duration:** 19:10  
> **Status:** AUDITED  

---

## 🔵 Optimal $O(N)$ Upper-Bound Implementation

```cpp
#include <vector>
#include <climits>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionBstFromPreorder {
private:
    int idx = 0;

    TreeNode* build(const vector<int>& preorder, int bound) {
        if (idx >= preorder.size() || preorder[idx] > bound) {
            return nullptr;
        }

        TreeNode* root = new TreeNode(preorder[idx++]);
        root->left = build(preorder, root->val);
        root->right = build(preorder, bound);

        return root;
    }

public:
    TreeNode* bstFromPreorder(vector<int>& preorder) {
        idx = 0;
        return build(preorder, INT_MAX);
    }
};
```
- **Time Complexity:** $O(N)$. Space Complexity: $O(H)$.
