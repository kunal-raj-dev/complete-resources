# Lecture 69: Valid Parentheses (LeetCode 20)

> **One-Line Purpose:** Determine if bracket strings are properly nested and balanced by pairing closing brackets against expected top-of-stack opening brackets in $O(N)$ time and space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #69  
> **Video ID:** `NlHupEeDXzY`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=NlHupEeDXzY)  
> **Duration:** 16:25  
> **Status:** AUDITED  

---

## 💻 Complete C++ Implementation

```cpp
#include <string>
#include <stack>
#include <iostream>

using namespace std;

class SolutionValidParentheses {
public:
    bool isValid(string s) {
        stack<char> st;

        for (char ch : s) {
            if (ch == '(' || ch == '{' || ch == '[') {
                st.push(ch);
            } else {
                if (st.empty()) return false; // Closing bracket with no matching opening bracket
                char top = st.top();
                if ((ch == ')' && top == '(') ||
                    (ch == '}' && top == '{') ||
                    (ch == ']' && top == '[')) {
                    st.pop();
                } else {
                    return false; // Mismatched bracket types
                }
            }
        }

        return st.empty(); // Must have resolved all opening brackets
    }
};

int main() {
    SolutionValidParentheses solver;
    cout << "()[]{}: " << (solver.isValid("()[]{}") ? "VALID" : "INVALID") << endl; // VALID
    cout << "(]:     " << (solver.isValid("(]") ? "VALID" : "INVALID") << endl;     // INVALID
    return 0;
}
```

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(N)$
- **Space Complexity:** $O(N)$ worst-case stack depth.

---

## 🧠 Core Intuition — Why This Works

**The Bracket Pairing Insight:** Every closing bracket must match the **most recently seen** unmatched opening bracket. This is LIFO — the last opened bracket is the first one that must be closed. A stack naturally models this.

**Real-World Analogy:** Think of Russian nesting dolls (Matryoshka). You must open and close them in strictly reverse order. If you open a large doll, then a medium one inside, you must close the medium before the large.

```
"( [ { } ] )"  →  VALID
   ↑ opens: stack = [(, []
         ↑ opens: stack = [(, [, {]
           ↑ closes {: matches top {, pop → stack = [(, []
             ↑ closes ]: matches top [, pop → stack = [()]
               ↑ closes ): matches top (, pop → stack = []
               Stack empty → VALID ✓

"( ]"  →  INVALID
   ↑ opens: stack = [(]
     ↑ closes ]: top is (, mismatch → return false ✗
```

---

## 🎯 Pattern Recognition — When to Use Stack for Brackets

- Any problem with **nested structure** that must be closed in the reverse order it was opened.
- Keywords: "balanced", "valid", "matching brackets", "well-formed", "properly nested".
- **Simpler version (1 bracket type):** Use a counter — increment on `(`, decrement on `)`. Return `counter == 0` and counter never goes negative. No stack needed!

---

## 🔍 Dry Run Trace

Input: `"({[]})"`

```
i=0  ch='('  Opening → push '('    Stack: ['(']
i=1  ch='{'  Opening → push '{'    Stack: ['(', '{']
i=2  ch='['  Opening → push '['    Stack: ['(', '{', '[']
i=3  ch=']'  Closing, top='[' ✓   Stack: ['(', '{']       pop
i=4  ch='}'  Closing, top='{' ✓   Stack: ['(']            pop
i=5  ch=')'  Closing, top='(' ✓   Stack: []               pop
Loop ends. Stack empty → return TRUE
```

Input: `"([)]"`

```
i=0  ch='('  push         Stack: ['(']
i=1  ch='['  push         Stack: ['(', '[']
i=2  ch=')'  top='[' ≠ '(' → MISMATCH → return FALSE
```

---

## ⚠️ Common Interview Mistakes

1. **Not checking stack empty before accessing top:** `st.top()` on empty stack = UB. Always do `if (st.empty()) return false;` when you encounter a closing bracket.

2. **Forgetting to check stack is empty at the end:** Input `"((("` would pass the loop without error but the stack wouldn't be empty. Must `return st.empty()` not `return true`.

3. **Wrong bracket match mapping:** A very common typo — mapping `')'` to `')'` instead of `'('`. Use a map or triple-condition if-else.

4. **Treating all characters as brackets:** In extended versions, if the string contains non-bracket characters, only push/check actual brackets.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] Why is a stack the right data structure here instead of a simple counter?
**Answer:** A simple counter works only when there is **one type of bracket** — increment on open, decrement on close, check counter == 0 at end and never negative. With **multiple bracket types**, the order of closure matters. `"([)]"` has equal opens and closes, so a counter says valid, but a stack correctly identifies it as invalid because `]` doesn't match `(`.

### Q2: [Extension] How do you find the **minimum number of bracket insertions** to make a string valid?
**Answer:** Use two counters: `open` (unmatched opens needing a close) and `close` (unmatched closes needing an open).
```cpp
int minInsertions(string s) {
    int open = 0, close = 0;
    for (char ch : s) {
        if (ch == '(') open++;
        else { // ch == ')'
            if (open > 0) open--; // Match with existing open
            else close++;         // Need to insert an open
        }
    }
    return open + close; // open unmatched opens + close unmatched closes
}
```

### Q3: [Extension] Longest Valid Parentheses (LeetCode 32): How do you find the length of the longest valid substring?
**Answer:** Push **indices** instead of characters. Start with `-1` as a base index on the stack.
```cpp
int longestValidParentheses(string s) {
    stack<int> st;
    st.push(-1); // Base index
    int maxLen = 0;
    for (int i = 0; i < s.size(); i++) {
        if (s[i] == '(') {
            st.push(i);
        } else {
            st.pop();
            if (st.empty()) st.push(i); // New base
            else maxLen = max(maxLen, i - st.top());
        }
    }
    return maxLen;
}
```
Time: $O(N)$, Space: $O(N)$.

### Q4: [Output Prediction] What does the following code print for input `"[]{}("`?
```cpp
bool isValid(string s) {
    stack<char> st;
    for (char ch : s) {
        if (ch == '(' || ch == '{' || ch == '[') st.push(ch);
        else {
            if (st.empty()) return false;
            char top = st.top();
            if ((ch==')' && top=='(') || (ch=='}' && top=='{') || (ch==']' && top=='['))
                st.pop();
            else return false;
        }
    }
    return st.empty();
}
```
**Answer:** The loop processes `[`, `]` (match, pop), `{`, `}` (match, pop), `(` (push). At end, stack = `['(']`, which is NOT empty → returns **`false`**. The string is invalid because `(` is never closed.

### Q5: [Complexity] Can you solve Valid Parentheses in O(1) space?
**Answer:** Only for **single bracket types**. Use a counter: increment on `(`, decrement on `)`, return false if counter < 0 at any point, and true if counter == 0 at the end. For **multiple bracket types**, $O(N)$ space is provably necessary because we need to remember the order of all unmatched openers.

### Q6: [Extension] How would you check valid XML/HTML tags using a stack?
**Answer:** Same principle — when you encounter an opening tag `<tag>`, push `tag`. When you encounter a closing tag `</tag>`, check if it matches `st.top()`. If not, invalid. If yes, pop. At the end, the stack should be empty. The only difference from bracket matching is extracting the tag name string from the angle-bracket syntax.

### Q7: [Extension] How does the compiler use this concept to validate code?
**Answer:** Parsers in compilers perform bracket matching as part of **syntax analysis (parsing)**. They build an Abstract Syntax Tree (AST) where every `{` opens a scope block and `}` closes it. The parser uses an explicit stack to track open scopes. Mismatched braces in C++ give compile-time errors — that's the compiler's bracket-matching algorithm at work.

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Hint |
|---|---------|----------|
| 20 | Valid Parentheses | Classic stack matching |
| 32 | Longest Valid Parentheses | Push indices, track base |
| 678 | Valid Parenthesis String (`*`) | Stack + greedy range |
| 921 | Minimum Add to Make Parentheses Valid | Count unmatched opens/closes |
| 1249 | Minimum Remove to Make Valid | Push indices to remove |

---

## 🔗 Cross-Topic Connections

- **Recursion:** Recursive grammars (like arithmetic expressions) use implicit stacks — same principle.
- **Compiler Design:** Syntax parsing uses this exact pattern for scope validation.
- **String Manipulation:** Many "nested structure" string problems reduce to bracket matching.

---

## ⚡ 2-Minute Revision Flash Card

- **Key insight:** Most-recently-opened bracket must be closed first → LIFO → Stack.
- **Algorithm:** Push opens, match closes against stack top, return `st.empty()`.
- **Critical empty check:** `if (st.empty()) return false` when you see a closing bracket.
- **Single bracket type:** No stack needed, just use a counter.
- **Pitfall:** Don't forget `return st.empty()` at the end — not `return true`.
