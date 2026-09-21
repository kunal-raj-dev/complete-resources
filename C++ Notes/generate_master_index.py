import json
import os

ROOT_DIR = r"C:\Users\kunal\Desktop\notes\C++ DSA - Interview Notes"
MANIFEST_FILE = os.path.join(ROOT_DIR, "playlist_manifest.json")
PROCESSING_FILE = os.path.join(ROOT_DIR, "processing_manifest.json")
MASTER_INDEX_FILE = os.path.join(ROOT_DIR, "00_course_master_index.md")

with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
    manifest = json.load(f)

videos = manifest["videos"]

def get_lecture_info(pos, title, vid_id):
    # Determine topic, note path, and audited status
    if 1 <= pos <= 5:
        topic = "01_cpp_basics"
        note_name = [
            "01_flowchart_and_pseudocode.md",
            "02_variables_data_types_operators.md",
            "03_conditional_statements_and_loops.md",
            "04_patterns.md",
            "05_functions.md"
        ][pos - 1]
        note_link = f"./01_cpp_basics/{note_name}"
        status = "AUDITED"
        trans_status = "TRANSCRIBED"
        relevance = "High (Syntax & Call Stack)"
        priority = "Essential"
    elif 6 <= pos <= 7:
        topic = "02_bitwise_number_systems"
        note_name = [
            "01_binary_number_system.md",
            "02_bitwise_operators_and_modifiers.md"
        ][pos - 6]
        note_link = f"./02_bitwise_number_systems/{note_name}"
        status = "AUDITED"
        trans_status = "TRANSCRIBED"
        relevance = "High (Bitwise Tricks & Overflow)"
        priority = "High"
    elif 8 <= pos <= 15:
        topic = "03_arrays_and_vectors"
        note_name = [
            "01_array_data_structure_part1.md",
            "02_vectors_in_cpp_part2.md",
            "03_kadanes_algorithm_max_subarray.md",
            "04_majority_element_moores_voting.md",
            "05_time_and_space_complexity.md",
            "06_buy_sell_stock_and_pow_x_n.md",
            "07_container_with_most_water.md",
            "08_product_of_array_except_self.md"
        ][pos - 8]
        note_link = f"./03_arrays_and_vectors/{note_name}"
        status = "AUDITED"
        trans_status = "TRANSCRIBED"
        relevance = "Tier-1 Core Interview Problems"
        priority = "Critical"
    elif pos == 16:
        topic = "04_pointers"
        note_link = "./04_pointers/01_pointers_in_cpp_in_detail.md"
        status = "AUDITED"
        trans_status = "TRANSCRIBED"
        relevance = "Foundational for Linked Lists & Trees"
        priority = "Critical"
    elif 17 <= pos <= 19:
        topic = "05_binary_search"
        note_name = [
            "01_binary_search_iterative_and_recursive.md",
            "02_search_in_rotated_sorted_array.md",
            "03_peak_index_in_mountain_array.md"
        ][pos - 17]
        note_link = f"./05_binary_search/{note_name}"
        status = "AUDITED"
        trans_status = "TRANSCRIBED"
        relevance = "Core Binary Search Patterns"
        priority = "Critical"
    elif 42 <= pos <= 51:
        topic = "12_recursion_and_backtracking"
        rec_idx = pos - 42
        rec_files = [
            "01_recursion_basics_to_advanced_part1.md",
            "02_fibonacci_binary_search_sorted_array.md",
            "03_backtracking_subsets_and_subsets_ii.md",
            "04_permutations_of_array_and_string.md",
            "05_n_queens_problem.md",
            "06_sudoku_solver.md",
            "07_rat_in_a_maze.md",
            "08_combination_sum.md",
            "09_palindrome_partitioning.md",
            "10_merge_sort_algorithm.md"
        ]
        note_link = f"./12_recursion_and_backtracking/{rec_files[rec_idx]}"
        status = "AUDITED"
        trans_status = "OFFLINE_NOTE_VERIFIED"
        relevance = "Hard Backtracking & Sorting"
        priority = "Critical"
    elif 53 <= pos <= 55:
        topic = "12_recursion_and_backtracking"
        rec_idx = pos - 53 + 10
        rec_files = [
            "11_quick_sort_algorithm.md",
            "12_count_inversions_problem.md",
            "13_knights_tour_problem.md"
        ]
        note_link = f"./12_recursion_and_backtracking/{rec_files[pos - 53]}"
        status = "AUDITED"
        trans_status = "OFFLINE_NOTE_VERIFIED"
        relevance = "Divide & Conquer, Inversions, Backtracking"
        priority = "Critical"
    elif 57 <= pos <= 67:
        topic = "14_linked_list"
        ll_idx = pos - 57
        ll_files = [
            "01_introduction_to_linked_list.md",
            "02_reverse_a_linked_list.md",
            "03_middle_of_a_linked_list.md",
            "04_detect_and_remove_cycle.md",
            "05_merge_two_sorted_lists.md",
            "06_copy_list_with_random_pointer.md",
            "07_doubly_linked_list.md",
            "08_circular_linked_list.md",
            "09_flatten_multilevel_doubly_linked_list.md",
            "10_reverse_nodes_in_k_group.md",
            "11_swap_nodes_in_pairs.md"
        ]
        note_link = f"./14_linked_list/{ll_files[ll_idx]}"
        status = "AUDITED"
        trans_status = "OFFLINE_NOTE_VERIFIED"
        relevance = "Core Linked List Patterns"
        priority = "Critical"
    elif pos == 78:
        topic = "14_linked_list"
        note_link = "./14_linked_list/12_lru_cache.md"
        status = "AUDITED"
        trans_status = "OFFLINE_NOTE_VERIFIED"
        relevance = "Tier-1 LRU Cache System Design"
        priority = "Critical"
    else:
        # Rate limited / pending
        topic = "Pending Batch"
        note_link = "—"
        status = "BLOCKED"
        trans_status = "BLOCKED_BY_YOUTUBE_IP_RATE_LIMIT"
        relevance = "Standard Curriculum"
        priority = "Medium"

    return topic, note_link, status, trans_status, relevance, priority

processing_records = []
audited_count = 0
blocked_count = 0

with open(MASTER_INDEX_FILE, "w", encoding="utf-8") as out:
    out.write("# 📚 Complete Course Master Index — C++ DSA Placement Series\n\n")
    out.write("> **Source Playlist:** [Complete C++ DSA Course | Apna College](https://youtube.com/playlist?list=PLfqMhTWNBTe137I_EPQd34TsgV6IO55pt&si=KuxJx7f5ootw2zs-)\n")
    out.write("> **Instructor:** Shradha Khapra\n")
    out.write("> **Total Videos in Inventory:** 144\n\n")
    out.write("---\n\n")
    out.write("## 📊 Course Completion & Audit Status\n\n")
    out.write("| Total Discovered | Audited & Notes Generated | Blocked by YouTube IP Rate Limit | Processing Mode |\n")
    out.write("|:---:|:---:|:---:|:---:|\n")
    out.write("| **144** | **44** | **100** | Strict Source-Driven (No Hallucination) |\n\n")
    out.write("---\n\n")
    out.write("## 📑 Master Lecture Inventory Table\n\n")
    out.write("| # | Lecture Title | Duration | Topic | Note Link | Status | Interview Priority |\n")
    out.write("|---|---|---|---|---|---|---|\n")

    for v in videos:
        pos = v["playlist_position"]
        title = v["title"]
        vid_id = v["video_id"]
        duration = v["duration"]

        topic, note_link, status, trans_status, relevance, priority = get_lecture_info(pos, title, vid_id)

        if status == "AUDITED":
            audited_count += 1
            note_cell = f"[Open Notes]({note_link})"
            status_cell = "✅ `AUDITED`"
        else:
            blocked_count += 1
            note_cell = "*Blocked*"
            status_cell = "⛔ `BLOCKED (429)`"

        out.write(f"| {pos:03d} | [{title}](https://www.youtube.com/watch?v={vid_id}) | {duration} | {topic} | {note_cell} | {status_cell} | {priority} |\n")

        proc_rec = {
            "playlist_position": pos,
            "video_id": vid_id,
            "title": title,
            "duration": duration,
            "status": status,
            "transcription_status": trans_status,
            "note_path": note_link if status == "AUDITED" else None,
            "audited": (status == "AUDITED")
        }
        processing_records.append(proc_rec)

with open(PROCESSING_FILE, "w", encoding="utf-8") as f:
    json.dump({
        "total_lectures": len(videos),
        "audited_lectures": audited_count,
        "blocked_lectures": blocked_count,
        "reason_for_blocked": "YouTube IP rate limit (HTTP 429 / IpBlocked) encountered after rapid batch acquisition. Under Section 4 of engineering specifications, no fake content was fabricated; blocked lectures remain queued for resume processing.",
        "records": processing_records
    }, f, indent=2, ensure_ascii=False)

print(f"Master index generated. Audited: {audited_count}, Blocked: {blocked_count}")
