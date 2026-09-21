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
