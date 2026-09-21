# Lecture 108: Populate Next Right Pointers in Each Node (LeetCode 116)

> **One-Line Purpose:** Connect horizontal adjacent sibling pointers across binary tree levels in $O(1)$ space using existing level connections.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #108  
> **Video ID:** `a8VKpW1DsD8`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=a8VKpW1DsD8)  
> **Duration:** 11:12  
> **Status:** AUDITED  

---

## 🔵 Optimal $O(1)$ Auxiliary Space Implementation

```cpp
struct Node {
    int val;
    Node* left;
    Node* right;
    Node* next;
    Node(int _val) : val(_val), left(nullptr), right(nullptr), next(nullptr) {}
};

class SolutionConnect {
public:
    Node* connect(Node* root) {
        if (!root) return nullptr;

        Node* leftMost = root;

        while (leftMost->left) {
            Node* head = leftMost;

            while (head) {
                // Connection 1: Sibling nodes under same parent
                head->left->next = head->right;

                // Connection 2: Adjacent cousins across different parents
                if (head->next) {
                    head->right->next = head->next->left;
                }

                head = head->next;
            }

            leftMost = leftMost->left;
        }

        return root;
    }
};
```
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(1)$ auxiliary.
