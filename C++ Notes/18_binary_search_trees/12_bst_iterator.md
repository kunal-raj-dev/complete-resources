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

## 1. 🧱 Prerequisite Concepts
- **Inorder Traversal:** Visiting a BST in Left-Root-Right order yields elements in sorted (ascending) order.
- **Iterative Tree Traversal:** Using an explicit Stack to mimic the call stack of a recursive function.
- **Amortized Time Complexity:** An operation might occasionally be slow, but on average across a sequence of operations, it's fast (e.g., $O(1)$).

## 2. 🧠 Core Concept & Explanation
A naive approach to implement a BST Iterator is to just do a full Inorder Traversal and store the result in an array. `next()` just returns the next array element in $O(1)$ time. But what about space? The array takes $O(N)$ space.
What if we only need the first 3 elements of a massive tree? A full traversal is a huge waste!

The optimal approach is to **simulate recursion step-by-step using a Custom Stack**. 
In standard recursion, when you visit a node, you immediately dive deep down its left side. We do exactly this: we keep pushing `node->left` to our stack until we hit `null`.
The `top` of the stack is now our *smallest available element*. When the user calls `next()`, we pop it. Before returning it, if this node has a right child, we must explore its right subtree. How? By treating its `right` child as a brand new root, diving deep down *its* left side, and stacking them up!

## 3. 🚶‍♂️ Step-by-step Approach (Algorithm)
1. **State:** Maintain a stack `st` of `TreeNode*`.
2. **Helper Function `pushAllLeft(node)`:** Takes a node, and pushes it and all its continuous left children into the stack.
3. **Constructor `BSTIterator(root)`:** Call `pushAllLeft(root)` to initialize the stack with the path to the absolute smallest element.
4. **`hasNext()`:** Simply return whether the stack is empty or not (`!st.empty()`).
5. **`next()`:** 
   - Extract the node at the top of the stack. This is the next element in sorted order.
   - Pop it from the stack.
   - If the extracted node has a right child, call `pushAllLeft(node->right)`. (This sets up the stack for future `next()` calls).
   - Return the extracted node's value.

## 4. 🔍 Dry Run / Execution Trace
Tree:
```text
       7
      / \
     3   15
        /  \
       9    20
```
- **Init:** `pushAllLeft(7)`. Stack pushes 7, then 3. Stack = `[7, 3]` (top is 3).
- **`next()` 1st call:**
  - Top is `3`. Pop it. Stack = `[7]`.
  - Node `3` has no right child. Nothing pushed.
  - Returns `3`.
- **`next()` 2nd call:**
  - Top is `7`. Pop it. Stack = `[]`.
  - Node `7` has a right child (`15`). `pushAllLeft(15)` pushes `15`, then `9`. Stack = `[15, 9]` (top is 9).
  - Returns `7`.
- **`next()` 3rd call:**
  - Top is `9`. Pop it. Stack = `[15]`.
  - Node `9` has no right child. Nothing pushed.
  - Returns `9`.

## 5. 💻 Complete C++ Implementation

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

## 6. ⏱️ Complexity Analysis
- **Time Complexity:** 
  - `hasNext()`: $O(1)$. Just checking stack emptiness.
  - `next()`: **Amortized** $O(1)$. Even though `pushAllLeft` has a `while` loop, across a full traversal, every node in the tree is pushed onto the stack exactly once and popped exactly once. $N$ pushes and $N$ pops over $N$ calls to `next()` averages to $O(1)$ per call.
- **Space Complexity:** $O(H)$ auxiliary stack space where $H$ is the tree height. In the worst-case (skewed tree), it's $O(N)$, but in a balanced BST, it's $O(\log N)$. This satisfies the requirement of an Iterator.

## 7. ⚠️ Edge Cases to Consider
- **Empty Tree:** The constructor should handle `root == nullptr` gracefully. Stack remains empty, `hasNext()` correctly returns false.
- **Right-Skewed Tree:** Initially only 1 element goes to stack. It dynamically loads only when needed.

## 8. ❌ Common Pitfalls & Mistakes
- **Pre-computing all elements ($O(N)$ Space Array):** A huge red flag in interviews. If the interviewer asks for an iterator, they want "lazy evaluation". Pre-computing is eager evaluation and wastes space.
- **Forgetting Amortized bounds:** An interviewer might point out the `while` loop in `next()` and ask "Isn't this $O(H)$ time?". You must confidently explain that it's $O(H)$ in the worst *single* call, but strictly amortized $O(1)$.

## 🎯 Pattern Recognition — When to Use This
- **Trigger Cues:** "Implement an iterator over a tree", "Next element in sorted order on demand", "Process BST elements dynamically without $O(N)$ space".
- **Why Custom Stack?** Any time an interviewer asks for "lazy evaluation" or an iterator, they are testing your ability to manually control a recursive traversal. By managing your own stack, you can pause and resume execution, achieving the required $O(H)$ space instead of aggressively flattening the tree.

## 🏆 Related Problems (Leetcode)
- **Leetcode 173. Binary Search Tree Iterator:** The exact problem.
- **Leetcode 230. Kth Smallest Element in a BST:** You can trivially solve this by calling `next()` exactly $K$ times using this iterator structure.
- **Leetcode 653. Two Sum IV - Input is a BST:** A classic application. You instantiate a forward iterator (Inorder) and a backward iterator (Reverse Inorder) and apply the standard Two-Pointer technique to find the sum in $O(N)$ time and $O(H)$ space!
- **Leetcode 284. Peeking Iterator:** A design extension where you wrap an existing iterator to support `peek()`.

## 🔗 Cross-Topic Connections
- **Design / OOP:** Implementing iterators is a fundamental Object-Oriented Design pattern. It abstracts the underlying tree structure from the user.
- **Stacks & Recursion:** A perfect example of converting implicit system call stacks into explicit dynamic memory stacks.

## 9. 💡 Expert Q&A / Interview Follow-ups
**Q1: Can we design an iterator to traverse backwards (Descending order)?**  
*Answer:* Yes! Simply reverse the logic: rename `pushAllLeft` to `pushAllRight`. Start by diving deep down the `right` path. In `next()`, if a right node is popped, check for its `left` child and `pushAllRight` on it.

**Q2: What if the BST is modified (insertions/deletions) while iterating?**  
*Answer:* As currently designed, structural modifications that alter the nodes currently in the stack (or subtrees we haven't visited yet) could corrupt the traversal. This is identical to a `ConcurrentModificationException` in Java. We would need a versioning mechanism or tree-locks to make it thread-safe.

**Q3: Does this logic work for a regular Binary Tree, or only a BST?**  
*Answer:* The code actually performs a generic Iterator for standard Inorder Traversal! It works for *any* Binary Tree. However, only in a BST does it guarantee that the returned values are sorted.

**Q4: How do you mathematically prove that `next()` is amortized $O(1)$?**
*Answer:* Across a full iteration of $N$ nodes, every single node in the tree is pushed onto the stack exactly once (during some `pushAllLeft` call) and popped exactly once (inside `next()`). That is $2N$ stack operations spread over $N$ calls to `next()`. Thus, the average cost per `next()` call is $2N / N = 2$, which is strictly $O(1)$.

**Q5: Is there any way to achieve $O(1)$ space instead of $O(H)$?**
*Answer:* Yes, using Morris Traversal. However, Morris Traversal modifies the tree structure (threading) during iteration. If the interviewer strictly forbids modifying the tree (even temporarily), then $O(H)$ space via a stack is the theoretical minimum.

**Q6: How would you use this iterator to solve Two Sum in a BST?**
*Answer:* I would create one forward iterator (`BSTIterator`) and one backward iterator (`BSTReverseIterator`). I fetch the smallest element (forward) and largest element (backward). If their sum equals target, return true. If sum < target, advance the forward iterator. If sum > target, advance the backward iterator. Total time $O(N)$, total space $O(H)$.

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Traverse a BST on demand in $O(1)$ amortized time per call and $O(H)$ space.
- **Data Structure:** Explicit `stack<TreeNode*>`.
- **Initialization:** Push `root` and all its continuous left children (`pushAllLeft`).
- **`next()` logic:** Pop top node, if it has a right child, call `pushAllLeft(node->right)`. Return popped node.
- **Trap:** Interviewers often question the $O(1)$ time complexity because of the `while` loop. Assert that it is *amortized* $O(1)$ because every node is stacked once.
