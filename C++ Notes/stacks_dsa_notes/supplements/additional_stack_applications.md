# Additional stack applications

[Study index](../README.md) · [Patterns](monotonic_stack_patterns.md) · [Practice](practice_roadmap.md) · [Interview questions](interview_questions.md)

**Scope:** Interview/CP extension beyond the verified lecture material. Implementations are independently authored C++17. Prerequisites: basic stacks, vectors, strings, recursion, and [histogram boundaries](../lectures/72_largest_rectangle_in_histogram.md). Stack displays run bottom → top.

## Contents

- [1. Postfix expression evaluation](#1-postfix-expression-evaluation)
- [2. Infix and prefix conversion](#2-infix-and-prefix-conversion)
- [3. Stack-based simulation](#3-stack-based-simulation)
- [4. Greedy digit removal](#4-greedy-digit-removal)
- [5. Recursion and iterative DFS](#5-recursion-and-iterative-dfs)
- [6. Queue using two stacks](#6-queue-using-two-stacks)
- [7. Maximal rectangle in a binary matrix](#7-maximal-rectangle-in-a-binary-matrix)
- [8. Subarray contributions](#8-subarray-contributions)
- [9. When a stack is the wrong abstraction](#9-when-a-stack-is-the-wrong-abstraction)

## 1. Postfix expression evaluation

In postfix or Reverse Polish notation (RPN), operands come before the operator: infix `8-(3*2)` becomes `8 3 2 * -`. When an operator arrives, its operands are already available on top of the stack. Parentheses and precedence are encoded by token order.

Pop **right operand first**, then left. Subtraction and division make this essential: `8 3 -` is 5, not -5. Push the combined result, so each stack entry represents a complete subexpression whose internal operations have already been performed.

| Token | Action | Stack |
|---|---|---|
| 8 | Push | `[8]` |
| 3 | Push | `[8,3]` |
| 2 | Push | `[8,3,2]` |
| * | Compute `3*2` | `[8,6]` |
| - | Compute `8-6` | `[2]` |

The [official RPN problem](https://leetcode.com/problems/evaluate-reverse-polish-notation/) uses integer division truncating toward zero and guarantees a valid expression. Our reusable version also rejects operand underflow, invalid number tokens, division by zero, and leftover operands.

**Numeric contract:** tokens parse as `long long`, and every intermediate operation must fit `long long`; in particular, never divide `LLONG_MIN` by -1. These wider inputs are an extension beyond the judge's 32-bit guarantee. The code does not implement arbitrary-precision arithmetic or arithmetic-overflow detection.

```cpp
#include <stack>
#include <stdexcept>
#include <string>
#include <vector>

long long evaluateRPN(const std::vector<std::string>& tokens) {
    std::stack<long long> values;
    for (const std::string& token : tokens) {
        const bool op = token == "+" || token == "-" || token == "*" || token == "/";
        if (!op) {
            std::size_t used = 0;
            const long long number = std::stoll(token, &used);
            if (used != token.size()) throw std::invalid_argument("invalid number");
            values.push(number);
            continue;
        }
        if (values.size() < 2) throw std::invalid_argument("missing operand");
        const long long right = values.top(); values.pop();
        const long long left = values.top(); values.pop();
        if (token == "+") values.push(left + right);
        else if (token == "-") values.push(left - right);
        else if (token == "*") values.push(left * right);
        else {
            if (right == 0) throw std::domain_error("division by zero");
            values.push(left / right);
        }
    }
    if (values.size() != 1) throw std::invalid_argument("invalid expression");
    return values.top();
}
```

Usage: `evaluateRPN({"8","3","2","*","-"})` returns 2; `{"-7","3","/"}` returns -2. For T tokens and B total characters, processing costs O(T+B), assuming bounded-width integer arithmetic; auxiliary stack space O(T), result O(1). Every operand is pushed and every binary operator replaces two entries by one.

## 2. Infix and prefix conversion

Infix is convenient for humans but needs precedence and associativity rules. The **operator stack** postpones operators until their right operands have been emitted to the postfix output. Operands go directly to output. An opening parenthesis creates a boundary; a closing parenthesis drains operators back to that boundary.

The following template expects **pre-tokenized, grammatically valid** expressions with binary `+,-,*,/`, parentheses, and integer/identifier operands. It checks mismatched parentheses but is not a lexer or a full syntax validator. Tokens such as `"-12"` may be supplied as a single numeric operand; a separate unary minus operator is unsupported. Exponentiation is also unsupported.

For left-associative operators, pop prior operators of **greater or equal** precedence. Thus `a-b-c` means `(a-b)-c`. If extending to a right-associative operator such as exponentiation, equal-precedence operators must stay on the stack when the incoming operator is right-associative.

```cpp
#include <stack>
#include <stdexcept>
#include <string>
#include <vector>

std::vector<std::string> infixToPostfix(const std::vector<std::string>& tokens) {
    auto precedence = [](const std::string& s) {
        if (s == "+" || s == "-") return 1;
        if (s == "*" || s == "/") return 2;
        return 0;
    };
    std::stack<std::string> operators;
    std::vector<std::string> output;
    for (const auto& token : tokens) {
        if (token == "(") operators.push(token);
        else if (token == ")") {
            while (!operators.empty() && operators.top() != "(") {
                output.push_back(operators.top()); operators.pop();
            }
            if (operators.empty()) throw std::invalid_argument("unmatched close");
            operators.pop();
        } else if (precedence(token) != 0) {
            while (!operators.empty() && operators.top() != "("
                   && precedence(operators.top()) >= precedence(token)) {
                output.push_back(operators.top()); operators.pop();
            }
            operators.push(token);
        } else output.push_back(token);
    }
    while (!operators.empty()) {
        if (operators.top() == "(") throw std::invalid_argument("unmatched open");
        output.push_back(operators.top()); operators.pop();
    }
    return output;
}
```

**Dry run:** `a + b * ( c - d )`. Each output below is the accumulated postfix token sequence.

| Token | Operator stack | Output |
|---|---|---|
| a | `[]` | `a` |
| + | `[+]` | `a` |
| b | `[+]` | `a b` |
| * | `[+,*]` | `a b` |
| ( | `[+,*,(]` | `a b` |
| c | `[+,*,(]` | `a b c` |
| - | `[+,*,(,-]` | `a b c` |
| d | `[+,*,(,-]` | `a b c d` |
| ) | `[+,*]` | `a b c d -` |
| End | `[]` | `a b c d - * +` |

The invariant is that output preserves completed operand order, while the stack holds operators awaiting completion inside their current parentheses region. Popping an operator with higher/equal precedence finishes a subexpression that must bind before the incoming operator. Each operator is pushed/popped once: O(T+B) time, O(T+B) total token storage including copied strings and output.

**Prefix** places the operator before its operands: the same example becomes `+ a * b - c d`. One straightforward conversion builds complete prefix subexpressions from postfix:

```cpp
#include <stack>
#include <stdexcept>
#include <string>
#include <vector>

std::string postfixToPrefix(const std::vector<std::string>& tokens) {
    std::stack<std::string> expressions;
    for (const auto& token : tokens) {
        const bool op = token == "+" || token == "-" || token == "*" || token == "/";
        if (!op) expressions.push(token);
        else {
            if (expressions.size() < 2) throw std::invalid_argument("missing operand");
            const std::string right = expressions.top(); expressions.pop();
            const std::string left = expressions.top(); expressions.pop();
            expressions.push(token + " " + left + " " + right);
        }
    }
    if (expressions.size() != 1) throw std::invalid_argument("invalid postfix");
    return expressions.top();
}
```

Usage: `postfixToPrefix({"8","3","2","*","-"})` returns `"- 8 * 3 2"`. String rebuilding can take O(BT) worst-case time for a skewed expression, or O(T²) for constant-size tokens. Live expression strings have O(B+T) total characters because they describe disjoint subexpressions. A tree with token nodes followed by preorder traversal avoids repeated concatenation and gives linear output generation.

For evaluating prefix directly, scan right → left and pop **left operand first**, then right. Do not reuse postfix's operand order unchanged.

## 3. Stack-based simulation

Use a stack when the next event interacts with the most recent surviving event. In [Asteroid Collision](https://leetcode.com/problems/asteroid-collision/), positive values move right and negative values move left; magnitude is size. Only a positive survivor immediately to the left of an incoming negative asteroid can collide. Two left-moving asteroids, two right-moving asteroids, or `[-3,5]` move without a collision.

```cpp
#include <vector>

std::vector<int> asteroidCollision(const std::vector<int>& asteroids) {
    std::vector<int> alive; // Nonzero inputs; vector used as a stack.
    for (int current : asteroids) {
        bool survives = true;
        while (survives && current < 0 && !alive.empty() && alive.back() > 0) {
            const long long incomingSize = -static_cast<long long>(current);
            if (alive.back() < incomingSize) alive.pop_back();
            else if (alive.back() == incomingSize) {
                alive.pop_back(); survives = false;
            } else survives = false;
        }
        if (survives) alive.push_back(current);
    }
    return alive;
}
```

For `[5,10,-12,4,-4]`, survivors evolve `[5]`, `[5,10]`, `[-12]`, `[-12,4]`, `[-12]`. The -12 destroys 10 and then 5; 4 and -4 destroy each other. Cast **before** negating so an extended input `INT_MIN` is handled safely.

Invariant: the stored survivors have no unresolved collision with each other. Only their rightmost positive asteroid can meet the incoming negative one first. Removing a destroyed survivor exposes the next possible collision. Each asteroid is appended at most once and removed at most once, so O(n) time; auxiliary live stack O(n), returned survivor output O(n), using the same vector as both.

Similar simulation uses include undo histories, browser back navigation, nested directory processing, and removing adjacent equal characters. Identify what an entry represents and when it is irrevocably resolved before choosing a stack.

## 4. Greedy digit removal

[Remove K Digits](https://leetcode.com/problems/remove-k-digits/) asks for the smallest number after deleting exactly k digits while retaining the order of the others. Assume a nonempty decimal string and `0 <= k <= length`.

Earlier digits dominate numerical order after normalizing leading zeros. If the last kept digit is greater than the incoming digit and deletions remain, deleting that last digit improves the earliest available position. Repeatedly do this with a stack. If deletions remain after the scan, remove trailing digits; no improving descent remains.

```cpp
#include <string>

std::string removeKdigits(const std::string& number, int k) {
    std::string kept;
    for (char digit : number) {
        while (k > 0 && !kept.empty() && kept.back() > digit) {
            kept.pop_back(); --k;
        }
        kept.push_back(digit);
    }
    while (k > 0) { kept.pop_back(); --k; }
    const auto first = kept.find_first_not_of('0');
    return first == std::string::npos ? "0" : kept.substr(first);
}
```

For `"3521", k=2`: keep `[3]`; then `[3,5]`; incoming 2 removes 5 and 3, leaving `[2]` with k=0; append 1 to produce `"21"`. Equal digits do not force a pop: deleting an equal digit yields no immediate improvement. Once k is exhausted, the remaining stack need not be monotonic.

An exchange argument proves correctness: at a descending adjacent kept pair, deleting the larger earlier digit yields a lexicographically smaller fixed-length remaining sequence than retaining it and spending that deletion later. Repeating safe exchanges builds an optimal sequence; any unused deletions should come from the suffix. Each digit pushes/pops once: O(n) time, O(n) working space, O(n) output space.

## 5. Recursion and iterative DFS

A recursive call stack stores more than a node: it retains local variables and **where execution resumes**. In recursive DFS, after exploring one neighbor, the call resumes at the next neighbor. To reproduce the exact recursive visiting order, keep frames `(vertex, next-neighbor position)`.

The following function visits only vertices reachable from `start`, follows adjacency-list order, and assumes all neighbor indices are valid. An invalid start returns empty output. A visited array prevents cycles from generating repeated calls.

```cpp
#include <cstddef>
#include <vector>

std::vector<int> dfsOrder(const std::vector<std::vector<int>>& adjacency, int start) {
    const int n = static_cast<int>(adjacency.size());
    if (start < 0 || start >= n) return {};
    struct Frame { int vertex; std::size_t next; };
    std::vector<Frame> frames;
    std::vector<bool> visited(n, false);
    std::vector<int> order;
    visited[start] = true;
    order.push_back(start);
    frames.push_back({start, 0});
    while (!frames.empty()) {
        const int vertex = frames.back().vertex;
        if (frames.back().next == adjacency[vertex].size()) {
            frames.pop_back();
            continue;
        }
        const int neighbor = adjacency[vertex][frames.back().next++];
        if (!visited[neighbor]) {
            visited[neighbor] = true;
            order.push_back(neighbor);
            frames.push_back({neighbor, 0});
        }
    }
    return order;
}
```

For adjacency `0:[1,2], 1:[3], 2:[3], 3:[]`, entry order is `[0,1,3,2]`. After entering 3 the frame path is `[0:1,1:1,3:0]`; completing 3 and 1 resumes 0 at neighbor 2. The already visited 3 is skipped from vertex 2.

Invariant: frames represent the current recursive path, and each `next` field identifies the first unexplored neighbor. Push corresponds to a recursive call; pop corresponds to return. No reference to `frames.back()` is retained across `push_back`, which might reallocate the vector.

Worst-case O(V+E) time, O(V) auxiliary storage including visited and frames, O(V) output. Explicit storage avoids dependence on the process's recursion-depth limit. For a whole-graph traversal, start another DFS at each unvisited vertex, **sharing** one visited array.

A shorter version pushes vertices alone and reverses neighbor order, but the choice of marking on push versus pop can change visiting order on graphs with cross edges. Use frames when exact recursive order, postorder, or enter/exit events matter. A simple unweighted shortest-path search needs a queue and BFS rather than DFS.

## 6. Queue using two stacks

A queue removes the oldest entry; a stack exposes the newest. Keep `incoming` for newly enqueued values and `outgoing` for removal. Transfer all values from incoming to outgoing **only when outgoing is empty**. Reversal brings the oldest incoming entry to the top of outgoing.

```cpp
#include <stack>
#include <stdexcept>

class TwoStackQueue {
    std::stack<int> incoming, outgoing;
    void prepareFront() {
        if (outgoing.empty()) {
            while (!incoming.empty()) {
                outgoing.push(incoming.top()); incoming.pop();
            }
        }
        if (outgoing.empty()) throw std::underflow_error("empty queue");
    }
public:
    bool empty() const { return incoming.empty() && outgoing.empty(); }
    void push(int value) { incoming.push(value); }
    int front() { prepareFront(); return outgoing.top(); }
    void pop() { prepareFront(); outgoing.pop(); }
};
```

Push 1 and 2: incoming `[1,2]`, outgoing `[]`. Calling front transfers to outgoing `[2,1]`, returning 1. Pop leaves outgoing `[2]`. Push 3 adds incoming `[3]`; front is still 2. After popping 2, the next front transfers 3 and returns 3.

Invariant: outgoing contains the older queue segment in reverse stack order; incoming contains the newer segment in insertion order. Transferring while outgoing still holds old values would put new values before them and break FIFO.

Push has O(1) underlying stack work. One front/pop may transfer O(n) entries, but every entry crosses from incoming to outgoing at most once and is finally popped at most once. Thus each queue operation is amortized O(1), with O(n) live storage. Front mutates the internal representation although it leaves the logical queue unchanged. See [the official queue problem](https://leetcode.com/problems/implement-queue-using-stacks/) for the judge's `peek` naming.

## 7. Maximal rectangle in a binary matrix

For [Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/), update a histogram for each row: height at a column is the number of consecutive 1s ending at that row. A 0 resets the height. Solve a histogram after every row.

Every all-1 rectangle has some bottom row. At that row, every column in its width has accumulated height at least the rectangle's height, so the histogram contains it. Conversely, a histogram rectangle at a row corresponds to an all-1 rectangle ending at that row. Taking the maximum across rows is therefore exact.

```cpp
#include <algorithm>
#include <stack>
#include <string>
#include <vector>

long long maximalRectangle(const std::vector<std::string>& matrix) {
    if (matrix.empty()) return 0;
    const int columns = static_cast<int>(matrix[0].size());
    std::vector<int> height(columns, 0);
    long long answer = 0;
    // Precondition: rectangular matrix containing only '0' and '1'.
    for (const auto& row : matrix) {
        for (int j = 0; j < columns; ++j)
            height[j] = row[j] == '1' ? height[j] + 1 : 0;
        std::stack<int> bars;
        for (int j = 0; j <= columns; ++j) {
            while (!bars.empty() && (j == columns || height[bars.top()] >= height[j])) {
                const int bar = bars.top(); bars.pop();
                const int left = bars.empty() ? -1 : bars.top();
                answer = std::max(answer, 1LL * height[bar] * (j - left - 1));
            }
            if (j < columns) bars.push(j);
        }
    }
    return answer;
}
```

| Row | Histogram after row | Best at this bottom row | Running maximum |
|---|---|---|---|
| `101` | `[1,0,1]` | 1 | 1 |
| `111` | `[2,1,2]` | 3 | 3 |
| `011` | `[0,2,3]` | 4 | 4 |

Usage: `maximalRectangle({"101","111","011"})` returns 4. The helper uses a virtual end position to flush unresolved bars without indexing past the height array. Equal bars can be popped; a later equal bar retains the plateau's larger possible width. With R rows and C columns, time O(RC), auxiliary space O(C), result O(1). The input matrix is excluded from auxiliary space.

## 8. Subarray contributions

Enumerating all subarrays costs O(n²). Instead, ask how many subarrays choose index i as their minimum. Choose the **rightmost** occurrence when multiple equal minima appear.

Let L[i] be previous strictly smaller index, or -1. Let R[i] be next smaller-or-equal index, or n. A subarray owned by i starts at any position in `L+1..i` and ends at any position in `i..R-1`:

```text
number of owned subarrays = (i-L[i]) * (R[i]-i)
minimum contribution     = a[i] * (i-L[i]) * (R[i]-i)
```

Crossing L would introduce a smaller value. Crossing R would introduce a smaller value or a later equal minimum, changing ownership. Inside the permitted range, i is a minimum and is the rightmost occurrence of that minimum. Each nonempty subarray has exactly one rightmost minimum, so the sum counts it exactly once.

**Worked example:** `[2,2]` has subarrays `[2]` at index 0, `[2]` at index 1, and `[2,2]`. Boundaries L=`[-1,-1]`, R=`[1,2]`; counts are 1 and 2, contributions 2 and 4, total 6. Symmetric strict boundaries would count `[2,2]` twice.

The [Sum of Subarray Minimums statement](https://leetcode.com/problems/sum-of-subarray-minimums/) requests the answer modulo 1,000,000,007. Under its limits (`n <= 30000`, positive `a[i] <= 30000`), each individual unreduced 64-bit contribution is safe.

```cpp
#include <stack>
#include <vector>

long long sumSubarrayMinimums(const std::vector<int>& a) {
    constexpr long long mod = 1000000007LL;
    const int n = static_cast<int>(a.size());
    std::vector<int> left(n, -1), right(n, n);
    std::stack<int> indices;
    for (int i = 0; i < n; ++i) {
        while (!indices.empty() && a[indices.top()] >= a[i]) indices.pop();
        if (!indices.empty()) left[i] = indices.top();
        indices.push(i);
    }
    while (!indices.empty()) indices.pop();
    for (int i = n - 1; i >= 0; --i) {
        while (!indices.empty() && a[indices.top()] > a[i]) indices.pop();
        if (!indices.empty()) right[i] = indices.top();
        indices.push(i);
    }
    long long answer = 0;
    for (int i = 0; i < n; ++i) {
        const long long count = 1LL * (i - left[i]) * (right[i] - i);
        answer = (answer + count * a[i]) % mod;
    }
    return answer;
}
```

Usage: `{2,2}` returns 6; `{3,1,2}` returns 9 (minima `3,1,2,1,1,1`). Time O(n), auxiliary space O(n), scalar result O(1). For arbitrary larger n and values, reduce factors before multiplying or use an appropriate wider arithmetic strategy; merely applying modulo **after** an overflowing product does not fix overflow.

For [Sum of Subarray Ranges](https://leetcode.com/problems/sum-of-subarray-ranges/), each range is `maximum - minimum`. Compute the total contributions of maxima and minima separately and subtract. Maxima use previous **strictly greater**, next **greater-or-equal** under the same rightmost ownership convention.

```cpp
#include <stack>
#include <vector>

long long extremaContributions(const std::vector<int>& a, bool minima) {
    const int n = static_cast<int>(a.size());
    std::vector<int> left(n, -1), right(n, n);
    std::stack<int> indices;
    for (int i = 0; i < n; ++i) {
        while (!indices.empty() && (minima ? a[indices.top()] >= a[i]
                                           : a[indices.top()] <= a[i])) indices.pop();
        if (!indices.empty()) left[i] = indices.top();
        indices.push(i);
    }
    while (!indices.empty()) indices.pop();
    for (int i = n - 1; i >= 0; --i) {
        while (!indices.empty() && (minima ? a[indices.top()] > a[i]
                                           : a[indices.top()] < a[i])) indices.pop();
        if (!indices.empty()) right[i] = indices.top();
        indices.push(i);
    }
    long long total = 0;
    for (int i = 0; i < n; ++i)
        total += 1LL * a[i] * (i - left[i]) * (right[i] - i);
    return total;
}

long long sumSubarrayRanges(const std::vector<int>& a) {
    return extremaContributions(a, false) - extremaContributions(a, true);
}
```

This signed code supports negative values and assumes the exact intermediate totals fit `long long`; the referenced range problem's `n <= 1000`, `|a[i]| <= 10^9` satisfies that bound. Usage: `{1,3,2}` returns 5: singleton ranges are 0, pair ranges are 2 and 1, and the full range is 2. Time O(n), auxiliary space O(n), result O(1).

## 9. When a stack is the wrong abstraction

Nearest positional comparisons suit a monotonic stack; sliding-window extrema with expired indices usually suit a deque. FIFO processing suits a queue. Repeated arbitrary minimum removal suits a heap. Random access to every element suits a vector. A stack is useful when the most recent unresolved state is exactly the next state that should be handled.

**Revision:** evaluation stores completed values; conversion stores pending operators; simulation stores survivors; DFS stores paused calls; a two-stack queue reverses order lazily; matrix rectangles reduce to histograms; contribution problems require explicit duplicate ownership.
