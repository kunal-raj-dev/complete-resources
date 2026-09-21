# Lecture 108: Populate Next Right Pointers in Each Node (LeetCode 116)

> **One-Line Purpose:** Connect horizontal adjacent sibling pointers across binary tree levels in $O(1)$ space using existing level connections.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #108  
> **Video ID:** `a8VKpW1DsD8`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=a8VKpW1DsD8)  
> **Duration:** 11:12  
> **Status:** AUDITED  

---

## 1. 🧱 Prerequisite Concepts
- **Level Order Traversal (BFS):** Navigating a tree layer by layer using a Queue.
- **Linked Lists:** Understanding how `next` pointers form a singly-linked list.
- **Perfect Binary Tree:** A tree where all internal nodes have two children and all leaves are at the exact same level.

## 2. 🧠 Core Concept & Explanation
Normally, to connect nodes horizontally, you would use a Queue to do a Level Order Traversal (BFS). However, standard BFS uses $O(N)$ auxiliary space for the queue. The magic here is realizing that **the `next` pointers we are establishing can act exactly like a Queue for the next level!**

Think of it like building a bridge. Once you have a bridge built on Level 1, you can walk across it to build the bridges for Level 2.
We have two specific types of connections to make:
1. **Siblings (Same Parent):** `node->left->next = node->right`
2. **Cousins (Different Parents):** `node->right->next = node->next->left` (This only works if the parent itself is already connected to its `next` neighbor).

By making sure a level is completely connected before we move down to its children, we achieve optimal $O(1)$ space.

## 3. 🚶‍♂️ Step-by-step Approach (Algorithm)
1. If the `root` is null, return `nullptr`.
2. Keep a pointer `leftMost` that tracks the start of each level. Initially, `leftMost = root`.
3. Loop downwards as long as there is a next level (`leftMost->left != nullptr`).
4. Inside, create a horizontal iterator `head = leftMost`.
5. Traverse the current level horizontally using the `next` pointers we previously established:
   - Connect the children of `head`: `head->left->next = head->right`.
   - If `head` has a neighbor (`head->next != nullptr`), connect the gap between families: `head->right->next = head->next->left`.
   - Move `head` to `head->next`.
6. Once the level is traversed, drop down to the next level: `leftMost = leftMost->left`.
7. Return the unmodified `root`.

## 4. 🔍 Dry Run / Execution Trace
Let's consider a perfect binary tree:
```text
       1
     /   \
    2     3
   / \   / \
  4   5 6   7
```
**Initialization:** `leftMost = Node(1)`
- **Level 1:** `head = 1`. 
  - Connect children: `1->left->next = 1->right` => `2->next = 3`. 
  - `head->next` is null. 
  - Move `leftMost` to `2`.
- **Level 2:** `head = 2`.
  - Connect children: `2->left->next = 2->right` => `4->next = 5`.
  - Connect cousins: `2->next` is `3`. So `2->right->next = 2->next->left` => `5->next = 6`.
  - Move `head` to `3`.
  - Connect children: `3->left->next = 3->right` => `6->next = 7`.
  - `head->next` is null.
  - Move `leftMost` to `4`.
- **Level 3:** `4->left` is null. The outer loop terminates. All connected!

## 5. 💻 Complete C++ Implementation

```cpp
struct Node {
    int val;
    Node* left;
    Node* right;
    Node* next;
    Node(int _val) : val(_val), left(nullptr), right(nullptr), next(nullptr) {}
};

class SolutionConnect {
public:
    Node* connect(Node* root) {
        if (!root) return nullptr;

        Node* leftMost = root;

        while (leftMost->left) {
            Node* head = leftMost;

            while (head) {
                // Connection 1: Sibling nodes under same parent
                head->left->next = head->right;

                // Connection 2: Adjacent cousins across different parents
                if (head->next) {
                    head->right->next = head->next->left;
                }

                head = head->next;
            }

            leftMost = leftMost->left;
        }

        return root;
    }
};
```

## 6. ⏱️ Complexity Analysis
- **Time Complexity:** $O(N)$. We visit each node in the tree exactly once to establish its children's `next` pointers.
- **Space Complexity:** $O(1)$ auxiliary space. We do not use any recursive stack or BFS queues, utilizing only a few pointer variables.

## 7. ⚠️ Edge Cases to Consider
- **Empty Tree (`root = nullptr`):** Gracefully return `nullptr` without trying to access `leftMost->left`.
- **Single Node Tree:** Loop condition `leftMost->left` fails immediately; correctly returns root with `next` as `nullptr`.
- **Imperfect Binary Trees:** Note that this specific exact optimal logic ONLY applies to *Perfect Binary Trees* (LeetCode 116). If the tree is imperfect (LeetCode 117), the logic for finding the next available child is much more complex.

## 8. ❌ Common Pitfalls & Mistakes
- **Processing Bottom-Up:** You absolutely cannot process this bottom-up. A parent node's `next` pointer *must* be fully resolved before you can bridge the gap between its right child and the cousin's left child.
- **Using a Queue (Non-optimal space):** Many candidates immediately reach for `std::queue<Node*>`. While correct and $O(N)$ time, it consumes $O(N)$ space, failing the $O(1)$ space requirement explicitly asked in follow-ups for this problem.
- **Null Pointer Dereference:** Failing to check `if (head->next)` before accessing `head->next->left`.

## 🎯 Pattern Recognition — When to Use This
- **Trigger Cues:** "Connect nodes at the same level", "Level order traversal in $O(1)$ space", "Horizontal pointers".
- **Why level-by-level pointer manipulation?** Any time you are asked to connect or traverse nodes horizontally but are strictly forbidden from using a Queue ($O(N)$ space), you must leverage the connections you build on level $L$ to traverse and build level $L+1$.

## 🏆 Related Problems (Leetcode)
- **Leetcode 116. Populating Next Right Pointers in Each Node:** The perfect binary tree version (this lecture).
- **Leetcode 117. Populating Next Right Pointers in Each Node II:** The imperfect binary tree version, where children can be missing, requiring a dummy node approach.
- **Leetcode 199. Binary Tree Right Side View:** Once `next` pointers are populated, the right side view is simply the last node of each linked list level.

## 🔗 Cross-Topic Connections
- **Linked Lists:** The problem essentially asks you to weave multiple Singly-Linked Lists horizontally through a Binary Tree.
- **BFS:** This is a simulated Breadth-First Search that uses the tree's own structure instead of an external Queue.

## 9. 💡 Expert Q&A / Interview Follow-ups
**Q1: How does this algorithm change if the tree is NOT a perfect binary tree? (LeetCode 117)**  
*Answer:* If the tree is imperfect, `head->left->next = head->right` doesn't always hold (e.g., `left` might be null but `right` exists). We have to maintain a "dummy node" at the start of each next level, and iterate a `current` pointer to link whatever non-null children exist on the next level across the entire current horizontal level.

**Q2: What is the implicit assumption we are making about the tree representation in memory?**  
*Answer:* We are assuming nodes have an extra memory allocated for the `next` pointer. Without the ability to modify the Node structure, $O(1)$ space horizontal traversal becomes practically impossible without modifying standard traversal algorithms drastically.

**Q3: Can we solve this using Recursion in $O(1)$ space?**  
*Answer:* By strict academic definitions, recursion uses $O(H)$ stack space. However, many interview platforms (like LeetCode) explicitly state: *"You may assume that implicit stack space does not count as extra space for this problem."* If that's the case, a recursive pre-order traversal linking `root->left->next = root->right` is perfectly valid.

**Q4: Can we do this with Post-Order traversal?**
*Answer:* No. Post-order processes children before the parent. We *must* establish the parent-level horizontal connections (the "bridge") before we can cross it to connect cousins. Pre-order or strict level-by-level (top-down) is mandatory.

**Q5: How does this algorithm benefit CPU cache compared to Queue-based BFS?**
*Answer:* Standard BFS pushes and pops disjoint node pointers from a dynamically allocated queue, causing cache misses. This $O(1)$ approach purely traverses existing memory connections, avoiding memory allocator overhead entirely, though it still jumps around the heap.

**Q6: What if we wanted to connect the `next` pointer to the node on the *left* instead of the right?**
*Answer:* We would traverse the levels from right-to-left instead. `leftMost` would become `rightMost` (following `node->right`), and we would connect `head->right->prev = head->left` and `head->left->prev = head->prev->right`.

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Connect all nodes at the same level horizontally.
- **Constraint:** $O(1)$ extra space (No Queue allowed!).
- **Core Logic:** Use Level $L$'s `next` pointers to traverse and connect Level $L+1$.
- **Two Connections:** Sibling (`head->left->next = head->right`) and Cousin (`head->right->next = head->next->left`).
- **Complexity:** $O(N)$ Time, $O(1)$ Space.
