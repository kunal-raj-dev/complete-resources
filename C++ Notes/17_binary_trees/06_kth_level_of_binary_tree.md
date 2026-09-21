# Lecture 90: Kth Level of a Binary Tree

> **One-Line Purpose:** Retrieve or print all nodes at depth $K$ using DFS recursive level counters or BFS queue batching.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #90  
> **Video ID:** `ze4JO_ODl3w`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=ze4JO_ODl3w)  
> **Duration:** 07:59  
> **Status:** AUDITED  

---

## 🔵 Implementation (DFS Method)

```cpp
#include <vector>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

void getKthLevel(TreeNode* root, int k, vector<int>& res) {
    if (!root || k < 1) return;
    if (k == 1) {
        res.push_back(root->val);
        return;
    }
    getKthLevel(root->left, k - 1, res);
    getKthLevel(root->right, k - 1, res);
}
```
- **Time Complexity:** $O(N)$. Space Complexity: $O(H)$.
