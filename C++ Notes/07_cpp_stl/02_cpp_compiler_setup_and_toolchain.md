# Lecture 28: C++ Compiler Setup & Development Toolchain

> **One-Line Purpose:** Establish a modern, production-grade C++ compilation environment using GCC/Clang, VS Code tasks, and compiler optimization flags.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #28  
> **Video ID:** `varXreLWPRo`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=varXreLWPRo)  
> **Duration:** 01:40  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

- Setup C++ compilers on macOS / Linux (`clang++` / `g++`) and Windows (MinGW-w64 / MSVC).
- Understand modern C++ compiler flags: `-std=c++17`, `-Wall`, `-Wextra`, `-O2`.
- Fast terminal compilation commands for competitive programming.

---

## 🔵 Content

### Essential Terminal Flags
```bash
g++ -std=c++17 -Wall -Wextra -O2 main.cpp -o main
./main
```
- `-std=c++17` enables structured binding, inline variables, and `std::string_view`.
- `-Wall -Wextra` surfaces all latent compiler warnings (uninitialized variables, signed/unsigned comparisons).
- `-O2` turns on production compiler optimizations.
