import os, sys, re, subprocess, tempfile

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

root = r"C:\Users\kunal\Desktop\notes\C++ DSA - Interview Notes"

md_files = []
for r, d, fnames in os.walk(root):
    for f in fnames:
        if f.endswith(".md") and not f.startswith("."):
            md_files.append(os.path.join(r, f))

cpp_block_re = re.compile(r"```(?:cpp|c\+\+)\n(.*?)```", re.DOTALL)

results = []

for mf in md_files:
    rel_path = os.path.relpath(mf, root)
    with open(mf, "r", encoding="utf-8") as f:
        content = f.read()
    
    for match in cpp_block_re.finditer(content):
        block = match.group(1)
        start_pos = match.start()
        prev_lines = content[:start_pos].split("\n")
        line_num = len(prev_lines)
        heading = ""
        for l in reversed(prev_lines):
            if l.startswith("#"):
                heading = l
                break
        
        # Strip leading '>' if present
        cleaned_block = "\n".join(re.sub(r"^\s*>\s?", "", l) for l in block.split("\n"))
        
        headers = """#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <unordered_map>
#include <unordered_set>
#include <map>
#include <set>
#include <queue>
#include <stack>
#include <climits>
using namespace std;
struct ListNode { int val; ListNode *next, *random, *bottom, *prev, *child; ListNode(int x): val(x), next(nullptr), random(nullptr), bottom(nullptr), prev(nullptr), child(nullptr) {} };
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int x): val(x), left(nullptr), right(nullptr) {} };
"""
        # Try test 1: in func
        with tempfile.NamedTemporaryFile(suffix=".cpp", delete=False, mode="w", encoding="utf-8") as tf:
            tf_path = tf.name
            if "int main(" not in cleaned_block and "void main(" not in cleaned_block:
                full_src = f"{headers}\nvoid test_func() {{\n{cleaned_block}\n}}\n"
            else:
                full_src = f"{headers}\n{cleaned_block}\n"
            tf.write(full_src)
        
        res = subprocess.run(["g++", "-std=c++20", "-fsyntax-only", tf_path], capture_output=True, text=True)
        try: os.remove(tf_path)
        except: pass
        
        if res.returncode != 0:
            # Try test 2: global scope
            with tempfile.NamedTemporaryFile(suffix=".cpp", delete=False, mode="w", encoding="utf-8") as tf2:
                tf2_path = tf2.name
                tf2.write(f"{headers}\n{cleaned_block}\n")
            res2 = subprocess.run(["g++", "-std=c++20", "-fsyntax-only", tf2_path], capture_output=True, text=True)
            try: os.remove(tf2_path)
            except: pass
            if res2.returncode == 0:
                continue
            
            # Still failed
            err_line = res.stderr.strip().split("\n")[0] if res.stderr else ""
            results.append({
                "file": rel_path,
                "line": line_num,
                "heading": heading,
                "error": err_line,
                "snippet": block.strip()[:100]
            })

with open(os.path.join(root, ".scripts", "code_check_results.txt"), "w", encoding="utf-8") as out:
    out.write(f"Total problematic blocks: {len(results)}\n\n")
    for r in results:
        out.write(f"[{r['file']}:{r['line']}] Under \"{r['heading']}\"\n")
        out.write(f"   Error: {r['error']}\n")
        out.write(f"   Snippet: {r['snippet']}\n")
        out.write("-" * 50 + "\n")

print(f"Done. Found {len(results)} issues. Saved to code_check_results.txt")
