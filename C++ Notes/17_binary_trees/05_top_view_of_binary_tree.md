# Lecture 89: Top View of a Binary Tree

> **One-Line Purpose:** Generate the vertical projection of a binary tree using horizontal distance coordinate mapping and BFS level order.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #89  
> **Video ID:** `FGr-syrhvOA`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=FGr-syrhvOA)  
> **Duration:** 19:39  
> **Status:** AUDITED  

---

## 🔵 Complete C++ Implementation

```cpp
#include <vector>
#include <map>
#include <queue>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

vector<int> topView(TreeNode* root) {
    vector<int> ans;
    if (!root) return ans;

    // map: <horizontal_distance, node_value>
    map<int, int> topNodeMap;
    // queue: <TreeNode*, horizontal_distance>
    queue<pair<TreeNode*, int>> q;

    q.push({root, 0});

    while (!q.empty()) {
        auto [curr, hd] = q.front();
        q.pop();

        // If horizontal distance hd seen for the first time, record it
        if (topNodeMap.find(hd) == topNodeMap.end()) {
            topNodeMap[hd] = curr->val;
        }

        if (curr->left) q.push({curr->left, hd - 1});
        if (curr->right) q.push({curr->right, hd + 1});
    }

    for (auto const& [hd, val] : topNodeMap) {
        ans.push_back(val);
    }
    return ans;
}
```
- **Time Complexity:** $O(N \log N)$ due to `std::map` ordering ($O(N)$ with `unordered_map` + min/max tracking).
- **Space Complexity:** $O(N)$.
