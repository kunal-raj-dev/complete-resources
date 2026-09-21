# Lecture 29: Strings & Character Arrays in C++ — Part 1

> **One-Line Purpose:** Master the fundamental distinction between C-style null-terminated character arrays and dynamic `std::string` objects, memory layouts, and input streams.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #29  
> **Video ID:** `MOSjYaVymcU`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=MOSjYaVymcU)  
> **Duration:** 30:03  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The structure of C-style character arrays and the mandatory null-terminating character `'\0'`.
- Why `cin >>` stops reading at whitespace and how `cin.getline()` or `getline(cin, str)` captures full lines.
- The dynamic heap-allocated nature of C++ `std::string` and Small String Optimization (SSO).
- Crucial member functions: `length()`, `substr()`, `push_back()`, `pop_back()`.

---

## 🔵 Lecture Content

### 1. Character Arrays vs `std::string`

```cpp
#include <iostream>
#include <cstring>
#include <string>
using namespace std;

void stringBasics() {
    // 1. C-style char array
    char charArr[] = "hello"; // size is 6 bytes: 'h','e','l','l','o','\0'
    cout << "Length: " << strlen(charArr) << endl; // 5

    // 2. C++ std::string
    string s = "hello";
    s += " world"; // Dynamic reallocation handled automatically
    cout << "Size: " << s.size() << ", Capacity: " << s.capacity() << endl;

    // Reading with spaces
    string fullLine;
    // getline(cin, fullLine); // Reads until '\n'
}
```

---

## 2. Common Interview Traps with `getline`
When switching from `cin >> x` to `getline(cin, s)`, the trailing newline `'\n'` remains in the input stream buffer. Always consume it using `cin.ignore()` before `getline()`.

## 🧠 Core Intuition — Why This Works
A string is essentially a sequence of characters stored in memory. In C, it's just an array with a sentinel value (`\0`) at the end to mark termination. C++ introduced `std::string` which is a dynamic array (vector) of characters. It handles its own memory, tracking both size and capacity. When the capacity is exceeded, it dynamically allocates a larger block of memory (often double the size), copies the characters, and frees the old block. This allows strings to grow without bounds. Small String Optimization (SSO) often stores short strings (typically < 15-22 chars) directly inside the string object itself without heap allocation.

## 🎯 Pattern Recognition — When to Use This
- **Trigger cues:** "Parse a sentence", "Reverse string", "Check if character exists", "Handle user input with spaces".
- **Keywords:** `std::string`, `getline`, `cin.ignore()`, `c_str()`.

## 📐 Algorithm Walk-Through
When mixing `cin >>` and `getline`:
1. User inputs a number, presses Enter (`10\n`).
2. `cin >> n` reads `10` but leaves `\n` in the buffer.
3. `getline(cin, str)` sees `\n` immediately and reads an empty string!
4. **Fix:** Use `cin.ignore()` after `cin >> n` to consume the `\n`.

## 🔍 Dry Run Trace
Input Stream Buffer: `[ '4', '2', '\n', 'H', 'i', '\n' ]`
- `cin >> num;` -> Reads `'4'`, `'2'`. `num = 42`. Buffer: `[ '\n', 'H', 'i', '\n' ]`
- `getline(cin, str);` -> Reads until `\n`. It finds `\n` at index 0. `str = ""`.
- **With Fix:** `cin.ignore();` -> Consumes `\n`. Buffer: `[ 'H', 'i', '\n' ]`
- `getline(cin, str);` -> Reads `H`, `i`, stops at `\n`. `str = "Hi"`.

## ⚠️ Common Interview Mistakes
- **Mixing `cin` and `getline`:** Forgetting `cin.ignore()` and getting empty strings.
- **Index Out of Bounds:** Forgetting that C-style strings end with `\0`, so an array of 5 characters `char arr[5] = "hello"` is invalid (needs 6 bytes).
- **String Concatenation in Loops:** Doing `s = s + "a"` in a loop creates a new copy of `s` every time ($O(N^2)$). Use `s += "a"` or `s.push_back('a')` ($O(N)$ amortized).

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: What is Small String Optimization (SSO) in C++?
**Answer:** `std::string` implementations often avoid expensive heap allocations for short strings (typically under 15-22 bytes) by storing the characters directly within the memory allocated for the string object itself (stack/inline).

### Q2: Why is `s += 'a'` faster than `s = s + 'a'`?
**Answer:** `s += 'a'` appends the character directly to the existing string, amortizing capacity reallocations (just like `std::vector::push_back`). `s = s + 'a'` creates a completely new temporary string object, copies all existing characters, adds 'a', and then assigns it back, causing $O(N)$ work per operation.

### Q3: How do you convert a `std::string` to a C-style char array?
**Answer:** Use `s.c_str()`. This returns a `const char*` pointer to the internal array, guaranteed to be null-terminated. Note: The pointer becomes invalid if the string is modified or destroyed.

### Q4: Does `s.length()` calculate the length by iterating until `\0`?
**Answer:** No. `std::string` maintains an internal `size` variable. Therefore, `s.length()` and `s.size()` both execute in $O(1)$ time, unlike C's `strlen(char*)` which takes $O(N)$.

### Q5: Can `std::string` contain null characters (`\0`) in the middle?
**Answer:** Yes! Unlike C-strings which terminate at the first `\0`, `std::string` relies on its internal size counter. You can push a `\0` into it, and `size()` will accurately reflect it.

## 🏆 Related Problems (Leetcode)
- **LeetCode 344:** Reverse String (Basic character array manipulation)
- **LeetCode 58:** Length of Last Word (Basic string traversal)

## 🔗 Cross-Topic Connections
- **Dynamic Arrays (Vectors):** `std::string` operates almost identically to `std::vector<char>` internally.
- **Sliding Window:** String parsing is the foundation for Sliding Window string pattern matching.

## ⚡ 2-Minute Revision Flash Card
- **C-Strings:** Fixed arrays ending with `\0`. Use `strlen()` ($O(N)$).
- **C++ std::string:** Dynamic size, $O(1)$ `length()`.
- **Trap:** `cin >>` stops at space/newline. `getline()` reads full lines.
- **Fix:** Use `cin.ignore()` when switching from `cin >>` to `getline()`.
- **Performance:** Always use `+=` or `push_back()` in loops, never `= +`.
