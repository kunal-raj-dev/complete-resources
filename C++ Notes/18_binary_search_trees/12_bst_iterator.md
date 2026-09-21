# Lecture 109: BST Iterator (LeetCode 173)

> **One-Line Purpose:** Implement controlled lazy inorder BST traversal supporting `next()` and `hasNext()` in $O(1)$ amortized time and $O(H)$ space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #109  
> **Video ID:** `dS1bKglre3A`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=dS1bKglre3A)  
> **Duration:** 17:16  
> **Status:** AUDITED  

---

## 🔵 Complete C++ Implementation

```cpp
#include <stack>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class BSTIterator {
private:
    stack<TreeNode*> st;

    void pushAllLeft(TreeNode* node) {
        while (node) {
            st.push(node);
            node = node->left;
        }
    }

public:
    BSTIterator(TreeNode* root) {
        pushAllLeft(root);
    }

    int next() {
        TreeNode* topNode = st.top();
        st.pop();
        if (topNode->right) {
            pushAllLeft(topNode->right);
        }
        return topNode->val;
    }

    bool hasNext() {
        return !st.empty();
    }
};
```
- **Time Complexity:** `hasNext()` is $O(1)$; `next()` is amortized $O(1)$ (each node pushed and popped once).
- **Space Complexity:** $O(H)$ stack space where $H$ is the tree height.
