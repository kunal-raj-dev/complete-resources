# Lecture 80: Circular Queue: Array Modulo Arithmetic (LeetCode 622)

> **One-Line Purpose:** Eliminate array false-overflow in bounded queues by wrapping indices with modulo arithmetic.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #80  
> **Video ID:** `4mKKolshFD0`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=4mKKolshFD0)  
> **Duration:** 18:37  
> **Status:** AUDITED  

---

## 🔵 Complete C++ Implementation

```cpp
#include <vector>
#include <iostream>
using namespace std;

class MyCircularQueue {
private:
    vector<int> data;
    int front;
    int rear;
    int size;
    int capacity;

public:
    MyCircularQueue(int k) : data(k), front(0), rear(-1), size(0), capacity(k) {}

    bool enQueue(int value) {
        if (isFull()) return false;
        rear = (rear + 1) % capacity;
        data[rear] = value;
        size++;
        return true;
    }

    bool deQueue() {
        if (isEmpty()) return false;
        front = (front + 1) % capacity;
        size--;
        return true;
    }

    int Front() {
        return isEmpty() ? -1 : data[front];
    }

    int Rear() {
        return isEmpty() ? -1 : data[rear];
    }

    bool isEmpty() { return size == 0; }
    bool isFull() { return size == capacity; }
};
```
