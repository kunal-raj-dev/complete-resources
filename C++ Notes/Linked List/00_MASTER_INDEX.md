# 📚 Linked List Master Roadmap & Interview Cheat Sheet
> **Playlist:** [Linked List Complete Series for FAANG](https://www.youtube.com/playlist?list=PLGjplNEQ1it-OKRcYlCEDpTiIB1YOcvn6) by Shradha Khapra  
> **Target Audience:** Engineering Students, FAANG / Tier-1 Product Company Aspirants  
> **Language & Style:** Intuitive Hinglish + Professional English Technical Standard

---

## 🗺️ Playlist Structure & Index

| # | Topic / Video Title | Core Technique / Pattern | LeetCode Ref | Difficulty | Notes File Link |
|---|---|---|---|---|---|
| **01** | Introduction to Linked List | Dynamic Memory, Singly LL, CRUD Operations | Basic DS | Easy | [01_introduction_to_linked_list.md](./01_introduction_to_linked_list.md) |
| **02** | Reverse a Linked List | 3-Pointers (`prev`, `curr`, `next`), Recursion | LC 206 | Easy | [02_reverse_a_linked_list.md](./02_reverse_a_linked_list.md) |
| **03** | Middle of a Linked List | Tortoise & Hare (Slow & Fast Pointers) | LC 876 | Easy | [03_middle_of_a_linked_list.md](./03_middle_of_a_linked_list.md) |
| **04** | Detect & Remove Cycle | Floyd's Cycle Algorithm, Cycle Entry Proof | LC 141, 142 | Medium | [04_detect_and_remove_cycle.md](./04_detect_and_remove_cycle.md) |
| **05** | Merge Two Sorted Lists | Dummy Node, Pointer Rewiring, Recursion | LC 21 | Easy | [05_merge_two_sorted_lists.md](./05_merge_two_sorted_lists.md) |
| **06** | Copy List with Random Pointer | Hash Map vs In-place Interleaving ($O(1)$ Space) | LC 138 | Medium | [06_copy_list_with_random_pointer.md](./06_copy_list_with_random_pointer.md) |
| **07** | Doubly Linked List Tutorial | Bidirectional Pointers (`prev`, `next`), CRUD | Standard DS | Easy-Med | [07_doubly_linked_list.md](./07_doubly_linked_list.md) |
| **08** | Circular Linked List | Tail Pointer Optimization, Modulo Traversal | Standard DS | Easy-Med | [08_circular_linked_list.md](./08_circular_linked_list.md) |
| **09** | Flatten Multilevel Doubly LL | DFS Traversal, Tail Stitching | LC 430 | Medium | [09_flatten_a_multilevel_doubly_linked_list.md](./09_flatten_a_multilevel_doubly_linked_list.md) |
| **10** | Reverse Nodes in K-Group | K-Length Verification, Group Reversal | LC 25 | Hard | [10_reverse_nodes_in_k_group.md](./10_reverse_nodes_in_k_group.md) |
| **11** | Swap Nodes in Pairs | Dummy Node, 2-Node Reversal, Pointer Swap | LC 24 | Medium | [11_swap_nodes_in_pairs.md](./11_swap_nodes_in_pairs.md) |
| **12** | Implement LRU Cache | Doubly Linked List + Hash Map ($O(1)$ ops) | LC 146 | Med-Hard | [12_lru_cache.md](./12_lru_cache.md) |

---

## ⚡ Core Patterns & Mental Models (FAANG Interview Cheat Sheet)

### 1. Two Pointers / Fast & Slow (Tortoise and Hare)
* **Kaha use karein?** 
  - Middle element find karna ho.
  - Cycle detect karna ho (Floyd's algorithm).
  - K-th node from end dhundhna ho.
* **Key Rule:**
  - `slow` moves 1 step: `slow = slow->next`
  - `fast` moves 2 steps: `fast = fast->next->next`
  - Termination condition: `while (fast != nullptr && fast->next != nullptr)`

### 2. Dummy / Sentinel Node Technique
* **Kaha use karein?**
  - Jab new head decide na ho (e.g., Merge 2 sorted lists, Partition list).
  - Jab head node delete ya modify ho sakta ho (e.g., Remove duplicates, Swap in pairs).
* **Fayda:**
  - Head ke liye special `if (head == NULL)` conditions nahi likhni padti.
  - `dummy->next` hamesha result list ka actual head hold karta hai.

### 3. In-Place Reversal (3-Pointer Pattern)
* **Pointers:** `prev = nullptr`, `curr = head`, `next_node = nullptr`
* **Loop Step:**
  ```cpp
  next_node = curr->next;  // 1. Aage ka raasta save karo
  curr->next = prev;       // 2. Arrow piche mod do
  prev = curr;             // 3. prev ko aage badhao
  curr = next_node;        // 4. curr ko aage badhao
  ```
* Loop ke baad naya head `prev` ban jata hai!

### 4. Hash Map + Doubly Linked List (Design Pattern)
* **Kaha use karein?** LRU Cache, LFU Cache, All $O(1)$ Data Structures.
* **Why DLL?** Kisi bhi node ko $O(1)$ mein remove karne ke liye `node->prev` aur `node->next` directly available hote hain.
* **Why HashMap?** Kisi bhi key ko $O(1)$ mein lookup karne ke liye.

---

## ⏱️ Complexity Quick Reference

| Operation | Array / Vector | Singly Linked List | Doubly Linked List |
|---|---|---|---|
| Access by Index (`arr[i]`) | $O(1)$ | $O(N)$ | $O(N)$ |
| Insert at Head | $O(N)$ (shift elements) | $O(1)$ | $O(1)$ |
| Insert at Tail (with tail pointer) | $O(1)$ amortized | $O(1)$ | $O(1)$ |
| Insert at Middle (given pointer) | $O(N)$ (shifting) | $O(1)$ | $O(1)$ |
| Delete at Head | $O(N)$ (shift elements) | $O(1)$ | $O(1)$ |
| Delete at Tail | $O(1)$ | $O(N)$ (need prev of tail) | $O(1)$ |
| Search element | $O(N)$ (sorted: $O(\log N)$) | $O(N)$ | $O(N)$ |

---

## 💡 Top 5 Golden Rules for Linked List Interviews

1. **Always check for `NULL`:** Kabhi bhi `curr->next` access karne se pehle ensure karo `curr != NULL`. Agar double pointer hop kar rahe ho (`curr->next->next`), toh dono check karo: `curr != NULL && curr->next != NULL`.
2. **Never lose the reference to the remaining list:** Jab bhi koi pointer rewire karo, pehle aage ki list ka address kisi temporary variable (`temp` / `next_node`) mein store karo.
3. **Use Pen & Paper first:** Interview mein code likhne se pehle 4-5 nodes ka diagram draw karke pointers move karo.
4. **Always test on Edge Cases:**
   - Empty list (`head == NULL`)
   - Single node (`head->next == NULL`)
   - Two nodes
   - Odd vs Even length
5. **Memory Management (C++):** Real-world aur pure C++ interviews mein deleted nodes ko `delete temp;` karna mat bhulo to avoid memory leaks.
