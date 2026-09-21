# Lecture 122: Flood Fill Algorithm (LeetCode 733)

> **One-Line Purpose:** Re-color connected matrix pixels matching an initial target color using 4-directional DFS.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #122  
> **Video ID:** `JI_e2RzARbM`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=JI_e2RzARbM)  
> **Duration:** 15:10  
> **Status:** AUDITED  

---

## 🔵 Implementation

```cpp
#include <vector>
using namespace std;

class SolutionFloodFill {
private:
    void dfs(vector<vector<int>>& img, int r, int c, int oldColor, int newColor) {
        if (r < 0 || r >= img.size() || c < 0 || c >= img[0].size() || img[r][c] != oldColor) return;

        img[r][c] = newColor;

        dfs(img, r + 1, c, oldColor, newColor);
        dfs(img, r - 1, c, oldColor, newColor);
        dfs(img, r, c + 1, oldColor, newColor);
        dfs(img, r, c - 1, oldColor, newColor);
    }

public:
    vector<vector<int>> floodFill(vector<vector<int>>& image, int sr, int sc, int color) {
        if (image[sr][sc] != color) {
            dfs(image, sr, sc, image[sr][sc], color);
        }
        return image;
    }
};
```
