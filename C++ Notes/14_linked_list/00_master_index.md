# Topic 14: Linked List — Master Index

> **Domain:** Non-Contiguous Dynamic Memory, Node Pointers, Cycle Detection, Structural Rewiring, and Cache Systems

---

## 📋 Topic Overview

This module provides a comprehensive exploration of Linked Lists, from low-level memory allocation of self-referential Node structs to FAANG-hard structural rewiring problems. It covers Singly, Doubly, and Circular Linked Lists, slow-fast two pointer techniques (Floyd's Cycle Algorithm), recursive list reversals, deep cloning with arbitrary random pointers, multilevel flattening, $K$-group node reversals, and constant-time LRU Cache architecture.

---

## 📑 Lecture Index

| # | Lecture Title | Focus Areas | Notes Link | Status |
|---|---|---|---|---|
| **57** | Introduction to Linked List | Heap nodes, `head`/`tail`, traversal, insertion, deletion, $O(1)$ vs $O(N)$ | [01_introduction_to_linked_list.md](./01_introduction_to_linked_list.md) | **AUDITED** |
| **58** | Reverse a Linked List | Iterative 3-pointer (`prev`, `curr`, `next`), recursive reversal (LC 206) | [02_reverse_a_linked_list.md](./02_reverse_a_linked_list.md) | **AUDITED** |
| **59** | Middle of a Linked List | Tortoise & Hare slow-fast pointer convergence (LC 876) | [03_middle_of_a_linked_list.md](./03_middle_of_a_linked_list.md) | **AUDITED** |
| **60** | Detect & Remove Cycle | Floyd's Cycle Algorithm, mathematical cycle entry proof (LC 141, 142) | [04_detect_and_remove_cycle.md](./04_detect_and_remove_cycle.md) | **AUDITED** |
| **61** | Merge Two Sorted Lists | Dummy head node, pointer rewiring without new nodes (LC 21) | [05_merge_two_sorted_lists.md](./05_merge_two_sorted_lists.md) | **AUDITED** |
| **62** | Copy List with Random Pointer | Hash map lookup vs $O(1)$ in-place node interleaving (LC 138) | [06_copy_list_with_random_pointer.md](./06_copy_list_with_random_pointer.md) | **AUDITED** |
| **63** | Doubly Linked List Tutorial | Bidirectional pointers (`prev`, `next`), in-place insertion/deletion | [07_doubly_linked_list.md](./07_doubly_linked_list.md) | **AUDITED** |
| **64** | Circular Linked List | Tail pointer optimization, circular traversal, Josephus connection | [08_circular_linked_list.md](./08_circular_linked_list.md) | **AUDITED** |
| **65** | Flatten Multilevel Doubly LL | DFS traversal, child list splicing, tail pointer stitching (LC 430) | [09_flatten_multilevel_doubly_linked_list.md](./09_flatten_multilevel_doubly_linked_list.md) | **AUDITED** |
| **66** | Reverse Nodes in K-Group | $K$-length pre-validation, group reversal, tail-to-next reconnection (LC 25) | [10_reverse_nodes_in_k_group.md](./10_reverse_nodes_in_k_group.md) | **AUDITED** |
| **67** | Swap Nodes in Pairs | Dummy node, 2-node rewiring, iterative vs recursive (LC 24) | [11_swap_nodes_in_pairs.md](./11_swap_nodes_in_pairs.md) | **AUDITED** |
| **78** | Implement LRU Cache | Doubly Linked List + Hash Map $O(1)$ `get`/`put` system design (LC 146) | [12_lru_cache.md](./12_lru_cache.md) | **AUDITED** |

---

## 🎯 Topic Revision & Interview Preparation
- **Topic Quick Revision:** [topic_revision.md](./topic_revision.md)
- **Topic Interview Question Bank:** [topic_interview_questions.md](./topic_interview_questions.md)
