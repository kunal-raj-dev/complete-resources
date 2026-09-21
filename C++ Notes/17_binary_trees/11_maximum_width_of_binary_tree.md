# Lecture 95: Maximum Width of Binary Tree (LeetCode 662)

> **One-Line Purpose:** Calculate maximum horizontal tree width using 0-based heap indices with level-offset normalization to avoid 64-bit integer overflow.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #95  
> **Video ID:** `rhz-csskg_A`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=rhz-csskg_A)  
> **Duration:** 21:09  
> **Status:** AUDITED  

---

## 🔵 Complete C++ Overflow-Safe Implementation

```cpp
#include <queue>
#include <algorithm>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionWidth {
public:
    int widthOfBinaryTree(TreeNode* root) {
        if (!root) return 0;
        unsigned long long maxWidth = 0;

        queue<pair<TreeNode*, unsigned long long>> q;
        q.push({root, 0});

        while (!q.empty()) {
            int size = q.size();
            unsigned long long minIdx = q.front().second; // Offset for current level
            unsigned long long first = 0, last = 0;

            for (int i = 0; i < size; i++) {
                auto [node, curIdx] = q.front();
                q.pop();

                // Normalize index by subtracting minimum index of this level
                unsigned long long normIdx = curIdx - minIdx;
                if (i == 0) first = normIdx;
                if (i == size - 1) last = normIdx;

                if (node->left) q.push({node->left, 2 * normIdx + 1});
                if (node->right) q.push({node->right, 2 * normIdx + 2});
            }

            maxWidth = max(maxWidth, last - first + 1);
        }

        return (int)maxWidth;
    }
};
```
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(W)$.
