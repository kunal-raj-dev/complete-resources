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

## 🎯 Learning Objectives
- Use the Inorder property of a BST to extract elements in sorted order.
- Merge two sorted arrays efficiently using the classic Two-Pointer technique.
- Reconstruct a balanced BST from a sorted array using Divide and Conquer.

## 🧠 Core Intuition — Why This Works
If you just take two BSTs and try to insert the nodes of one into the other, you might end up with a highly skewed tree (worst case $O(N \times M)$ time).
Instead, we break the problem down into three foolproof, linear-time steps:
1. **Flatten to Arrays:** Since an inorder traversal of a BST gives a sorted array, we can turn both trees into two sorted arrays.
2. **Merge Arrays:** Merging two sorted arrays into one sorted array is a classic $O(N+M)$ operation (like the merge step in Merge Sort).
3. **Build Balanced Tree:** Given a sorted array, the middle element is the perfect root. The left half forms the left subtree, and the right half forms the right subtree. Repeating this recursively guarantees a perfectly balanced BST!

**Visualization:**
```text
Tree 1:       Tree 2:
  2             3
 / \           / \
1   4         0   5

1. Inorder 1: [1, 2, 4]
2. Inorder 2: [0, 3, 5]
3. Merged:    [0, 1, 2, 3, 4, 5]
4. Build Balanced BST from Merged:
      Mid is 2 (index 2)
           2
         /   \
        0     4
         \   / \
          1 3   5
```

## 🎯 Pattern Recognition — When to Use This
**Trigger cues:**
- "Merge two BSTs"
- "Combine binary search trees into a balanced tree"
→ **Action:** Inorder extraction $\rightarrow$ Two-pointer merge $\rightarrow$ Sorted array to balanced BST.

## 📐 Algorithm Walk-Through
1. **Step 1:** Call `getInorder` on `root1` to populate vector `a1`.
2. **Step 2:** Call `getInorder` on `root2` to populate vector `a2`.
3. **Step 3 (Merge):** 
   - Initialize pointers `i = 0` and `j = 0`.
   - While `i < a1.size()` and `j < a2.size()`, push the smaller element to `merged` and increment its pointer.
   - Flush remaining elements from `a1` or `a2`.
4. **Step 4 (Construct):**
   - Call `sortedArrayToBST(merged, 0, merged.size() - 1)`.
   - In `sortedArrayToBST`: `mid = left + (right - left) / 2`.
   - `root = new TreeNode(nums[mid])`.
   - `root->left = sortedArrayToBST(left, mid - 1)`.
   - `root->right = sortedArrayToBST(mid + 1, right)`.
   - Return `root`.

## 💻 Complete C++ Implementation

```cpp
#include <vector>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionMergeBST {
private:
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

public:
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
};
```

## 🔍 Dry Run Trace
**Tree 1:** `[2, 1, 3]`, **Tree 2:** `[4]`
- `a1`: `[1, 2, 3]`
- `a2`: `[4]`
- `merged`: `[1, 2, 3, 4]`
- `sortedArrayToBST([1, 2, 3, 4], 0, 3)`
  - `mid = 1` (value 2). Root is 2.
  - `root->left = build(0, 0)` $\rightarrow$ `mid = 0` (value 1). Leaf 1.
  - `root->right = build(2, 3)` $\rightarrow$ `mid = 2` (value 3). Root 3.
    - `root->left = build(2, 1)` $\rightarrow$ null.
    - `root->right = build(3, 3)` $\rightarrow$ `mid = 3` (value 4). Leaf 4.
- Returns tree: `[2, 1, 3, null, null, null, 4]`.

## ⚠️ Common Interview Mistakes
- **Doing naive insertions:** Traversing one tree and calling `insert()` on the other tree. This is $O(M \log N)$ if balanced, but $O(M \times N)$ if skewed, and it doesn't guarantee the final tree will be balanced.
- **Sorting the merged array with `std::sort`:** After dumping both inorders into a single array, some candidates call `sort(merged.begin(), merged.end())`. This is $O((N+M) \log (N+M))$, which is suboptimal compared to the $O(N+M)$ two-pointer merge.

## 📊 Complexity Analysis
- **Time Complexity:** $O(N + M)$ to extract arrays, merge them, and build the tree.
- **Space Complexity:** $O(N + M)$ to store the arrays `a1`, `a2`, and `merged`, plus the recursion stack of $O(\log(N+M))$ for tree construction.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: [Optimization] Can we do this in $O(H_1 + H_2)$ space instead of $O(N + M)$ space?
**Answer:** Yes, but it requires destroying the original trees. We can convert both BSTs into sorted Doubly Linked Lists in-place using $O(H)$ space. Then, we merge the two sorted doubly linked lists in $O(1)$ auxiliary space. Finally, we convert the merged doubly linked list back into a balanced BST in-place. The total time remains $O(N+M)$, but auxiliary space drops to $O(H_1 + H_2)$.

### Q2: [Logic] Why do we pick `mid = left + (right - left) / 2` instead of just `(left + right) / 2`?
**Answer:** While `(left + right) / 2` works for small arrays, it causes Integer Overflow if `left` and `right` are huge (close to `INT_MAX`). `left + (right - left) / 2` prevents overflow and is the industry standard for calculating midpoints.

### Q3: [Variant] What if the trees contain duplicate values?
**Answer:** The current code handles duplicates safely. `a1[i] <= a2[j]` ensures stability. The generated BST will have duplicates correctly placed in the left or right subtree depending on the implementation of `sortedArrayToBST` (here, left bound is `mid - 1`, meaning duplicates could go to either side based on the exact index).

## 🏆 Related Problems (Leetcode)
- **Leetcode 108:** Convert Sorted Array to Binary Search Tree
- **Leetcode 88:** Merge Sorted Array
- **Leetcode 1305:** All Elements in Two Binary Search Trees

## 🔗 Cross-Topic Connections
- **Merge Sort:** The array merging step is literally the "Merge" routine from Merge Sort.

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Merge 2 BSTs into a balanced BST optimally.
- **Approach:** 
  1. Inorder 1 $\rightarrow$ Array 1
  2. Inorder 2 $\rightarrow$ Array 2
  3. Merge Array 1 and Array 2 (Two Pointers)
  4. Array to BST (Mid is root, recurse left/right)
- **Time/Space:** $O(N+M)$ Time, $O(N+M)$ Space.
- **Bonus:** Can be done in $O(H)$ space using In-place DLL conversion.
