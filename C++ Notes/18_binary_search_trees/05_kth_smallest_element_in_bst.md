# Lecture 102: Kth Smallest Element in BST (LeetCode 230)

> **One-Line Purpose:** Retrieve the Kth smallest element in $O(H + K)$ time via early-terminating inorder traversal.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #102  
> **Video ID:** `Kq4BbvIhj44`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=Kq4BbvIhj44)  
> **Duration:** 12:43  
> **Status:** AUDITED  

---

## 🔵 Implementation

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionKthSmallest {
private:
    int result = -1;
    int count = 0;

    void inorder(TreeNode* root, int k) {
        if (!root || count >= k) return;

        inorder(root->left, k);

        count++;
        if (count == k) {
            result = root->val;
            return;
        }

        inorder(root->right, k);
    }

public:
    int kthSmallest(TreeNode* root, int k) {
        count = 0;
        inorder(root, k);
        return result;
    }
};
```
