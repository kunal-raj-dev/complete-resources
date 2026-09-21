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

## 🎯 Learning Objectives
- Understand why a standard insert operation into an empty BST using a sorted array yields a heavily unbalanced (skewed) tree.
- Learn to build a height-balanced BST by utilizing the middle element of the sorted array as the root.
- Apply the divide-and-conquer paradigm to construct the left and right subtrees recursively.

## 🧠 Core Intuition — Why This Works
If you insert elements of a sorted array sequentially (`1, 2, 3, 4, 5`) into a BST, you get a straight line (a linked list), which is $O(N)$ for searches. 
To keep the tree **balanced** (depth of left and right subtrees differ by at most 1), the root must be the median of the data. 
In a sorted array, the median is simply the **middle element**. 
- Take the middle element, make it the root.
- All elements to its left are smaller (forms the left subtree).
- All elements to its right are larger (forms the right subtree).
- Recursively repeat this process for the left and right halves.

**Visualization:**
`Array: [-10, -3, 0, 5, 9]`

1. Middle is `0`. Root = `0`.
   `Left part: [-10, -3]` | `Right part: [5, 9]`
2. Middle of `[-10, -3]` is `-10`. Left child of `0` is `-10`.
3. Middle of `[5, 9]` is `5`. Right child of `0` is `5`.

Resulting BST:
```text
      0
     / \
  -10   5
    \    \
    -3    9
```

## 🎯 Pattern Recognition — When to Use This
**Trigger cues:**
- "Sorted array/list" + "Binary Search Tree" → **Middle element is root**
- "Convert X to balanced BST" → **Divide and conquer** using middle elements
- "Height balanced" constraint on tree construction.

## 📐 Algorithm Walk-Through
1. Define a helper function `build(left, right)`.
2. Base case: If `left > right`, return `nullptr` (empty subtree).
3. Find the midpoint: `mid = left + (right - left) / 2` (prevents integer overflow).
4. Create a new `TreeNode` with the value at `nums[mid]`.
5. Recursively build the left subtree using the left half: `build(left, mid - 1)`.
6. Recursively build the right subtree using the right half: `build(mid + 1, right)`.
7. Return the created node.

## 🔵 Complete C++ Implementation

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

## 🔍 Dry Run Trace
**Input:** `nums = [1, 2, 3]`
1. `build(0, 2)`:
   - `mid = 1`, `root = new TreeNode(nums[1]) -> 2`
   - `root->left = build(0, 0)`
   - `root->right = build(2, 2)`
2. `build(0, 0)` (left child of 2):
   - `mid = 0`, `node = new TreeNode(nums[0]) -> 1`
   - `node->left = build(0, -1) -> nullptr`
   - `node->right = build(1, 0) -> nullptr`
   - Returns node `1`.
3. `build(2, 2)` (right child of 2):
   - `mid = 2`, `node = new TreeNode(nums[2]) -> 3`
   - `node->left = build(2, 1) -> nullptr`
   - `node->right = build(3, 2) -> nullptr`
   - Returns node `3`.
4. Root `2` is connected to left `1` and right `3`. Returns root `2`.

## ⚠️ Common Interview Mistakes
- **Integer Overflow:** Calculating mid as `(left + right) / 2`. If `left` and `right` are huge, this overflows. Always use `left + (right - left) / 2`.
- **Wrong Base Case:** Using `left >= right` instead of `left > right`. `left == right` means there is one element left to process, it should not return `nullptr`.
- **Slicing Vectors:** Passing copies of sliced vectors instead of passing by reference with `left`/`right` indices. Slicing vectors repeatedly degrades time complexity to $O(N \log N)$ and space to $O(N \log N)$.

## 📊 Complexity Analysis
- **Time Complexity:** $O(N)$ where $N$ is the number of elements in the array. We visit every node exactly once to create it.
- **Space Complexity:** $O(\log N)$. The recursive call stack goes as deep as the height of the balanced tree, which is strictly $\log N$. (Excluding the space required for the output tree itself).

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: [Conceptual] Is the height-balanced BST created by this method unique?
**Answer:** Not necessarily. If the array has an even number of elements, you have two choices for the exact "middle" element (left-mid or right-mid). Both choices will yield a perfectly valid, height-balanced BST, but the structures will be slightly different.

### Q2: [Time Complexity] Why is the time complexity $O(N)$ and not $O(N \log N)$?
**Answer:** Although it looks like binary search (which divides by 2), we are not discarding half of the array at each step. We are recursively visiting *both* halves. The recurrence relation is $T(N) = 2T(N/2) + O(1)$, which by the Master Theorem resolves to $O(N)$. We do $O(1)$ work per element exactly once.

### Q3: [Variant] How would this change if the input was a Sorted Linked List instead of an Array?
**Answer:** A linked list doesn't support $O(1)$ random access to the middle element. You have two options:
1. Fast/Slow pointer to find the middle ($O(N \log N)$ time, $O(\log N)$ space).
2. (Optimal) Inorder simulation: Count the length $N$. Recursively build the left half, *then* create the root using the current list head, advance the list head, *then* build the right half. This runs in $O(N)$ time and $O(\log N)$ space without converting the list to an array first.

### Q4: [Edge Case] What happens if there are duplicate elements in the sorted array?
**Answer:** This algorithm still works perfectly. It will place one of the duplicates as the parent of the other. However, standard BST definitions often disallow duplicates. If duplicates are allowed, the condition $\text{Left} \le \text{Root} < \text{Right}$ (or similar) will naturally be maintained by the midpoint split.

## 🏆 Related Problems (Leetcode)
- **Leetcode 108:** Convert Sorted Array to Binary Search Tree (Easy)
- **Leetcode 109:** Convert Sorted List to Binary Search Tree (Medium)
- **Leetcode 1382:** Balance a Binary Search Tree (Medium)

## 🔗 Cross-Topic Connections
- **Divide & Conquer:** This is a classic divide-and-conquer algorithm, structurally identical to the merge step breakdown in Merge Sort.
- **Binary Search:** The midpoint logic is directly lifted from Binary Search.

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Sorted array to balanced BST.
- **Root:** Always choose the middle element `mid = left + (right - left) / 2`.
- **Recursion:** Left child = `build(left, mid - 1)`, Right child = `build(mid + 1, right)`.
- **Base Case:** `if (left > right) return nullptr;`.
- **Performance:** $O(N)$ Time, $O(\log N)$ Space (due to recursive call stack).
- **Beware:** Do not slice arrays; pass by reference with index boundaries.
