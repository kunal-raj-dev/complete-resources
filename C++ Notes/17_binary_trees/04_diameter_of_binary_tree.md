# Lecture 88: Diameter of Binary Tree (LeetCode 543)

> **One-Line Purpose:** Compute the longest path between any two nodes in a binary tree in optimal $O(N)$ time by combining height calculation with diameter updates.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #88  
> **Video ID:** `aPyDPImR5UM`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=aPyDPImR5UM)  
> **Duration:** 19:29  
> **Status:** AUDITED  

---

## 🔵 Optimal $O(N)$ Implementation

```cpp
#include <algorithm>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionDiameter {
private:
    int maxDiameter = 0;

    int calculateHeight(TreeNode* root) {
        if (!root) return 0;

        int leftH = calculateHeight(root->left);
        int rightH = calculateHeight(root->right);

        // Longest path passing through current root is leftH + rightH
        maxDiameter = max(maxDiameter, leftH + rightH);

        return 1 + max(leftH, rightH);
    }

public:
    int diameterOfBinaryTree(TreeNode* root) {
        maxDiameter = 0;
        calculateHeight(root);
        return maxDiameter;
    }
};
```
- **Time Complexity:** $O(N)$ — Single postorder traversal.
- **Space Complexity:** $O(H)$ auxiliary stack.
