# Lecture 94: Binary Tree Paths (LeetCode 257)

> **One-Line Purpose:** Collect all root-to-leaf paths as formatted strings using depth-first search backtracking.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #94  
> **Video ID:** `AWJD__CfM6A`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=AWJD__CfM6A)  
> **Duration:** 10:01  
> **Status:** AUDITED  

---

## 🔵 Implementation

```cpp
#include <vector>
#include <string>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionPaths {
private:
    void dfs(TreeNode* root, string path, vector<string>& paths) {
        if (!root) return;

        path += to_string(root->val);

        // Leaf node reached
        if (!root->left && !root->right) {
            paths.push_back(path);
            return;
        }

        path += "->";
        dfs(root->left, path, paths);
        dfs(root->right, path, paths);
    }

public:
    vector<string> binaryTreePaths(TreeNode* root) {
        vector<string> paths;
        dfs(root, "", paths);
        return paths;
    }
};
```
