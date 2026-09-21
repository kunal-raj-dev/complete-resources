# 💼 Topic 15 Interview Question Bank: Stacks

> **Curated FAANG Interview Bank:** High-frequency technical questions, value encoding proofs, and monotonic stack variations.

---

## 📌 Conceptual & Architectural Questions

### Q1: How do you identify when a problem requires a Monotonic Stack?
**Answer:** Look for "nearest greater/smaller element to the left or right" queries on an array, or problems where a candidate element's utility is terminated by a larger or smaller subsequent element. Common keywords include: Largest Rectangle, Water Trapping, Stock Span, Daily Temperatures, Building Views.

### Q2: How does $2x - \text{minVal}$ allow Min Stack to achieve $O(1)$ space without a second stack?
**Answer:** It's an algebraic encoding trick. When a new minimum $x$ is pushed ($x < \text{minVal}$), storing $2x - \text{minVal}$ creates a value *strictly smaller* than $x$ because $x - \text{minVal} < 0 \Rightarrow x + (x - \text{minVal}) < x$. When reading `top()`, any value less than the current `minVal` indicates that `minVal` itself is the real top element. When popping, the previous minimum is mathematically recovered via $2 \cdot \text{minVal} - \text{encoded\_topVal}$.

### Q3: What is the difference between an Infix, Prefix, and Postfix expression?
**Answer:**
- **Infix:** Operators between operands (`A + B`). Requires operator precedence and parentheses to resolve ambiguity.
- **Postfix (Reverse Polish Notation):** Operators follow operands (`A B +`). Evaluated in a single left-to-right pass using a stack without needing parentheses.
- **Prefix (Polish Notation):** Operators precede operands (`+ A B`). Evaluated right-to-left using a stack.

### Q4: Why are Stacks used to evaluate Postfix expressions, and how does it work?
**Answer:** Stacks naturally model the "last-in, first-out" evaluation required by postfix. You read left-to-right: push numbers onto the stack. When you encounter an operator, you pop the top two numbers, apply the operator, and push the result back onto the stack. The final remaining number is the answer.

### Q5: How do you implement a Queue using two Stacks?
**Answer:** Use an `input` stack and an `output` stack.
- **Push:** Always push to the `input` stack. $O(1)$.
- **Pop/Peek:** If `output` is empty, pop all elements from `input` and push them into `output` (reversing their order to FIFO). Then pop/peek from `output`. Amortized $O(1)$.

### Q6: How do you implement a Stack using Queues?
**Answer:** Use a single Queue.
- **Push:** Push the new element to the back of the queue. Then, pop the previous $N-1$ elements from the front of the queue and push them immediately back to the rear of the queue. This rotates the new element to the front! $O(N)$ push, $O(1)$ pop.

### Q7: Why is a Monotonic Stack $O(N)$ when there's a `while` loop inside a `for` loop?
**Answer:** Time complexity is determined by the total number of operations, not the loop nesting depth. In a Monotonic Stack, every element is pushed onto the stack exactly once. Therefore, it can only be popped exactly once. The `while` loop pops elements. Across the entire `for` loop, the `while` loop runs at most $N$ times total. $O(N) + O(N) = O(N)$.

### Q8: In the Largest Rectangle in Histogram problem, why must we flush the stack at the end?
**Answer:** If the array contains a strictly increasing sequence (e.g., `[1, 2, 3, 4]`), the `while` loop condition (`currentHeight < stack.top()`) is never met. The array finishes processing but all indices are stuck in the stack, computing no areas. Flushing the stack (often by simulating a final bar of height 0) forces all pending rectangles to calculate their widths to the end of the array.

### Q9: Explain the difference between Next Greater Element and Next Greater Element II (Circular Array).
**Answer:** Standard NGE scans the array once (or builds the stack once backwards). NGE II implies the array wraps around, meaning the NGE for the last element might be the first element. To solve it, we simulate concatenating the array to itself (length $2N$) using modulo arithmetic `i % N`, ensuring every element gets a full $N-1$ lookahead.

### Q10: Why do we use a Decreasing Stack for Next Greater Element?
**Answer:** We want to find the next element that is *larger*. If we push elements that are decreasing (e.g., `5, 4, 3`), they are all waiting for a larger element. When an `8` arrives, it is greater than `3, 4, 5`. The `8` pops them all, serving as the "Next Greater Element" for every single one of them simultaneously.

### Q11: What is the "Celebrity Problem" and why is it optimally solved with Two Pointers instead of a Stack?
**Answer:** The Celebrity Problem finds a person who knows nobody, but everyone knows them. The Stack approach pushes all $N$ people, pops two, asks if A knows B, eliminates one, and pushes the survivor back. It takes $O(N)$ space. The Two-Pointer approach (`left=0`, `right=N-1`) asks the same question and increments/decrements pointers, achieving the exact same tournament elimination in $O(1)$ auxiliary space.

### Q12: How do you sort a stack using only one other stack?
**Answer:** You have an `input` stack and a `temp` stack.
1. Pop `val` from `input`.
2. While `temp` is not empty and `temp.top() > val`, pop `temp` and push back to `input`.
3. Push `val` to `temp`.
4. Repeat until `input` is empty. The `temp` stack is now sorted. Time: $O(N^2)$.

---

## 💻 Debugging & Trace Challenges

### Q13: [Debugging] Why does this standard Next Greater Element code SegFault?
```cpp
while (nums[i] > nums[st.top()]) {
    nge[st.top()] = nums[i];
    st.pop();
}
```
**Answer:** It lacks the `!st.empty()` check in the while loop condition. If the stack becomes empty, calling `st.top()` attempts to access invalid memory and causes a Segmentation Fault. It must be `while (!st.empty() && nums[i] > nums[st.top()])`.

### Q14: [Output Prediction] Trace this string through the standard Valid Parentheses algorithm: `([)]`
**Answer:**
1. `(`: Push `)`. Stack: `[)]`
2. `[`: Push `]`. Stack: `[), ]]`
3. `)`: Current char `)` does NOT match `st.top()` which is `]`.
4. Returns `false` immediately. The string is improperly nested.

### Q15: [Conceptual Bug] In Trapping Rainwater, what happens if we use a strict `<` instead of `<=` in the Monotonic Stack condition?
**Answer:** If we use `while (height[i] < height[st.top()])`, consecutive bars of the *same* height will not be popped. The stack will contain duplicates. While this might accidentally calculate water correctly (adding `0` area strips), it fundamentally violates the "Strictly Decreasing" property of the stack, unnecessarily increasing peak memory usage and complicating width calculations.
