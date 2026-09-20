# 📖 Lecture 07: Doubly Linked List Tutorial
> **Video Link:** [Doubly Linked List Tutorial](https://www.youtube.com/watch?v=bO5DasTsaRQ)  
> **Instructor:** Shradha Khapra  
> **Topic:** Doubly Linked List (DLL) Architecture, Bidirectional Traversal, Full Implementation ($O(1)$ Operations)

---

## 🎯 1. Concept Ki Baat (Core Intuition)

### Singly Linked List Ki Sabse Badi Kamzori:
Singly Linked List mein ek bohot badi limitation thi:
- Hum sirf **aage (forward)** chal sakte hain, **piche (backward)** nahi!
- Agar humare paas `tail` pointer ho bhi, tab bhi `pop_back()` karne ke liye hume `head` se pura traverse karke second-last node tak aana padta tha ($O(N)$ time).
- Agar kisi given node ko delete karna ho, toh jab tak uske piche waala node pata na ho, hum us node ko direct delete nahi kar sakte the.

### 🌟 Doubly Linked List (DLL) Ka Solution:
DLL mein har node ke paas do pointers hote hain:
1. `next`: Agle node ka address.
2. `prev`: Piche waale node ka address.

```
NULL ◄── [ prev | 10 | next ] ◄═══► [ prev | 20 | next ] ◄═══► [ prev | 30 | next ] ──► NULL
              head                                                    tail
```

### ⚖️ DLL ke Fayde vs Nuksaan:
- **Pros:**
  - Forward aur Backward dono directions mein traverse kar sakte hain.
  - Given pointer wale node ko $O(1)$ mein delete kiya ja sakta hai.
  - `pop_back()` direct **$O(1)$** ho jata hai (kyunki `tail->prev` directly available hai).
  - LRU Cache aur browser history implementation ke liye perfect data structure.
- **Cons:**
  - Extra memory overhead (har node par ek extra pointer store hota hai).
  - Har insertion aur deletion mein **char (4) pointers** update karne padte hain instead of two.

---

## 🧱 2. Anatomy of a Doubly Node

```cpp
class Node {
public:
    int data;
    Node* next;
    Node* prev;

    Node(int val) {
        data = val;
        next = nullptr;
        prev = nullptr;
    }
};
```

---

## 🛠️ 3. Step-by-Step Operations & Pointer Mechanics

### Operation 1: `push_front(val)` (Insert at Head)
**Time Complexity:** $O(1)$

**Step-by-step Logic:**
1. Naya node create karo: `Node* newNode = new Node(val);`
2. Agar list empty hai (`head == NULL`):
   - `head = tail = newNode;`
3. Agar list empty nahi hai:
   - `newNode->next = head;`
   - `head->prev = newNode;`
   - `head = newNode;`

```
Before:
newNode [ NULL | 5 | NULL ]
head ──► [ NULL | 10 | next ] ◄══► [ prev | 20 | NULL ]

After Steps:
head ──► [ NULL | 5 | next ] ◄══► [ prev | 10 | next ] ◄══► [ prev | 20 | NULL ]
```

---

### Operation 2: `push_back(val)` (Insert at Tail)
**Time Complexity:** $O(1)$

**Step-by-step Logic:**
1. Naya node banao: `Node* newNode = new Node(val);`
2. Agar list empty hai (`head == NULL`):
   - `head = tail = newNode;`
3. Agar list empty nahi hai:
   - `newNode->prev = tail;`
   - `tail->next = newNode;`
   - `tail = newNode;`

```
After Steps:
... ◄══► [ prev | 20 | next ] ◄══► [ prev | 30 | NULL ] ◄── tail
```

---

### Operation 3: `pop_front()` (Delete from Head)
**Time Complexity:** $O(1)$

**Step-by-step Logic:**
1. Agar list empty hai (`head == NULL`): return.
2. Agar single node hai (`head == tail`):
   - `delete head;`
   - `head = tail = nullptr;`
3. Agar >1 nodes hain:
   - `Node* temp = head;`
   - `head = head->next;`
   - `head->prev = nullptr;` (Naye head ka piche ka link NULL karo)
   - `delete temp;`

---

### Operation 4: `pop_back()` (Delete from Tail)
**Time Complexity:** **$O(1)$** (Compare this to Singly LL which was $O(N)$!)

**Step-by-step Logic:**
1. Agar list empty hai (`head == NULL`): return.
2. Agar single node hai (`head == tail`):
   - `delete head;`
   - `head = tail = nullptr;`
3. Agar >1 nodes hain:
   - `Node* temp = tail;`
   - `tail = tail->prev;` (Directly piche jump kiya!)
   - `tail->next = nullptr;` (Naye tail ka agla link NULL karo)
   - `delete temp;`

```
Before:
... ◄══► [ prev | 20 | next ] ◄══► [ prev | 30 | NULL ] (tail / temp)

Step 1: tail = tail->prev
... ◄══► [ prev | 20 | next ] (tail)

Step 2: tail->next = nullptr; delete temp;
... ◄══► [ prev | 20 | NULL ] (tail)
```

---

## 💻 4. Complete C++ Implementation

```cpp
#include <iostream>
using namespace std;

class Node {
public:
    int data;
    Node* next;
    Node* prev;

    Node(int val) {
        data = val;
        next = nullptr;
        prev = nullptr;
    }
};

class DoublyList {
private:
    Node* head;
    Node* tail;

public:
    DoublyList() {
        head = nullptr;
        tail = nullptr;
    }

    ~DoublyList() {
        Node* curr = head;
        while (curr != nullptr) {
            Node* nextNode = curr->next;
            delete curr;
            curr = nextNode;
        }
        head = tail = nullptr;
    }

    // Insert at front - O(1)
    void push_front(int val) {
        Node* newNode = new Node(val);
        if (head == nullptr) {
            head = tail = newNode;
            return;
        }
        newNode->next = head;
        head->prev = newNode;
        head = newNode;
    }

    // Insert at back - O(1)
    void push_back(int val) {
        Node* newNode = new Node(val);
        if (head == nullptr) {
            head = tail = newNode;
            return;
        }
        newNode->prev = tail;
        tail->next = newNode;
        tail = newNode;
    }

    // Delete at front - O(1)
    void pop_front() {
        if (head == nullptr) {
            cout << "List is empty!\n";
            return;
        }
        Node* temp = head;
        if (head == tail) {
            head = tail = nullptr;
        } else {
            head = head->next;
            head->prev = nullptr;
        }
        delete temp;
    }

    // Delete at back - O(1)
    void pop_back() {
        if (head == nullptr) {
            cout << "List is empty!\n";
            return;
        }
        Node* temp = tail;
        if (head == tail) {
            head = tail = nullptr;
        } else {
            tail = tail->prev;
            tail->next = nullptr;
        }
        delete temp;
    }

    // Print forward - O(N)
    void print_forward() {
        Node* temp = head;
        cout << "Forward:  NULL <-> ";
        while (temp != nullptr) {
            cout << temp->data << " <-> ";
            temp = temp->next;
        }
        cout << "NULL\n";
    }

    // Print backward - O(N)
    void print_backward() {
        Node* temp = tail;
        cout << "Backward: NULL <-> ";
        while (temp != nullptr) {
            cout << temp->data << " <-> ";
            temp = temp->prev;
        }
        cout << "NULL\n";
    }
};

int main() {
    DoublyList dll;
    dll.push_back(10);
    dll.push_back(20);
    dll.push_back(30);
    dll.push_front(5);

    dll.print_forward();
    // Output: Forward:  NULL <-> 5 <-> 10 <-> 20 <-> 30 <-> NULL

    dll.print_backward();
    // Output: Backward: NULL <-> 30 <-> 20 <-> 10 <-> 5 <-> NULL

    dll.pop_front();
    dll.pop_back();

    dll.print_forward();
    // Output: Forward:  NULL <-> 10 <-> 20 <-> NULL
    return 0;
}
```

---

## 🧪 5. Edge Cases & Interview Pitfalls

1. **Single Node Deletion:**
   - Single node delete karte time agar aapne `head = head->next; head->prev = nullptr;` direct kar diya, toh `head` NULL hone ke baad `head->prev` crash kar dega!
   - Hamesha check karo `if (head == tail)` first!
2. **Dangling Pointers:**
   - Jab bhi kisi node ko delete karo, ensure karo ki padosi nodes ke pointers `NULL` ya sahi adjacent node par set ho chuke hon.
3. **Circular Reference Leaks (in GC languages like Java/Python):**
   - Agar references sahi se nullify nahi hue, toh cyclic reference ki wajah se memory leak ho sakti hai.

---

## ⚡ 6. 1-Minute Revision Cheat Sheet

- **Node Structure:** `prev`, `data`, `next`.
- **Key Advantage over Singly LL:** `pop_back()` is **$O(1)$**!
- **All Core Operations:** `push_front`, `push_back`, `pop_front`, `pop_back` $\to$ **All $O(1)$**.
- **Important Invariant:** For any inner node `curr`:
  `curr->next->prev == curr` AND `curr->prev->next == curr`.
