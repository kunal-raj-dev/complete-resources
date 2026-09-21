# Lecture 06: Binary Number System & Conversions

> **One-Line Purpose:** Understand binary positional representation, 2's complement encoding for negative numbers, and algorithmic conversions between Decimal and Binary number systems.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #06  
> **Video ID:** `xpy5NXiBFvA`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=xpy5NXiBFvA)  
> **Duration:** 37:20  
> **Transcript:** `.transcripts/02_bitwise_number_systems/006_Binary_Number_System___DSA_Series_by_Shradha_Khapra_Ma_am___C__.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The fundamental mathematical basis of Positional Number Systems: Decimal (Base-10) vs Binary (Base-2).
- The algorithmic method for converting Decimal integers to Binary representations without relying on external libraries.
- The algorithmic method for converting Binary numbers back to Decimal.
- Internal computer representation of signed integers using **Two's Complement**.
- Why modern CPUs use 2's complement rather than Sign-Magnitude or 1's complement (eliminating positive/negative zero and allowing uniform adder circuitry).

---

## 🔵 Lecture Context

All computer hardware operates exclusively on digital transistors representing binary states ($0$ and $1$). In DSA, bitwise manipulation is a premier technique for $O(1)$ operations, subset generation, bitmasks, and low-level optimization. Mastering binary arithmetic is the prerequisite for Bitwise Operators (Lecture 07) and advanced bitmasking.

---

## 1. Positional Number Systems

> 🔵 **Lecture Content**

In a positional base-$B$ system, a number is represented by digits $d_k d_{k-1} \dots d_0$, with total numerical value:
$$\text{Value} = \sum_{i=0}^k d_i \times B^i$$

- **Decimal ($B = 10$):** Digits $0 \dots 9$.
  $$345_{10} = (3 \times 10^2) + (4 \times 10^1) + (5 \times 10^0) = 300 + 40 + 5 = 345$$
- **Binary ($B = 2$):** Digits $0$ and $1$.
  $$1101_2 = (1 \times 2^3) + (1 \times 2^2) + (0 \times 2^1) + (1 \times 2^0) = 8 + 4 + 0 + 1 = 13_{10}$$

---

## 2. Conversions: Theory & Implementation

### A. Decimal to Binary Conversion
1. Divide the decimal number by $2$.
2. Note the remainder ($0$ or $1$).
3. Update the quotient: $N = N / 2$.
4. Repeat until $N = 0$.
5. The binary representation is the remainders written in **reverse order**.

```cpp
#include <iostream>
using namespace std;

int decToBinary(int decNum) {
    int ans = 0;
    int pow = 1; // Tracks 10^0, 10^1, 10^2... to build decimal integer

    while (decNum > 0) {
        int rem = decNum % 2;
        decNum /= 2;

        ans += (rem * pow);
        pow *= 10;
    }
    return ans;
}

int main() {
    int dec = 42;
    cout << "Binary of " << dec << " is: " << decToBinary(dec) << endl; // Prints 101010
    return 0;
}
```

> ⚠️ **Limitation of the Integer-Simulation Approach:**
> An `int` in C++ can only hold up to $\approx 2 \times 10^9$. A binary number with 10 digits exceeds $10^9$. For large numbers, binary must be stored as a `std::string` or `std::vector<int>` to prevent integer overflow.

---

### B. Binary to Decimal Conversion
1. Extract the last binary digit: `rem = binNum % 10`.
2. Multiply by positional weight of $2$: `ans += rem * pow`.
3. Update weight: `pow *= 2`.
4. Reduce binary number: `binNum /= 10`.

```cpp
#include <iostream>
using namespace std;

int binToDecimal(int binNum) {
    int ans = 0;
    int pow = 1; // Represents 2^0, 2^1, 2^2...

    while (binNum > 0) {
        int rem = binNum % 10;
        ans += (rem * pow);

        binNum /= 10;
        pow *= 2;
    }
    return ans;
}

int main() {
    int bin = 101010;
    cout << "Decimal of " << bin << " is: " << binToDecimal(bin) << endl; // Prints 42
    return 0;
}
```

---

## 3. Negative Numbers & Two's Complement

> 🔵 **Lecture Content**

How do computers store negative numbers like `-5` using only bits?

### The Two's Complement Algorithm:
1. **Find Binary of Absolute Value:**  
   $5_{10} = 00000101_2$ (in 8 bits).
2. **One's Complement (Bit Inversion):**  
   Flip all bits ($0 \to 1, 1 \to 0$):  
   $11111010_2$.
3. **Add 1 (Two's Complement):**  
   $$11111010_2 + 1_2 = 11111011_2 = -5_{10}$$

```
Value: -5
Bit Pattern (8-bit): [ 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 ]
                      ▲
             MSB = 1 indicates NEGATIVE
```

> 🧠 **Brain Trigger**
> 
> Why does Two's Complement prevail over One's Complement in CPU design?
> 
> **Answer:** 
> 1. In One's Complement, zero has two representations: $+0$ (`00000000`) and $-0$ (`11111111`), which complicates comparison logic. Two's complement has exactly **one zero** (`00000000`).
> 2. Standard addition circuitry ($A + B$) works identically for both positive and negative numbers without requiring separate subtraction hardware.

---

## 🔥 Interview Questions

### Q1: [Range Analysis] Why is the range of an 8-bit signed integer $[-128, 127]$ instead of $[-127, 127]$?
- **Short Answer:** Because $0$ is represented by positive zero (`00000000`), leaving an extra pattern (`10000000`) for the negative range.
- **Detailed Explanation:** In an $n$-bit 2's complement system:
  - Non-negative numbers: $0 \dots 2^{n-1} - 1$ ($0 \dots 127$).
  - Negative numbers: $-1 \dots -2^{n-1}$ ($-1 \dots -128$).
  - Pattern `10000000` has value $-2^7 = -128$. Its positive negation ($+128$) cannot be represented in 8 signed bits.

---

## Key Takeaways

1. **Binary Base:** Base-2 positional system where each bit represents powers of 2.
2. **2's Complement:** `~X + 1 = -X`. Eliminates dual-zero ambiguity.
3. **Range Asymmetry:** Signed $n$-bit integer ranges from $-2^{n-1}$ to $2^{n-1}-1$.

---

## ⚡ 2-Minute Revision

- **Dec $\to$ Bin:** Repeatedly extract `% 2`, divide by `2`, collect remainders in reverse.
- **Bin $\to$ Dec:** Extract `% 10`, multiply by running power of $2$, divide by `10`.
- **MSB:** $0$ = Non-negative, $1$ = Negative.
- **Negation:** Inverting all bits and adding $1$ gives the arithmetic negative.
