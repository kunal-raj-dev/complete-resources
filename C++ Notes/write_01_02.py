import os
from generate_clean_topic12 import notes_data
from generate_clean_topic12_p2 import notes as notes_02

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t12_dir = os.path.join(root, "12_recursion_and_backtracking")

with open(os.path.join(t12_dir, "01_recursion_basics_to_advanced_part1.md"), "w", encoding="utf-8") as f:
    f.write(notes_data["01_recursion_basics_to_advanced_part1.md"])
print("Wrote 01 to disk.")

with open(os.path.join(t12_dir, "02_fibonacci_binary_search_sorted_array.md"), "w", encoding="utf-8") as f:
    f.write(notes_02["02_fibonacci_binary_search_sorted_array.md"])
print("Wrote 02 to disk.")
