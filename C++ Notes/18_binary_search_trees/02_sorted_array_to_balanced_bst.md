# Lecture 99: Sorted Array to Balanced BST (LeetCode 108)

> **One-Line Purpose:** Convert a sorted array into a height-balanced BST in $O(N)$ time by recursively picking midpoint roots.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #99  
> **Video ID:** `0s6sCjs_4g0`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=0s6sCjs_4g0)  
> **Duration:** 08:44  
> **Status:** AUDITED  

---

## 🔵 Implementation

```cpp
#include <vector>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionSortedArrayToBST {
private:
    TreeNode* build(const vector<int>& nums, int left, int right) {
        if (left > right) return nullptr;

        int mid = left + (right - left) / 2;
        TreeNode* root = new TreeNode(nums[mid]);

        root->left = build(nums, left, mid - 1);
        root->right = build(nums, mid + 1, right);

        return root;
    }

public:
    TreeNode* sortedArrayToBST(vector<int>& nums) {
        return build(nums, 0, nums.size() - 1);
    }
};
```
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(\log N)$ stack depth.
