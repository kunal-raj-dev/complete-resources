# ⚡ JavaScript Notes — Complete Curriculum & Study Guide

> **Curriculum Source:** Anurag Singh — *Complete JavaScript Course (ProCodrr)*  
> **Total Lectures Covered:** **68 Comprehensive In-Depth Lectures (Ep. 01 → Ep. 68)**  
> **Modules Included:**  
> - **Module 01: Core JavaScript Fundamentals (Ep. 01 – Ep. 25)**  
> - **Module 02: Advanced Loops, Execution Context, Scopes, Closures, Functional Patterns & ES6+ (Ep. 26 – Ep. 50)**  
> - **Module 03: DOM, Modern Events Architecture & Web Storage (Ep. 51 – Ep. 68)**  
> **Language & Standard:** 100% Technical English | ECMAScript 2024+ & WHATWG DOM Standard  

---

## 📖 Master Index & Comprehensive Guide

👉 **[Open Complete 68-Episode Master Curriculum Index (`00-master-index.md`)](./00-master-index.md)**  
*(Includes 8-Phase Learning Roadmap, Cross-Topic Dependency Graphs, 65-Question FAANG Active-Recall Question Bank, and Master Anti-Pattern Bug Matrix).*

---

## 📂 Quick Episode Navigation

### 🔹 Module 01: Core JavaScript Fundamentals (Ep. 01 → Ep. 25)

| Ep. | Lecture Title | Key Topic | Note Link |
|:---:|:---|:---|:---:|
| **01** | The Story of JavaScript | Brendan Eich, Netscape, V8 Engine, JIT Pipeline | [Read Notes](./01-story-of-javascript.md) |
| **02** | Introduction to JavaScript | Script Linking, `<script defer>` vs `async`, DevTools REPL | [Read Notes](./02-introduction-to-javascript.md) |
| **03** | Data Types in JavaScript | 7 Primitives vs Objects, `typeof null === 'object'` Bug | [Read Notes](./03-data-types-in-javascript.md) |
| **04** | Variables Explained in Depth | `let`, `const`, `var`, `undefined` vs `not defined`, TDZ | [Read Notes](./04-javascript-variables-explained-in-depth.md) |
| **05** | Line-by-Line in DevTools | Setup Phase vs Execution Phase, Sources Stepping, Scope | [Read Notes](./05-watch-your-code-running-line-by-line-in-dev-tools.md) |
| **06** | Dialog Boxes | `alert()`, `confirm()`, `prompt()`, Synchronous Thread Blocking | [Read Notes](./06-dialog-boxes-in-javascript.md) |
| **07** | Template Literals & Strings | Autoboxing, UTF-16 Code Units, Immutability, String Methods | [Read Notes](./07-template-literals-string-methods-and-properties.md) |
| **08** | The Math Object | Static Namespace, Float Precision, Uniform Random Formula | [Read Notes](./08-math-object-in-javascript.md) |
| **09** | Truthy and Falsy Values | Exactly 8 Falsy Values, `ToBoolean`, Objects/Arrays Truthy | [Read Notes](./09-truthy-and-falsy-values.md) |
| **10** | Comparison Operators | `===` vs `==`, Abstract Coercion, Relational `null >= 0` | [Read Notes](./10-comparison-operators-in-javascript.md) |
| **11** | Logical Operators | Short-Circuit Evaluation, Value Returns (`&&`, `||`, `??`) | [Read Notes](./11-logical-operators-in-javascript.md) |
| **12** | Decision Making with if | Branching, Block Scope, Accidental Assignment, Semicolon Trap | [Read Notes](./12-decision-making-using-if-statement.md) |
| **13** | Optimizing with else if | Cascading Waterfall, Short-Circuiting, Specificity Ordering | [Read Notes](./13-optimize-decision-making-using-else-if-and-else.md) |
| **14** | Nested if-else Statements | Multi-tier Preconditions, Arrow Anti-Pattern, Guard Clauses | [Read Notes](./14-nested-if-else-statement-in-javascript.md) |
| **15** | The switch Statement | Strict Matching (`===`), Case Fall-Through, Scope in Cases | [Read Notes](./15-switch-statement-in-javascript.md) |
| **16** | The Ternary Operator | Statements vs Expressions, JSX Inline Conditions, Chaining | [Read Notes](./16-ternary-operator-in-javascript.md) |
| **17** | Variable Object References | Call Stack vs Heap, Chrome Heap Snapshots, `@id` Identifiers | [Read Notes](./17-how-to-see-variable-address-in-dev-tools.md) |
| **18** | Objects Explained in Depth | Manila Folder Model, Dot vs Bracket, Dynamic Keys, `hasOwn` | [Read Notes](./18-objects-in-javascript-explained-in-depth.md) |
| **19** | Object.freeze() vs seal() | Property Descriptors, Shallow Freeze, Immutability Guard | [Read Notes](./19-object-freeze-vs-object-seal.md) |
| **20** | Arrays Explained in Depth | Exotic Objects, Synchronized `.length`, Array Holes, `isArray` | [Read Notes](./20-arrays-explained-in-depth.md) |
| **21** | Most Common Array Methods | Mutating vs Non-Mutating, `slice` vs `splice`, String `.sort` | [Read Notes](./21-most-common-array-methods-in-javascript.md) |
| **22** | Multidimensional Arrays | Jagged Arrays, Matrix Coordinates, `.fill([])` Reference Bug | [Read Notes](./22-multidimensional-arrays.md) |
| **23** | The Right Way to Copy | Reference vs Shallow vs Deep, `structuredClone()`, JSON Traps | [Read Notes](./23-right-way-to-copy-objects-and-arrays.md) |
| **24** | Compound & Update Operators | `+=`, Prefix `++x` vs Postfix `x++`, `x = x++` Reset Bug | [Read Notes](./24-combined-assignment-operators.md) |
| **25** | The while Loop in JavaScript | 4 Loop Pillars, Infinite Loop Starvation, Two-Pointer Pattern | [Read Notes](./25-while-loop-in-javascript.md) |

---

### 🔹 Module 02: Advanced Loops, Execution Context, Scopes, Closures, FP & ES6+ (Ep. 26 → Ep. 50)

| Ep. | Lecture Title | Key Topic | Note Link |
|:---:|:---|:---|:---:|
| **26** | For Loop in JavaScript | 3-Part Header, `let` Per-Iteration Scoping, Closure Loop Bug | [Read Notes](./26-for-loop-in-javascript.md) |
| **27** | Do-While Loop in JavaScript | Post-Test Execution, Guaranteed Single Run, Semicolon Syntax | [Read Notes](./27-do-while-loop-in-javascript.md) |
| **28** | Introduction to Functions | Declarations, Parameters vs Arguments, Default `undefined` | [Read Notes](./28-introduction-to-functions.md) |
| **29** | The return Keyword | Ejection Seat, Call Site Value Delivery, Omitted Return | [Read Notes](./29-return-keyword-in-javascript.md) |
| **30** | Execution Context Explained | Memory Creation vs Code Execution, GEC vs FEC, Environments | [Read Notes](./30-execution-context-in-javascript.md) |
| **31** | The Call Stack in JavaScript | LIFO Stack, Frame Allocation, Recursion, Stack Overflow | [Read Notes](./31-call-stack-in-javascript.md) |
| **32** | What is Hoisting? | Variable/Function Allocation, `var` vs `let`/`const` in TDZ | [Read Notes](./32-what-is-hoisting-in-javascript.md) |
| **33** | Global Scope vs Local Scope | One-Way Scope Glass, Privacy Boundaries, Variable Shadowing | [Read Notes](./33-global-scope-vs-local-scope.md) |
| **34** | Lexical & Block Scope | Author-Time Nesting, Scope Chain Traversal, Block Bounds | [Read Notes](./34-lexical-and-block-scope.md) |
| **35** | Higher-Order Functions & Callbacks | First-Class Citizens, Functions as Data, Inversion of Control | [Read Notes](./35-higher-order-functions-and-callbacks.md) |
| **36** | setTimeout and setInterval | Web API Timers, Timer Tokens, Cancellation, 4ms Clamping | [Read Notes](./36-settimeout-and-setinterval.md) |
| **37** | Event Loop & Callback Queue | Single-Thread Concurrency, Call Stack Starvation, Task Queue | [Read Notes](./37-event-loop-and-callback-queue.md) |
| **38** | Returning Functions with Closures | Lexical Backpack, Retained Outer State, Data Encapsulation | [Read Notes](./38-returning-functions-with-closures.md) |
| **39** | Methods vs Functions | Object Method Properties, Invocation Context, Implicit `this` | [Read Notes](./39-difference-between-methods-and-functions.md) |
| **40** | Arrow Functions in JavaScript | Lexical `this`, Concise Syntax, Constructor & `arguments` Ban | [Read Notes](./40-arrow-functions-in-javascript.md) |
| **41** | for-of vs for-in Loop | Iterables vs Enumerable Keys, Prototype Leaks, `Symbol.iterator` | [Read Notes](./41-for-of-vs-for-in-loop.md) |
| **42** | forEach Array Method | Declarative Traversal, `(el, idx, arr)`, Non-Breakable Iteration | [Read Notes](./42-foreach-array-method.md) |
| **43** | map, filter & reduce | FP Trinity, 1:1 Mapping, Boolean Filtering, Rolling Accumulator | [Read Notes](./43-map-filter-reduce-in-javascript.md) |
| **44** | some & every Array Methods | Short-Circuit Boolean Predicates, Vacuous Truth Semantics | [Read Notes](./44-some-and-every-array-methods.md) |
| **45** | The arguments Keyword | Legacy Array-Like Object, Arity Reflection, Arrow Incompatibility | [Read Notes](./45-arguments-keyword-in-javascript.md) |
| **46** | Default Parameters (ES6) | Strictly `undefined` Trigger, Dynamic Expressions, Parameter TDZ | [Read Notes](./46-default-parameters-in-javascript.md) |
| **47** | Spread Operator in JavaScript | Unpacking Iterables, Shallow Copy Nature, Key Precedence | [Read Notes](./47-spread-operator-in-javascript.md) |
| **48** | Rest Parameters in JavaScript | Genuine Array Condensation, Trailing Position Rule, Arity Impact | [Read Notes](./48-rest-parameters-in-javascript.md) |
| **49** | Destructuring in JavaScript | Positional Array Swap, Key Aliasing, Defaults, Nested Unboxing | [Read Notes](./49-destructuring-in-javascript.md) |
| **50** | What is BOM in JavaScript? | `window` Host Root, `location`, `history`, `navigator`, `screen` | [Read Notes](./50-what-is-bom-in-javascript.md) |

---

### 🔹 Module 03: DOM, Modern Events Architecture & Web Storage (Ep. 51 → Ep. 68)

| Ep. | Lecture Title | Key Topic | Note Link |
|:---:|:---|:---|:---:|
| **51** | Introduction to DOM | Render Tree, Critical Rendering Path, `window` vs `document` | [Read Notes](./51-introduction-to-dom.md) |
| **52** | Selecting Elements in JS | `getElementById` vs `querySelector`, Live vs Static Collections | [Read Notes](./52-selecting-elements-in-javascript.md) |
| **53** | innerText vs textContent | Layout Reflows, Script vs Spectator, XSS Prevention | [Read Notes](./53-difference-between-innertext-and-textcontent.md) |
| **54** | getAttribute & setAttribute | HTML Attributes vs Live DOM Properties, `dataset` API | [Read Notes](./54-getattribute-and-setattribute.md) |
| **55** | How to Apply Styles in JS | `classList` API vs Inline `style`, Layout Thrashing | [Read Notes](./55-how-to-apply-styles-in-javascript.md) |
| **56** | Access Family Elements | `parentElement`, `children`, Element vs Node Traversal | [Read Notes](./56-access-parent-sibling-and-children-elements.md) |
| **57** | Difference Between Element & Node | Animal Taxonomy, `nodeType` (1, 3, 8), Text Nodes, Whitespace | [Read Notes](./57-difference-between-element-and-node.md) |
| **58** | append vs appendChild | Variadic Appending, DOMStrings Conversion, Modern Standards | [Read Notes](./58-difference-between-append-and-appendchild.md) |
| **59** | Creating Elements in JS | `createElement`, `DocumentFragment` Batching, Virtual DOM Roots | [Read Notes](./59-creating-elements-in-javascript.md) |
| **60** | Removing Elements in JS | `element.remove()`, `removeChild()`, Detached DOM Leaks | [Read Notes](./60-how-to-remove-element-using-javascript.md) |
| **61** | Event Listeners In-Depth | Observer Pattern, Anonymous Unbinding Bug, `AbortSignal` | [Read Notes](./61-event-listeners-explained-in-depth.md) |
| **62** | Form Event & Event Object | `submit`, `input`, `preventDefault()`, `e.target` vs `currentTarget` | [Read Notes](./62-form-event-and-event-object.md) |
| **63** | Keyboard Events in JS | `e.code` (Hardware Grid) vs `e.key` (Semantic), IME, Game Loops | [Read Notes](./63-keyboard-events-in-javascript.md) |
| **64** | Mouse, Touch & Pointer Events | `mouseenter` vs `mouseover`, Pointer Events API, Pointer Capture | [Read Notes](./64-mouse-events-in-javascript.md) |
| **65** | Event Bubbling & Capturing | 3-Phase Flow, Trickling vs Bubbling, `stopPropagation` | [Read Notes](./65-event-bubbling-and-event-capturing.md) |
| **66** | Event Simulation in JS | Synthetic Events, `dispatchEvent()`, `requestSubmit()`, `isTrusted` | [Read Notes](./66-event-simulation-in-javascript.md) |
| **67** | Event Delegation in JS | Lobby Receptionist, `e.target.closest()`, Memory Optimization | [Read Notes](./67-event-delegation-in-javascript.md) |
| **68** | Local Storage & Master Revision | Web Storage API, ~5MB Quota, XSS Risks + **Master Revision** | [Read Notes](./68-local-storage-explained-in-depth.md) |

---

## 🎯 Pedagogical Features of These Notes

- **Physical Mental Models:** Every concept is introduced with a visual, real-world metaphor (e.g., *Manila folders for objects*, *Laser pointer vs GPS scanner for element selectors*, *Lobby receptionist for event delegation*).
- **Debugger-First Tracing:** Complete line-by-line DevTools execution flows and ASCII memory diagrams showing exactly what happens in the Call Stack, Heap, Scope Chain, and Render Tree.
- **Specification vs Implementation Clarity:** Clear badges distinguishing universal ECMAScript/W3C guarantees from browser engine implementation details (e.g. V8 TurboFan, Blink reflow triggers).
- **Interactive "Predict First" Interview Puzzles:** Code challenges with hidden answers to test true technical comprehension before looking at explanations.
- **Standardized ⚡ 30-Second Revision:** Every note concludes with 5 standardized revision pillars (Essential Facts, Key Mental Model, Common Trap, Interview Question, and Production Code Pattern).\n