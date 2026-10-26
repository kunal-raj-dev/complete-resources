# Stack interview questions and model answers

[Study index](../README.md) · [Practice roadmap](practice_roadmap.md) · [Quick revision](quick_revision.md)

**Scope:** Interview/CP extension and active recall across Lectures 66–75. Prerequisites: read the core chapters first. Try answering aloud before reading each answer.

## Contents

- [1. Foundations and implementation tradeoffs](#1-foundations-and-implementation-tradeoffs)
- [2. Pattern reasoning](#2-pattern-reasoning)
- [3. Minimum stacks and numeric safety](#3-minimum-stacks-and-numeric-safety)
- [4. Geometry and elimination](#4-geometry-and-elimination)
- [5. Explain a solution aloud](#5-explain-a-solution-aloud)
- [6. Follow-up design questions](#6-follow-up-design-questions)

## 1. Foundations and implementation tradeoffs

**1. What is a stack, and what does `pop()` return in C++?**

A stack exposes LIFO insertion/removal at one top end. `std::stack::pop()` returns void; read `top()` before popping if you need the removed value. Both operations require a nonempty stack. Returning -1 for underflow is ambiguous if -1 is a valid stored value; a precondition, exception, or optional result communicates failure more clearly. See [Lecture 66](../lectures/66_introduction_to_stacks.md).

**2. Which implementation would you choose?**

| Implementation | Push | Pop/top | Practical tradeoff |
|---|---|---|---|
| Fixed array | Worst-case O(1) | O(1) | Known capacity; must detect full state |
| Vector, top at back | Amortized O(1), worst O(n) | O(1) for integers | Compact contiguous storage; reallocation |
| Singly linked nodes, top at head | O(1) structural work | O(1) | Allocation and pointer overhead; explicit ownership |
| `std::stack<int>` | Uses underlying container operations | Uses underlying container operations | Clear restricted interface; default deque |

I would normally use `std::stack` for clarity or a vector when direct stack storage/access is useful. A fixed array is useful when capacity is guaranteed; raw nodes are useful to demonstrate ownership, but need careful lifetime handling. These operation costs use the usual RAM model and exclude unbounded allocator/system latency.

**3. Why can a vector push be both O(n) and amortized O(1)?**

One reallocation moves existing items, so one push can cost O(n). Across a sequence, the standard guarantees amortized constant complexity for push_back. The expensive operations are infrequent enough that total work for n pushes is O(n). Amortized analysis is a bound across operations, not an assumption that inputs are random. [Vector specification](https://eel.is/c++draft/vector.modifiers).

**4. Can you retain a reference to a vector stack's top across a push?**

Not safely in general: reallocation invalidates pointers, references, and iterators into the vector. Store a copied value or an index and access again after the push. Even an index requires that insertions/removals do not shift its element. The note implementations return integer values rather than long-lived references.

**5. What is wrong with copying a raw owning head pointer?**

Both copies would believe they own the same nodes. Popping or destroying one makes the other's pointers dangling, and both destructors may delete the same allocation. Implement a deep copy, transfer ownership with a carefully defined move, or disable copying. Our teaching `LinkedStack` disables copy/move and destroys each node once. Destruction is O(n), even though each pop is O(1).

**6. Are an explicit stack and the function call stack the same thing?**

They share LIFO organization, but call frames also retain local state and the return/resume location. Iterative DFS may need a frame containing both vertex and next-neighbor position to reproduce recursive behavior. Replacing recursion does not remove its space requirement; it moves that state into an explicit container. See [DFS frames](additional_stack_applications.md#5-recursion-and-iterative-dfs).

## 2. Pattern reasoning

**7. Why are equal bracket counts insufficient?**

`([)]` has equal counts for every type but invalid nesting. The latest unmatched opener determines what may close next. A stack retains that ordering; a final empty check detects leftover openers. With only one bracket type, a counter can work if every prefix remains nonnegative and the final count is zero. [Lecture 67](../lectures/67_valid_parentheses.md).

**8. Why does stock span pop equal prices?**

Span includes previous consecutive days with price less than **or equal to** today's price. Equal prices belong inside the span, so they must not act as blockers. The remaining blocker is the nearest previous **strictly greater** price; span is `i-blocker`, or `i+1` if none exists. For prices `[6,6]`, spans are `[1,2]`, exposing a mistaken strict-pop implementation. [Lecture 68](../lectures/68_stock_span.md).

**9. What does “next greater” mean?**

The first strictly larger value encountered to the right, not the maximum suffix value. For `[2,4,9]`, the answer for 2 is 4, not 9. A reverse candidate stack removes values `<= current` and then reads top. Equality is invalid, but nearest positional order is preserved. [Lecture 69](../lectures/69_next_greater_element.md).

**10. Why is popping a candidate safe forever?**

For reverse next greater, a larger/equal current value lies closer to every future query on its left than the removed smaller/equal candidate. Whenever the removed value could qualify, the current value also qualifies and is closer. Whenever it cannot qualify, it is irrelevant. This domination argument justifies discarding history; “the stack must be sorted” describes structure but is not a sufficient proof.

**11. Why is a nested while loop linear here?**

Each input occurrence is pushed once and popped at most once. Sum the total stack events rather than multiplying loop bounds mechanically. One iteration can cost O(n), while the entire traversal costs O(n). Auxiliary space may still reach O(n) when no entries are popped.

**12. When must you store indices rather than values?**

When you need distances, rectangle widths, original occurrence identity, or query answers for duplicates. Values alone can suffice for neighbor-value outputs. A map keyed by value works for Next Greater Element I because its reference values are distinct; `[2,3,2,4]` shows why value alone cannot identify both 2 occurrences in a general array. See [representation choices](monotonic_stack_patterns.md#8-choose-the-right-representation).

**13. Does next greater always pop with `<=`?**

That rule belongs to the reverse **candidate** method. A forward **waiting-index** method pops while `a[waiting] < current`, assigning the incoming index as each popped entry's answer. Equality remains unresolved. Always explain what an entry means and what popping does before choosing the comparison.

**14. Why do circular next-greater algorithms make two passes?**

A virtual doubled traversal exposes the suffix followed by the wrapped prefix without physically copying the array. Use modulo n to map virtual positions. In the reverse method, the second copy prepares candidates; record answers for original positions. Pop `<=` so a value cannot match its equal duplicate occurrence, including itself. A singleton has no strictly greater answer. [Lecture 73](../lectures/73_next_greater_element_ii.md).

## 3. Minimum stacks and numeric safety

**15. Why can't one global minimum support arbitrary pops?**

After pushes `[8,3]`, removing 3 must recover 8. A scalar minimum has forgotten that history. Save a minimum per prefix, keep a stack of minima occurrences, or encode transitions reversibly. Scanning after every pop can make an operation O(n). [Lecture 71](../lectures/71_min_stack.md).

**16. How do duplicate minima affect the two-stack solution?**

Push equal minima too, using `x <= minTop`. Otherwise `[5,3,3]` followed by one pop might remove the only saved 3 while another 3 remains in the value stack. A counted `(minimum, frequency)` representation is another option. The pair-per-entry lecture method handles duplicates automatically.

**17. Derive the encoded minimum formulas.**

For a new minimum x below old minimum m, store `e=2*x-m` and set the new minimum to x. Since `e=x+(x-m)<x`, an entry below the current minimum identifies a marker. On marker pop, restore `old=2*current-e`; marker top returns current, not e. LIFO guarantees that later transitions have been undone before an older marker is interpreted.

**18. Is the encoded solution O(1) space or necessarily smaller in bytes?**

It adds O(1) bookkeeping beyond its stack, but n stored entries still cost O(n) total space. A 64-bit marker can occupy the same payload bytes as a pair of two 32-bit integers. Numeric encoding adds complexity and overflow concerns; the pair method is often preferable. Widen before multiplication: `2LL*x`, not `2*x` followed by assignment to a wider variable.

## 4. Geometry and elimination

**19. Derive histogram width without memorizing it.**

If the blocking smaller bars have indices L and R, usable bars are `L+1` through `R-1`, inclusive. Count them: `(R-1)-(L+1)+1 = R-L-1`. Missing blockers sit at -1 and n. For a single bar, width is `1-(-1)-1=1`. [Lecture 72](../lectures/72_largest_rectangle_in_histogram.md).

**20. Why does considering one limiting height per bar find the global rectangle?**

Every rectangle has at least one minimum-height bar in its span. For that bar, nearest strictly smaller boundaries enclose the largest span that can support its height, including the original rectangle. Evaluating every bar therefore includes a candidate at least as good as any feasible rectangle. All candidates are feasible, so the maximum is exact.

**21. Why can histogram use strict smaller boundaries on both sides while subarray sums cannot?**

Histogram takes a maximum, so repeated consideration of the same rectangle is harmless. A sum must count every interval exactly once. For repeated minima, use asymmetric strictness to assign each interval to one equal occurrence. `[2,2]` is the smallest counterexample. [Contribution ownership](additional_stack_applications.md#8-subarray-contributions).

**22. Why does the smaller running maximum determine rainwater?**

If the left known maximum is smaller than the right known maximum, the true right maximum for the left position is already at least that known right wall. The lower limiting level is therefore the left maximum. Unseen middle bars can increase the opposite maximum but cannot invalidate an existing wall. Process the left endpoint and move it inward; the other case is symmetric. [Lecture 74](../lectures/74_trapping_rainwater.md).

**23. Why is celebrity elimination insufficient by itself?**

One lookup proves one of two people impossible, but does not prove the survivor meets every relationship. Inputs without a celebrity still leave one survivor. Verify everyone else knows the candidate and the candidate knows nobody else, ignoring the diagonal. A real celebrity can never be eliminated by either branch. [Lecture 75](../lectures/75_celebrity_problem.md).

**24. How can celebrity be O(n) with an n² matrix?**

The algorithm performs O(n) selected lookups in an already available random-access matrix. Reading or constructing the full input takes O(n²), and input storage is O(n²). Distinguish that input cost from extra algorithmic work. Keeping one running candidate reduces auxiliary storage from O(n) to O(1), while retaining mandatory verification.

## 5. Explain a solution aloud

Use a short sequence with a concrete invariant:

1. **Restate the contract.** “I need the nearest previous price strictly greater than today's because equal prices count in the span.” Clarify values versus indices, circularity, duplicates, and permitted empty inputs.
2. **Give a baseline.** “Scanning backward for every day is quadratic.” Explain what repeated work is being avoided.
3. **Name the stored state.** “The stack contains indices of surviving greater-price candidates, with decreasing prices.”
4. **Justify removal.** “A newer equal/higher price dominates an older lower/equal price for future queries.”
5. **Compute the answer.** “Distance to the remaining blocker is the span; with no blocker all days through today count.”
6. **Prove the cost.** “Each day is pushed once and popped at most once, so total work is linear.”
7. **Test the weak point.** Walk through equal prices and an all-increasing array, then mention output versus auxiliary space.

For a geometry problem, derive the boundary formula on paper. For a stateful class, show how pop restores its previous invariant. For elimination, explicitly separate candidate selection and validation.

## 6. Follow-up design questions

**25. Can all operations have worst-case constant latency?** Fixed-capacity array push/pop/top can, assuming stored-value operations are constant. Vector growth and lazy two-stack queue transfer introduce expensive individual operations. Amortized throughput is not a worst-case latency guarantee. A min stack based on constant-time underlying stack operations does not perform scans.

**26. How would you test without trusting the optimized code?** Write a simple quadratic oracle with a different structure. Enumerate all intervals for histogram/contribution tests, scan for each neighbor, and scan matrix rows/columns for celebrity. Randomize small inputs with many duplicates, then compare. For stateful structures, compare each operation against a vector or deque reference model.

**27. What changes for very large values?** Check every intermediate multiplication and accumulation, not just the final return type. Histogram needs `1LL*height*width`; encoded minima need widened doubling; subarray totals can grow cubically with n times value. An `int` judge interface may be safe under its constraints while a reusable CP function needs a wider type.

**28. How do you distinguish an absent answer from value -1?** An index sentinel -1 is unambiguous for zero-based valid indices. A value result of -1 may be valid input data; a prescribed judge output can intentionally collapse both meanings, while a general API should return an optional value or `(found,value)` pair.

**Self-check:** you are ready when you can derive the inequalities, width, restoration equations, and verification conditions from the invariant without copying code.
