# 📖 Lecture 01: Introduction to Linked List | Data Structures & Algorithms
> **Video Link:** [Introduction to Linked List | Data Structures & Algorithms](https://www.youtube.com/watch?v=LyuuqCVkP5I)  
> **Instructor:** Shradha Khapra  
> **Topic:** Fundamental Linked List Concepts, Memory Anatomy, Class Design & Complete Implementation

---

## 🎯 1. Concept Ki Baat (Core Intuition)

### Why Linked List when we already have Arrays / Vectors?
Arrays memory mein **contiguous (lagaataar)** block allocate karte hain. 
- Agar hume array ka size badhana ho aur aage memory block khali na ho, toh naya bada array banakar pura data copy karna padta hai ($O(N)$ overhead).
- Array ke start ya middle mein element insert/delete karne ke liye baaki sabhi elements ko **shift** karna padta hai ($O(N)$).

**Linked List ka Solution:**
Linked List ek **linear data structure** hai jisme elements memory mein scattered (alag-alag jagah) hote hain. Har element (jise hum **Node** kehte hain) apne paas:
1. Apna **Data** rakhta hai.
2. Agle node ka **Address/Pointer** (`next`) rakhta hai.

```
Array (Contiguous Memory):
[ 10 | 20 | 30 | 40 ]  -> Blocks are strictly adjacent: 0x100, 0x104, 0x108...

Linked List (Non-Contiguous Memory):
[ 10 | 0x350 ] ---> [ 20 | 0x120 ] ---> [ 30 | 0x890 ] ---> [ 40 | NULL ]
   @ 0x100             @ 0x350             @ 0x120             @ 0x890
```

---

## ⚖️ 2. Array vs Linked List Comparison Table

| Parameter | Array / Vector | Linked List |
|---|---|---|
| **Memory Allocation** | Contiguous (Lagaataar) | Non-contiguous (Scattered) |
| **Size** | Fixed (Vector internally doubles) | Completely Dynamic |
| **Access Time** | $O(1)$ via index (`arr[i]`) | $O(N)$ (Traverse from `head`) |
| **Insertion at Beginning** | $O(N)$ (Shifting required) | $O(1)$ (Direct pointer change) |
| **Insertion at End** | $O(1)$ amortized | $O(1)$ (with `tail` pointer) |
| **Deletion at Beginning** | $O(N)$ (Shifting required) | $O(1)$ |
| **Memory Overhead** | Kam (Only data) | Zyada (Data + 4/8 bytes for pointer per node) |
| **Cache Friendliness** | Bahut High (Spatial Locality) | Kam (Cache misses occur) |

---

## 🧱 3. Anatomy of a Node

Har Node C++ mein ek `class` ya `struct` se represent hota hai:

```cpp
class Node {
public:
    int data;       // Value stored in the node
    Node* next;     // Pointer to the next Node

    // Constructor
    Node(int val) {
        data = val;
        next = nullptr;
    }
};
```

---

## ⚙️ 4. Linked List Class Design (Head & Tail)

Ek standard Linked List class do main pointers maintain karti hai:
- `head`: First node ka pointer.
- `tail`: Last node ka pointer.

```
       head                                                 tail
         │                                                    │
         ▼                                                    ▼
    ┌────────┬──────┐     ┌────────┬──────┐     ┌────────┬──────┐
    │  data  │ next ├────►│  data  │ next ├────►│  data  │ NULL │
    └────────┴──────┘     └────────┴──────┘     └────────┴──────┘
```

---

## 🛠️ 5. Step-by-Step Operations & Pointer Mechanics

### Operation 1: `push_front(val)` (Insert at Head)
**Time Complexity:** $O(1)$

**Step-by-step Logic:**
1. Naya node banao: `Node* newNode = new Node(val);`
2. Agar list empty hai (`head == NULL`):
   - `head = tail = newNode;`
3. Agar list empty nahi hai:
   - Naye node ka `next` puraane `head` par point karao: `newNode->next = head;`
   - `head` ko aage move karke `newNode` bana do: `head = newNode;`

```
Before:
newNode [ 5 | NULL ]
head ──► [ 10 | next ] ──► [ 20 | NULL ]

Step 1: newNode->next = head
newNode [ 5 |  • ] ──┐
                     ▼
head ──────────────► [ 10 | next ] ──► [ 20 | NULL ]

Step 2: head = newNode
head ──► [ 5 | next ] ──► [ 10 | next ] ──► [ 20 | NULL ]
```

---

### Operation 2: `push_back(val)` (Insert at Tail)
**Time Complexity:** $O(1)$ (with `tail` pointer)

**Step-by-step Logic:**
1. Naya node banao: `Node* newNode = new Node(val);`
2. Agar list empty hai (`head == NULL`):
   - `head = tail = newNode;`
3. Agar list empty nahi hai:
   - Puraane tail ka `next` naye node par point karao: `tail->next = newNode;`
   - `tail` ko update karke `newNode` bana do: `tail = newNode;`

```
Before:
[ 10 | next ] ──► [ 20 | NULL (tail) ]       newNode [ 30 | NULL ]

Step 1: tail->next = newNode
[ 10 | next ] ──► [ 20 |  • ] ──────────────► [ 30 | NULL ] (newNode)
                         tail

Step 2: tail = newNode
[ 10 | next ] ──► [ 20 | next ] ─────────────► [ 30 | NULL (tail) ]
```

---

### Operation 3: `pop_front()` (Delete from Head)
**Time Complexity:** $O(1)$

**Step-by-step Logic:**
1. Agar list empty hai (`head == NULL`): Print "List is empty" and return.
2. `temp` pointer banao jo current `head` ko point kare: `Node* temp = head;`
3. `head` ko agle node par move karo: `head = head->next;`
4. Puraane head ko memory se delete karo: `delete temp;`
5. Agar delete karne ke baad list empty ho gayi (`head == NULL`), toh `tail = NULL;` bhi set karo.

---

### Operation 4: `pop_back()` (Delete from Tail)
**Time Complexity:** $O(N)$
> ⚠️ **Important Interview Question:** Agar humare paas `tail` pointer hai, tab bhi `pop_back` $O(N)$ kyu leta hai?  
> **Answer:** Singly Linked List mein backward arrow nahi hota! Last node ko delete karne ke baad naya `tail` banega **second-last node**. Aur second-last node tak pahuchne ke liye hume `head` se pura traverse karna hi padega!

**Step-by-step Logic:**
1. Agar list empty hai (`head == NULL`): return.
2. Agar sirf 1 node hai (`head == tail`):
   - `delete head;`
   - `head = tail = nullptr;`
3. Agar >1 nodes hain:
   - Puraane list mein traverse karo jab tak `temp->next != tail` (second last node).
   - `delete tail;`
   - `tail = temp;`
   - `tail->next = nullptr;`

---

### Operation 5: `insert(val, pos)` (Insert at Position `pos` 0-indexed)
**Time Complexity:** $O(N)$ (Traversal to position)

**Step-by-step Logic:**
1. Agar `pos == 0`: Call `push_front(val);`
2. List mein `pos - 1` position tak traverse karo ek pointer `temp` ke saath.
3. Agar `temp == NULL`: Position out of bounds!
4. Naya node banao: `Node* newNode = new Node(val);`
5. `newNode->next = temp->next;`
6. `temp->next = newNode;`

```
Traverse till (pos - 1) node:
[ Node A (temp) ] ──────────────► [ Node B ]
        │                             ▲
        │ 1. newNode->next = temp->next
        ▼                             │
   [ newNode ] ───────────────────────┘
   
2. temp->next = newNode:
[ Node A ] ──► [ newNode ] ──► [ Node B ]
```

---

### Operation 6: `search(key)` (Linear Search)
**Time Complexity:** $O(N)$

```cpp
int search(int key) {
    Node* temp = head;
    int idx = 0;
    while (temp != nullptr) {
        if (temp->data == key) return idx;
        temp = temp->next;
        idx++;
    }
    return -1; // Not found
}
```

---

## 💻 6. Complete C++ Implementation

```cpp
#include <iostream>
using namespace std;

class Node {
public:
    int data;
    Node* next;

    Node(int val) {
        data = val;
        next = nullptr;
    }
};

class List {
private:
    Node* head;
    Node* tail;

public:
    List() {
        head = nullptr;
        tail = nullptr;
    }

    // Destructor to free dynamically allocated heap memory
    ~List() {
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
        head = newNode;
    }

    // Insert at back - O(1)
    void push_back(int val) {
        Node* newNode = new Node(val);
        if (head == nullptr) {
            head = tail = newNode;
            return;
        }
        tail->next = newNode;
        tail = newNode;
    }

    // Delete at front - O(1)
    void pop_front() {
        if (head == nullptr) {
            cout << "List is already empty!\n";
            return;
        }
        Node* temp = head;
        head = head->next;
        delete temp;
        if (head == nullptr) {
            tail = nullptr;
        }
    }

    // Delete at back - O(N)
    void pop_back() {
        if (head == nullptr) {
            cout << "List is already empty!\n";
            return;
        }
        if (head == tail) {
            delete head;
            head = tail = nullptr;
            return;
        }
        Node* prev = head;
        while (prev->next != tail) {
            prev = prev->next;
        }
        delete tail;
        tail = prev;
        tail->next = nullptr;
    }

    // Insert at index pos - O(N)
    void insert(int val, int pos) {
        if (pos < 0) {
            cout << "Invalid Position!\n";
            return;
        }
        if (pos == 0) {
            push_front(val);
            return;
        }

        Node* temp = head;
        for (int i = 0; i < pos - 1; i++) {
            if (temp == nullptr) {
                cout << "Position out of bounds!\n";
                return;
            }
            temp = temp->next;
        }

        if (temp == nullptr) {
            cout << "Position out of bounds!\n";
            return;
        }

        Node* newNode = new Node(val);
        newNode->next = temp->next;
        temp->next = newNode;

        if (newNode->next == nullptr) {
            tail = newNode;
        }
    }

    // Search key in list - O(N)
    int search(int key) {
        Node* temp = head;
        int idx = 0;
        while (temp != nullptr) {
            if (temp->data == key) return idx;
            temp = temp->next;
            idx++;
        }
        return -1;
    }

    // Print all nodes - O(N)
    void print() {
        Node* temp = head;
        while (temp != nullptr) {
            cout << temp->data << " -> ";
            temp = temp->next;
        }
        cout << "NULL\n";
    }
};

int main() {
    List ll;
    ll.push_front(3);
    ll.push_front(2);
    ll.push_front(1);
    ll.print(); // Output: 1 -> 2 -> 3 -> NULL

    ll.push_back(4);
    ll.push_back(5);
    ll.print(); // Output: 1 -> 2 -> 3 -> 4 -> 5 -> NULL

    ll.insert(99, 2);
    ll.print(); // Output: 1 -> 2 -> 99 -> 3 -> 4 -> 5 -> NULL

    ll.pop_front();
    ll.print(); // Output: 2 -> 99 -> 3 -> 4 -> 5 -> NULL

    ll.pop_back();
    ll.print(); // Output: 2 -> 99 -> 3 -> 4 -> NULL

    cout << "Index of 99: " << ll.search(99) << "\n"; // 1
    return 0;
}
```

---

## 🧪 7. Edge Cases & Interview Pitfalls

1. **Empty List Operations:**
   - Hamesha check karo `head == nullptr` pehle, warna `head->next` access karne par **Segmentation Fault (Crash)** hoga.
2. **Single Node Deletion:**
   - Jab list mein sirf ek node ho aur use delete kiya jaye, toh `head` aur `tail` dono ko `nullptr` banana zaroori hai.
3. **Memory Leaks:**
   - C++ mein `new` se allocate kiya gaya har node heap memory par banta hai. Agar use `delete` nahi kiya, toh memory leak hota hai. Hamesha Destructor likhna chahiye.
4. **Tail Pointer Invalidation:**
   - Jab last node par insert ya delete karo, toh ensure karo ki `tail` pointer sahi node ko point kare.

---

## ⚡ 8. 1-Minute Revision Cheat Sheet

- **Node = Data + Pointer to Next Node**
- **Head** = Pehla node, **Tail** = Aakhiri node (jiska next NULL hota hai).
- `push_front`: $O(1)$
- `push_back`: $O(1)$ with `tail`
- `pop_front`: $O(1)$
- `pop_back`: $O(N)$ (because second last node search karni padti hai)
- `search`: $O(N)$
- `insert(pos)`: $O(N)$
