# Lecture 92: Build Tree from Preorder & Inorder (LeetCode 105)

> **One-Line Purpose:** Reconstruct a unique binary tree from preorder root order and inorder boundary splitting with hash table index lookups.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #92  
> **Video ID:** `33b1M980cCA`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=33b1M980cCA)  
> **Duration:** 20:59  
> **Status:** AUDITED  

---

## 🔵 Complete C++ Implementation

```cpp
#include <vector>
#include <unordered_map>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionBuildTree {
private:
    unordered_map<int, int> inMap;
    int preIdx = 0;

    TreeNode* construct(const vector<int>& preorder, int inStart, int inEnd) {
        if (inStart > inEnd) return nullptr;

        int rootVal = preorder[preIdx++];
        TreeNode* root = new TreeNode(rootVal);

        int rootPos = inMap[rootVal];

        root->left = construct(preorder, inStart, rootPos - 1);
        root->right = construct(preorder, rootPos + 1, inEnd);

        return root;
    }

public:
    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        inMap.clear();
        preIdx = 0;
        for (int i = 0; i < inorder.size(); i++) {
            inMap[inorder[i]] = i;
        }
        return construct(preorder, 0, inorder.size() - 1);
    }
};
```
- **Time Complexity:** $O(N)$ with hash map lookups.
- **Space Complexity:** $O(N)$ map + recursion stack.
