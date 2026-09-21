# Lecture 04: Patterns (Nested Loops & 2D Matrix Logic)

> **One-Line Purpose:** Master 2D spatial coordinate manipulation and nested loop index synchronization to build mental models for matrices, 2D arrays, and dynamic programming grids.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #04  
> **Video ID:** `rga_q2N7vU8`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=rga_q2N7vU8)  
> **Duration:** 01:31:07  
> **Transcript:** `.transcripts/01_cpp_basics/004_Lecture_4__Patterns___DSA_Series_by_Shradha_Khapra_Ma_am___C__.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The cognitive purpose of pattern programming in developing 2D matrix indexing intuition.
- The Universal 4-Step Pattern Framework used to systematically solve any nested loop problem.
- How to derive mathematical formulas relating row indices ($i$) to column indices ($j$), spaces, and characters.
- Standard patterns: Square grids, Right-angled triangles, Inverted triangles, Floyd's triangle, and Character matrices.
- Advanced symmetrical patterns: Pyramids, Hollow Diamonds, and Butterfly patterns.

---

## 🔵 Lecture Context

In DSA, pattern printing is not merely an academic exercise. It is the fundamental bridge between single-dimensional iteration and multi-dimensional coordinate mapping. Traversing a 2D matrix, rotating images, flood-filling grids, or filling Dynamic Programming tables all require the exact same mental models developed when writing nested loops for geometric patterns.

---

## 1. The Universal 4-Step Pattern Framework

> 🔵 **Lecture Content**

Whenever approaching any pattern printing problem, execute these four steps in strict order:

```
Step 1: Identify Total Rows
   ↳ Determines the Outer Loop: for (int i = 1; i <= n; i++)

Step 2: For row i, Identify Columns / Spaces / Stars
   ↳ Formulate count of elements in terms of i:
      - Spaces = n - i
      - Stars  = i, or 2*i - 1, etc.

Step 3: What to Print?
   ↳ Identify if the content is:
      - Constant ('*')
      - Dependent on row (i)
      - Dependent on column (j)
      - Continuous counter (val++)
      - Alphabet (char('A' + j - 1))

Step 4: End of Line Transition
   ↳ Print newline (cout << "\n") after the inner loops complete.
```

---

## 2. Fundamental Patterns & Code

### Pattern 1: Square Grid with Sequential Numbers
```text
1 2 3 4
1 2 3 4
1 2 3 4
1 2 3 4
```

```cpp
#include <iostream>
using namespace std;

int main() {
    int n = 4;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            cout << j << " ";
        }
        cout << "\n";
    }
    return 0;
}
```

---

### Pattern 2: Right-Angled Star Triangle
```text
*
* *
* * *
* * * *
```

```cpp
#include <iostream>
using namespace std;

int main() {
    int n = 4;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) {
            cout << "* ";
        }
        cout << "\n";
    }
    return 0;
}
```

---

### Pattern 3: Floyd's Triangle
Continuous running counter incremented at every cell.
```text
1
2 3
4 5 6
7 8 9 10
```

```cpp
#include <iostream>
using namespace std;

int main() {
    int n = 4;
    int num = 1;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) {
            cout << num << " ";
            num++;
        }
        cout << "\n";
    }
    return 0;
}
```

---

### Pattern 4: Character Grid
```text
A B C D
A B C D
A B C D
A B C D
```

```cpp
#include <iostream>
using namespace std;

int main() {
    int n = 4;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            char ch = 'A' + j - 1;
            cout << ch << " ";
        }
        cout << "\n";
    }
    return 0;
}
```

---

### Pattern 5: Inverted & Rotated Half Pyramid (Spaces + Stars)
```text
      *
    * *
  * * *
* * * *
```

#### Formula Derivation:
- Total rows: $N = 4$
- In row $i$:
  - Spaces: $N - i$
  - Stars: $i$

```cpp
#include <iostream>
using namespace std;

int main() {
    int n = 4;
    for (int i = 1; i <= n; i++) {
        // 1. Print Spaces
        for (int j = 1; j <= n - i; j++) {
            cout << "  ";
        }
        // 2. Print Stars
        for (int j = 1; j <= i; j++) {
            cout << "* ";
        }
        cout << "\n";
    }
    return 0;
}
```

---

### Pattern 6: Full Pyramid (Centrally Aligned)
```text
      *
    * * *
  * * * * *
* * * * * * *
```

#### Formula Derivation:
- Row $i$ has $N - i$ leading spaces.
- Row $i$ has $2 \times i - 1$ stars.

```cpp
#include <iostream>
using namespace std;

int main() {
    int n = 4;
    for (int i = 1; i <= n; i++) {
        for (int sp = 1; sp <= n - i; sp++) {
            cout << " ";
        }
        for (int st = 1; st <= 2 * i - 1; st++) {
            cout << "*";
        }
        cout << "\n";
    }
    return 0;
}
```

---

## 3. Advanced Symmetrical Pattern: Butterfly Pattern

```text
*             *
* *         * *
* * *     * * *
* * * * * * * *
* * * * * * * *
* * *     * * *
* *         * *
*             *
```

#### Decomposition:
Consists of two mirror halves:
1. **Upper Half ($1 \dots N$):**
   - Stars on left: $i$
   - Spaces in middle: $2 \times (N - i)$
   - Stars on right: $i$
2. **Lower Half ($N \dots 1$):**
   - Exact reverse of upper half.

```cpp
#include <iostream>
using namespace std;

int main() {
    int n = 4;

    // Upper Half
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) cout << "*";
        for (int j = 1; j <= 2 * (n - i); j++) cout << " ";
        for (int j = 1; j <= i; j++) cout << "*";
        cout << "\n";
    }

    // Lower Half
    for (int i = n; i >= 1; i--) {
        for (int j = 1; j <= i; j++) cout << "*";
        for (int j = 1; j <= 2 * (n - i); j++) cout << " ";
        for (int j = 1; j <= i; j++) cout << "*";
        cout << "\n";
    }

    return 0;
}
```

---

## 🧠 Mental Model

Think of nested loops as a Cartesian coordinate raster scan:
```
(i=1, j=1)  (i=1, j=2)  (i=1, j=3)  ... (i=1, j=n)  -> endl
(i=2, j=1)  (i=2, j=2)  (i=2, j=3)  ... (i=2, j=n)  -> endl
...
```
Outer loop $i$ controls the **vertical Y-axis** (row step).  
Inner loop $j$ controls the **horizontal X-axis** (column step).

---

## ⚠️ Common Mistakes

1. **Reusing Loop Variable Names:** Writing `for (int i = 1; i <= n; i++)` and inside it `for (int i = 1; i <= n; i++)`. This creates variable shadowing and results in an infinite or corrupted loop.
2. **Hardcoding Space Widths:** Using 1 space for characters but 2 spaces for alignment can warp symmetrical pyramids. Maintain exact character-to-space ratios.

---

## 🔥 Interview Questions

### Q1: [Complexity Analysis] What is the Time Complexity of printing an $N \times N$ pattern?
- **Short Answer:** $O(N^2)$ time complexity and $O(1)$ auxiliary space.
- **Detailed Explanation:** The outer loop executes $N$ times. For each iteration, the inner loop executes on the order of $N$ times (or $i$ times, where $\sum_{i=1}^N i = \frac{N(N+1)}{2} = O(N^2)$). Thus, total characters printed is quadratic. Space complexity is $O(1)$ because only scalar variables are used.

### Q2: [Algorithmic Application] How does pattern printing translate to 2D Array Matrix problems?
- **Short Answer:** It builds intuition for traversal boundaries, diagonal conditions, and spiral traversals.
- **Detailed Explanation:** 
  - Primary Diagonal: Cells where $i == j$.
  - Secondary Diagonal: Cells where $i + j == N + 1$.
  - Upper Triangular Matrix: Cells where $j \ge i$.
  - Lower Triangular Matrix: Cells where $j \le i$.

---

## Key Takeaways

1. **Structured Derivation:** Never guess nested loop bounds—tabulate row index $i$ against count of spaces and stars.
2. **Floyd's Pattern:** Tracks state across loop iterations using an external counter.
3. **Matrix Foundations:** Directly maps to 2D arrays and image processing.

---

## ⚡ 2-Minute Revision

- **Square:** `i: 1->n`, `j: 1->n`.
- **Triangle:** `i: 1->n`, `j: 1->i`.
- **Inverted Triangle:** `i: 1->n`, `j: 1->(n - i + 1)`.
- **Pyramid Stars Formula:** $2 \times i - 1$ with $n - i$ spaces.
- **Time Complexity:** $O(N^2)$ for standard 2D patterns.
