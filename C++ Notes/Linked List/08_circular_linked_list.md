# 📖 Lecture 08: Circular Linked List in Data Structures
> **Video Link:** [Circular Linked List in Data Structures](https://www.youtube.com/watch?v=e6lZY5Yha8U)  
> **Instructor:** Shradha Khapra  
> **Topic:** Circular Linked List (CLL) Mechanics, Tail-Pointer Optimization, Round-Robin Applications

---

## 🎯 1. Concept Ki Baat (Core Intuition)

### What is a Circular Linked List?
Normal linked list mein last node ka `next` pointer `NULL` ko point karta hai.  
Circular Linked List (CLL) mein koi `NULL` pointer nahi hota! **Last node ka `next` wapas pehle node (`head`) ko point karta hai.**

```
          ┌───────────────────────────────────────────────┐
          │                                               │
          ▼                                               │
     ┌────────┬──────┐     ┌────────┬──────┐     ┌────────┴──────┐
head─►  10   │ next ├────►│   20   │ next ├────►│   30   │ next  │
     └────────┴──────┘     └────────┴──────┘     └───────────────┘
                                                        ▲
                                                        │
                                                       tail
```

### 🎮 Real-World Use Cases:
1. **OS Round-Robin Scheduling:** CPU processes ko circular queue mein time slice allocate karta hai. P1 -> P2 -> P3 -> P1...
2. **Multiplayer Board Games:** Turn-based games (Ludo, Monopoly, Uno) jisme har player ke baad automatically agle player ki baari aati hai aur aakhiri ke baad wapas Player 1 ki baari aati hai.
3. **Music Player Loop:** Playlist repeat mode mein gaane khatam hone par wapas first track play hona.

---

## 💡 2. The Pro-Tip: Maintain `tail` instead of `head`!

Interviews mein CLL design karte time sabse smart decision hota hai: **Sirf `tail` pointer maintain karna!**

### Kyun?
Agar humare paas `tail` pointer hai:
- `head` directly mil jata hai: `head = tail->next`!
- Insert at Head: $O(1)$
- Insert at Tail: $O(1)$
- Dono operations $O(1)$ ho jaate hain bina alag se do pointers maintain kiye!

---

## 🛠️ 3. Step-by-Step Operations & Pointer Mechanics

### Operation 1: `insertAtHead(val)`
**Time Complexity:** $O(1)$

**Logic:**
1. Naya node create karo: `Node* newNode = new Node(val);`
2. Agar list empty hai (`tail == NULL`):
   - `tail = newNode;`
   - `tail->next = tail;` (Apne aap ko point karega)
3. Agar list empty nahi hai:
   - `newNode->next = tail->next;` (Naya node puraane head ko point karega)
   - `tail->next = newNode;` (Tail ab naye node ko point karega)

---

### Operation 2: `insertAtTail(val)`
**Time Complexity:** $O(1)$

**Logic:**
Notice karein: Tail par insert karna aur Head par insert karna **lagbhag same** hai!  
Fark sirf itna hai ki tail par insert karne ke baad `tail` pointer ko naye node par move kar diya jata hai:
1. `insertAtHead(val);`
2. `tail = tail->next;`

```
Before:
tail points to [ 30 ] -> [ 10 (head) ]

Step 1: newNode [ 40 ] inserted between 30 and 10
[ 30 (tail) ] ──► [ 40 ] ──► [ 10 (head) ]

Step 2: tail = tail->next (tail becomes 40)
[ 30 ] ──► [ 40 (tail) ] ──► [ 10 (head) ]
```

---

### Operation 3: `deleteHead()`
**Time Complexity:** $O(1)$

**Logic:**
1. Agar list empty hai: return.
2. Agar single node hai (`tail->next == tail`):
   - `delete tail;`
   - `tail = nullptr;`
3. Agar >1 nodes hain:
   - `Node* head = tail->next;`
   - `tail->next = head->next;` (Tail naye head ko point karega)
   - `delete head;`

---

### Operation 4: `print()` (Traversal)
**Time Complexity:** $O(N)$

> ⚠️ **Common Bug in Traversal:** Agar aap `while (temp != head)` likhoge, toh pehli hi line mein loop break ho jayega kyunki `temp` initially `head` hi hota hai!  
> **Solution:** Always use a **`do-while` loop**!

```cpp
void print() {
    if (tail == nullptr) {
        cout << "Empty List\n";
        return;
    }
    Node* temp = tail->next; // Start from head
    do {
        cout << temp->data << " -> ";
        temp = temp->next;
    } while (temp != tail->next);
    cout << "(back to head: " << tail->next->data << ")\n";
}
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

    Node(int val) {
        data = val;
        next = nullptr;
    }
};

class CircularList {
private:
    Node* tail;

public:
    CircularList() {
        tail = nullptr;
    }

    ~CircularList() {
        if (tail == nullptr) return;
        Node* curr = tail->next;
        while (curr != tail) {
            Node* nextNode = curr->next;
            delete curr;
            curr = nextNode;
        }
        delete tail;
        tail = nullptr;
    }

    // Insert at Head - O(1)
    void insertAtHead(int val) {
        Node* newNode = new Node(val);
        if (tail == nullptr) {
            tail = newNode;
            tail->next = tail;
            return;
        }
        newNode->next = tail->next;
        tail->next = newNode;
    }

    // Insert at Tail - O(1)
    void insertAtTail(int val) {
        insertAtHead(val);
        tail = tail->next;
    }

    // Delete Head - O(1)
    void deleteHead() {
        if (tail == nullptr) {
            cout << "List is empty!\n";
            return;
        }
        if (tail->next == tail) { // Single node
            delete tail;
            tail = nullptr;
            return;
        }
        Node* head = tail->next;
        tail->next = head->next;
        delete head;
    }

    // Delete Tail - O(N) for Singly Circular
    void deleteTail() {
        if (tail == nullptr) {
            cout << "List is empty!\n";
            return;
        }
        if (tail->next == tail) {
            delete tail;
            tail = nullptr;
            return;
        }
        // Second last node dhundhna padega
        Node* prev = tail->next;
        while (prev->next != tail) {
            prev = prev->next;
        }
        prev->next = tail->next;
        delete tail;
        tail = prev;
    }

    // Traversal using do-while
    void print() {
        if (tail == nullptr) {
            cout << "List is empty!\n";
            return;
        }
        Node* temp = tail->next;
        do {
            cout << temp->data << " -> ";
            temp = temp->next;
        } while (temp != tail->next);
        cout << "(head)\n";
    }
};

int main() {
    CircularList cll;
    cll.insertAtHead(10);
    cll.insertAtHead(5);
    cll.insertAtTail(20);
    cll.insertAtTail(30);

    cll.print(); // 5 -> 10 -> 20 -> 30 -> (head)

    cll.deleteHead();
    cll.print(); // 10 -> 20 -> 30 -> (head)

    cll.deleteTail();
    cll.print(); // 10 -> 20 -> (head)
    return 0;
}
```

---

## 🧪 5. Edge Cases & Interview Pitfalls

1. **Infinite Traversal Bug:**
   - Normal `while (temp != NULL)` will run **forever**! Hamesha check karo `temp != head`.
2. **Single Node Self-Loop (`tail->next == tail`):**
   - Single node mein `next` pointer apne aap ko point karta hai. Deletion ke waqt is case ko explicitly check karna zaroori hai.
3. **Empty List Insertion:**
   - Empty list mein pehla node insert karte waqt `newNode->next = newNode` banana bhulna sabse common bug hai!

---

## ⚡ 6. 1-Minute Revision Cheat Sheet

- **Definition:** Last node points back to the first node (`head`).
- **Optimal Representation:** Maintain **`tail`** only (`head = tail->next`).
- **Insertion at Head:** $O(1)$.
- **Insertion at Tail:** $O(1)$ (`insertAtHead` then `tail = tail->next`).
- **Traversal:** Always use `do { ... } while (temp != head)`.
- **Use Cases:** Round-robin CPU scheduling, turn-based games, audio playlists.
