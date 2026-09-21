# 💼 Topic Interview Question Bank — Topic 17: Binary Trees

---

### Q1: How does Morris Traversal achieve $O(1)$ auxiliary space?
**Answer:**
Standard recursive or stack-based traversals require $O(H)$ space to remember the ancestor path so the program can backtrack to parent nodes. Morris Traversal temporarily repurposes unused `nullptr` leaf pointers (specifically, the right child of the inorder predecessor) to create temporary "threads" back to the ancestor. Once the thread is used to backtrack, it is severed to restore the original tree structure.
