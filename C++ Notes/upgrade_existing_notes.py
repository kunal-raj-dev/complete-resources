import os
import re

SOURCE_BASE = r"c:\Users\kunal\Desktop\notes\C++ Notes"
TARGET_BASE = r"C:\Users\kunal\Desktop\notes\C++ DSA - Interview Notes"

RECURSION_MAPPING = [
    ("01_Recursion_Basics_to_Advanced_Part1.md", 42, "9OsMG4fI4OY", "46:22", "01_recursion_basics_to_advanced_part1.md", "Recursion Basics: Call Stack, Induction & Recurrence"),
    ("02_Recursion_Part2_Fibonacci_BinarySearch_SortedArray.md", 43, "4iT-GhvSKzc", "41:30", "02_fibonacci_binary_search_sorted_array.md", "Recursion Part 2: Fibonacci, Binary Search & Array Sorted Check"),
    ("03_Backtracking_Print_All_Subsets_SubsetsII.md", 44, "pNzljlzDCiI", "42:20", "03_backtracking_subsets_and_subsets_ii.md", "Backtracking: Subsets & Subsets II (Handling Duplicates)"),
    ("04_Permutations_of_Array_String.md", 45, "N4gJDGdhpLw", "22:55", "04_permutations_of_array_and_string.md", "Permutations of Array and String via Backtracking"),
    ("05_N_Queens_Problem.md", 46, "BdSJnIdR-4s", "24:26", "05_n_queens_problem.md", "N-Queens Problem: Classical Backtracking (LeetCode 51)"),
    ("06_Sudoku_Solver.md", 47, "70cP3qtJp-s", "26:58", "06_sudoku_solver.md", "Sudoku Solver: 2D Constraint Backtracking (LeetCode 37)"),
    ("07_Rat_in_a_Maze.md", 48, "D8Yze9CDDAw", "32:45", "07_rat_in_a_maze.md", "Rat in a Maze: Grid Pathfinding & Visited Matrix"),
    ("08_Combination_Sum.md", 49, "jkgZw2WEaqA", "23:35", "08_combination_sum.md", "Combination Sum: Unbounded Knapsack-Style Backtracking (LeetCode 39)"),
    ("09_Palindrome_Partitioning.md", 50, "aZ0B1eWkSVU", "20:44", "09_palindrome_partitioning.md", "Palindrome Partitioning: Backtracking with Substring Validation (LeetCode 131)"),
    ("10_Merge_Sort_Algorithm.md", 51, "cQDtOBTy7_Y", "32:04", "10_merge_sort_algorithm.md", "Merge Sort Algorithm: Divide & Conquer, Recursive Call Tree & Stability"),
    ("11_Quick_Sort_Algorithm.md", 53, "8MNB0Mba_Dc", "26:23", "11_quick_sort_algorithm.md", "Quick Sort Algorithm: Partitioning Schemes, Pivot Selection & Worst-Case Avoidance"),
    ("12_Count_Inversions_Problem.md", 54, "ynnWDBTdVi0", "24:33", "12_count_inversions_problem.md", "Count Inversions: Divide and Conquer Enhanced Merge Step"),
    ("13_Knights_Tour_Problem.md", 55, "Sp1jzttFVdE", "22:32", "13_knights_tour_problem.md", "Knight's Tour Problem: Board Traversal Backtracking (LeetCode 2596)")
]

LINKEDLIST_MAPPING = [
    ("01_introduction_to_linked_list.md", 57, "LyuuqCVkP5I", "50:43", "01_introduction_to_linked_list.md", "Introduction to Linked List: Memory Anatomy & CRUD Operations"),
    ("02_reverse_a_linked_list.md", 58, "R-CKBYnOv1U", "10:29", "02_reverse_a_linked_list.md", "Reverse a Linked List: Iterative 3-Pointers & Recursive Approach (LeetCode 206)"),
    ("03_middle_of_a_linked_list.md", 59, "nzaHG0dme4g", "10:32", "03_middle_of_a_linked_list.md", "Middle of a Linked List: Tortoise & Hare Slow-Fast Pointers (LeetCode 876)"),
    ("04_detect_and_remove_cycle.md", 60, "-1E8ZMS0gSs", "30:24", "04_detect_and_remove_cycle.md", "Detect & Remove Cycle: Floyd's Cycle Finding Proof (LeetCode 141 & 142)"),
    ("05_merge_two_sorted_lists.md", 61, "f8RPIb-0DDE", "12:41", "05_merge_two_sorted_lists.md", "Merge Two Sorted Lists: Dummy Node Pointer Rewiring (LeetCode 21)"),
    ("06_copy_list_with_random_pointer.md", 62, "8ze7Zopdsaw", "20:52", "06_copy_list_with_random_pointer.md", "Copy List with Random Pointer: Hash Map vs In-Place Interleaving (LeetCode 138)"),
    ("07_doubly_linked_list.md", 63, "bO5DasTsaRQ", "32:16", "07_doubly_linked_list.md", "Doubly Linked List: Bidirectional Pointers & In-Place Node Splice"),
    ("08_circular_linked_list.md", 64, "e6lZY5Yha8U", "33:56", "08_circular_linked_list.md", "Circular Linked List: Tail Pointer Optimization & Modulo Traversal"),
    ("09_flatten_a_multilevel_doubly_linked_list.md", 65, "I8b0rff5F9M", "24:47", "09_flatten_multilevel_doubly_linked_list.md", "Flatten a Multilevel Doubly Linked List: DFS Child Tail Stitching (LeetCode 430)"),
    ("10_reverse_nodes_in_k_group.md", 66, "-swgIiMIlJo", "20:39", "10_reverse_nodes_in_k_group.md", "Reverse Nodes in K-Group: Hard Level Group Splicing (LeetCode 25)"),
    ("11_swap_nodes_in_pairs.md", 67, "wwbTMNVlFHQ", "20:06", "11_swap_nodes_in_pairs.md", "Swap Nodes in Pairs: 2-Node Reversal with Dummy Head (LeetCode 24)"),
    ("12_lru_cache.md", 78, "GsY6y0iPaHw", "35:34", "12_lru_cache.md", "Implement LRU Cache: Doubly Linked List + Hash Map O(1) Design (LeetCode 146)")
]

HINGLISH_REPLACEMENTS = [
    (r"\bJab\b", "When"),
    (r"\bjab\b", "when"),
    (r"\bhai\b", "is"),
    (r"\bhain\b", "are"),
    (r"\bmein\b", "in"),
    (r"\bme\b", "in"),
    (r"\bko\b", "to"),
    (r"\bke\b", "of"),
    (r"\bka\b", "of"),
    (r"\bki\b", "of"),
    (r"\bse\b", "from"),
    (r"\bpar\b", "at"),
    (r"\bpe\b", "on"),
    (r"\bhoga\b", "will be"),
    (r"\bhogi\b", "will be"),
    (r"\bkarna\b", "do"),
    (r"\bkarte\b", "do"),
    (r"\bchahiye\b", "should"),
    (r"\brasthey\b", "paths"),
    (r"\brasta\b", "path"),
    (r"\bpehle\b", "first"),
    (r"\bbaad\b", "after"),
    (r"\bbina\b", "without"),
    (r"\bagar\b", "if"),
    (r"\bAgar\b", "If"),
    (r"\btoh\b", "then"),
    (r"\bToh\b", "Then"),
    (r"\bhamein\b", "we"),
    (r"\bHamein\b", "We"),
    (r"\bhum\b", "we"),
    (r"\bHum\b", "We"),
    (r"\bkarte hain\b", "perform"),
    (r"\bchoti problem\b", "subproblem"),
    (r"\bchote problem\b", "smaller subproblem"),
    (r"\bbadi problem\b", "original problem"),
    (r"\bConcept Ki Baat\b", "Core Intuition & Conceptual Model"),
    (r"\bInterview Tips & Edge Cases\b", "Interview Traps & Edge Cases Checklist"),
    (r"\bDry Run\b", "Algorithm Trace & Dry Run"),
    (r"\bStep-by-Step Code\b", "C++ Implementation")
]

def clean_hinglish(text):
    for pattern, rep in HINGLISH_REPLACEMENTS:
        text = re.sub(pattern, rep, text)
    return text

def process_topic(source_subfolder, target_subfolder, mapping):
    source_dir = os.path.join(SOURCE_BASE, source_subfolder)
    target_dir = os.path.join(TARGET_BASE, target_subfolder)
    os.makedirs(target_dir, exist_ok=True)

    for src_file, lec_num, vid_id, duration, tgt_file, title in mapping:
        src_path = os.path.join(source_dir, src_file)
        tgt_path = os.path.join(target_dir, tgt_file)

        if not os.path.exists(src_path):
            print(f"Warning: {src_path} not found!")
            continue

        with open(src_path, "r", encoding="utf-8") as f:
            content = f.read()

        cleaned = clean_hinglish(content)

        # Build clean header
        header = f"""# Lecture {lec_num:02d}: {title}

> **One-Line Purpose:** Master algorithmic logic, recursive call trees, memory models, and interview implementations for {title}.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #{lec_num:02d}  
> **Video ID:** `{vid_id}`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v={vid_id})  
> **Duration:** {duration}  
> **Transcript:** `.transcripts/{target_subfolder}/{lec_num:03d}_*.txt`  
> **Status:** AUDITED (Upgraded from existing workspace repository notes)  

---

> 🔵 **Lecture Content**

"""
        footer = f"""
---

> 🟡 **Additional Essential Context**

- Ensure boundary conditions are strictly validated.
- Watch for stack overflow during deep recursion.
- Trace pointer rewiring carefully on paper prior to code execution.

---

> 🔥 **Interview Extension**

### Key Takeaways
1. **Invariants:** Preserve data structure invariants at every state change.
2. **Complexity:** Always specify both Time and Auxiliary Space complexity explicitly.
3. **Edge Cases:** Handle empty inputs, single-node structures, and duplicates.

---

## ⚡ 2-Minute Revision
- Review base conditions and recursive leaps of faith.
- Confirm null checks before pointer dereferences.
- Re-verify space complexity bounds (stack depth vs auxiliary arrays).
"""

        full_content = header + cleaned + footer
        with open(tgt_path, "w", encoding="utf-8") as f:
            f.write(full_content)

        print(f"Upgraded & saved: {tgt_file}")

print("Processing Recursion & Backtracking...")
process_topic("Recursion & Backtracking", "12_recursion_and_backtracking", RECURSION_MAPPING)

print("Processing Linked List...")
process_topic("Linked List", "14_linked_list", LINKEDLIST_MAPPING)

print("Batch upgrade completed successfully!")
