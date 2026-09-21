# Lecture 105: Merge Two Binary Search Trees

> **One-Line Purpose:** Merge two arbitrary BSTs into a single balanced BST in $O(M + N)$ time via inorder extraction and two-pointer array merging.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #105  
> **Video ID:** `AiKZjCuy2k4`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=AiKZjCuy2k4)  
> **Duration:** 16:39  
> **Status:** AUDITED  

---

## 🔵 Algorithmic Flow & Implementation

1. Extract Inorder of BST 1 ($O(N)$).
2. Extract Inorder of BST 2 ($O(M)$).
3. Merge sorted arrays using two pointers ($O(N + M)$).
4. Construct balanced BST from merged array ($O(N + M)$).

```cpp
#include <vector>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

void getInorder(TreeNode* root, vector<int>& arr) {
    if (!root) return;
    getInorder(root->left, arr);
    arr.push_back(root->val);
    getInorder(root->right, arr);
}

TreeNode* sortedArrayToBST(const vector<int>& nums, int left, int right) {
    if (left > right) return nullptr;
    int mid = left + (right - left) / 2;
    TreeNode* root = new TreeNode(nums[mid]);
    root->left = sortedArrayToBST(nums, left, mid - 1);
    root->right = sortedArrayToBST(nums, mid + 1, right);
    return root;
}

TreeNode* mergeBSTs(TreeNode* root1, TreeNode* root2) {
    vector<int> a1, a2, merged;
    getInorder(root1, a1);
    getInorder(root2, a2);

    int i = 0, j = 0;
    while (i < a1.size() && j < a2.size()) {
        if (a1[i] <= a2[j]) merged.push_back(a1[i++]);
        else merged.push_back(a2[j++]);
    }
    while (i < a1.size()) merged.push_back(a1[i++]);
    while (j < a2.size()) merged.push_back(a2[j++]);

    return sortedArrayToBST(merged, 0, merged.size() - 1);
}
```
- **Total Time Complexity:** $O(N + M)$.
- **Space Complexity:** $O(N + M)$.
