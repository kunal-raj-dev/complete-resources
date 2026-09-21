# Lecture 107: Largest BST in Binary Tree

> **One-Line Purpose:** Identify the maximum number of nodes in any subtree that strictly satisfies BST validity using bottom-up postorder propagation.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #107  
> **Video ID:** `Pr-HFxp7npk`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=Pr-HFxp7npk)  
> **Duration:** 24:56  
> **Status:** AUDITED  

---

## 🔵 Complete C++ Implementation

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

struct NodeInfo {
    bool isBST;
    int size;
    int minVal;
    int maxVal;
};

class SolutionLargestBST {
private:
    int maxBSTSize = 0;

    NodeInfo solve(TreeNode* root) {
        if (!root) {
            return {true, 0, INT_MAX, INT_MIN};
        }

        NodeInfo left = solve(root->left);
        NodeInfo right = solve(root->right);

        NodeInfo curr;
        curr.size = 1 + left.size + right.size;

        if (left.isBST && right.isBST && root->val > left.maxVal && root->val < right.minVal) {
            curr.isBST = true;
            curr.minVal = min(root->val, left.minVal);
            curr.maxVal = max(root->val, right.maxVal);
            maxBSTSize = max(maxBSTSize, curr.size);
        } else {
            curr.isBST = false;
            curr.minVal = INT_MIN;
            curr.maxVal = INT_MAX;
        }

        return curr;
    }

public:
    int largestBST(TreeNode* root) {
        maxBSTSize = 0;
        solve(root);
        return maxBSTSize;
    }
};
```
- **Time Complexity:** $O(N)$ — Every node visited once in bottom-up postorder.
- **Space Complexity:** $O(H)$.
