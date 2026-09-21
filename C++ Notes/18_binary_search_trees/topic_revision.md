# ⚡ Rapid Revision — Topic 18: Binary Search Trees

> **Target:** 5-minute pre-interview refresher on BST invariants and algorithms.

---

## 🔑 Key Takeaways
- **BST Invariant:** Left $<$ Root $<$ Right. Inorder traversal yields strictly increasing sorted values.
- **Validate BST:** Never just check left and right child! Pass `(minVal, maxVal)` bounds.
- **LCA in BST:** Walk down. If both $< \text{root}$, go left; if both $> \text{root}$, go right; else `root` is LCA.
- **BST Iterator:** Maintain stack of left children. Space is $O(H)$, amortized time is $O(1)$.
- **Largest BST in BT:** Postorder passing `min`, `max`, `size`, and `isBST`.
