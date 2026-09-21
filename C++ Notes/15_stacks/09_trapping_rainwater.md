# Lecture 76: Trapping Rainwater (LeetCode 42)

> **One-Line Purpose:** Master the Two-Pointer inward boundary method to calculate trapped rainwater in $O(N)$ time and $O(1)$ auxiliary memory.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #76  
> **Video ID:** `UHHp8USwx4M`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=UHHp8USwx4M)  
> **Duration:** 30:50  
> **Status:** AUDITED  

---

## 🔵 Optimal Two-Pointer $O(1)$ Space Implementation

```cpp
#include <vector>
#include <algorithm>
#include <iostream>
using namespace std;

class SolutionTrappingWater {
public:
    int trap(vector<int>& height) {
        int left = 0, right = height.size() - 1;
        int leftMax = 0, rightMax = 0;
        int water = 0;

        while (left < right) {
            if (height[left] <= height[right]) {
                if (height[left] >= leftMax) {
                    leftMax = height[left];
                } else {
                    water += leftMax - height[left];
                }
                left++;
            } else {
                if (height[right] >= rightMax) {
                    rightMax = height[right];
                } else {
                    water += rightMax - height[right];
                }
                right--;
            }
        }
        return water;
    }
};
```
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(1)$ auxiliary memory.
