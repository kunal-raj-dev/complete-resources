# Validation report

[Study index](README.md) · [Source coverage](SOURCE_COVERAGE.md)

**Result: PASS.** Last run: 2026-10-09 15:51:56 local time.

## Compilation

- Compiler: `g++.exe (Rev4, Built by MSYS2 project) 16.2.0`.
- Actual executable: `C:\Users\kunal\Desktop\stacks_dsa_notes\.research\toolchain\ucrt64\bin\g++.exe`.
- All **38 complete C++ blocks** extracted directly from the Markdown compiled independently as C++17 translation units.
- Flags: `-std=c++17 -Wall -Wextra -Wpedantic -Werror -BC:/msys64/ucrt64/bin/ -static`; all warnings treated as errors.
- A temporary namespaced collection of those exact blocks was compiled with the behavior harness. Functions and classes are exercised without relying on a judge wrapper.
- Build products were created in an automatically cleaned temporary directory.

## Behavior and examples

```text
PASS: 291894 assertions.
2,903 small array cases (1,800 random + 1,093 exhaustive + 10 fixed); all eight neighbor rules.
800 randomized query/matrix/celebrity/DFS/simulation/digit cases per family.
16,000 ordinary-stack, 36,000 min-stack, and 15,000 queue model operations.
1,000 randomized expression pairs; named examples, intermediate states, and large arithmetic checks.
```

Tests use deterministic seeds and independently structured brute-force/reference implementations. Array tests cover all eight strict/non-strict previous/next variants, spans, ordinary/circular next greater, previous smaller, both histogram optimizations, three rainwater optimizations, and minimum/range contributions. Stateful tests compare stack/min-stack/queue behavior to vectors/deques. Celebrity is checked against a complete row/column oracle; matrix rectangles, simulation, greedy digit deletion, expression order/precedence, and DFS order receive separate checks.

Empty/singleton inputs where allowed, monotone arrays, duplicates, all-equal arrays, absent answers, wraparound, repeated minima, diagonal 0/1, and widened arithmetic cases are included. Named example checkpoints and intermediate stack/boundary states are verified in the harness; the Markdown dry-run tables were also reviewed against the algorithms. The text uses consistent bottom-to-top notation.

## Source and Markdown audit

- 10 caption sequences (5753 segments), 136 ledger passages, 17 reviewed frame checkpoints.
- All 18 study/report Markdown files audited; 396 relative path/heading links resolved.
- Code fences balanced; table column counts consistent; headings separated from following content.
- Study chapters and supplements contain approximately 19,919 prose/table words, excluding fenced code.
- Official practice destinations and problem labels were reviewed on 2026-10-09; this is not a guarantee that external sites never change.

## Reproduce and interpret

Run `python validation/validate.py`; optionally select a compiler with `--cxx PATH` or the `CXX` environment variable. Tests re-extract current Markdown code. A workspace-local profile, when present and usable, selects the prepared compiler, installed binutils, and standalone runtime linking. Explicit `--cxx`/`CXX` takes priority. Without that profile, the validator tries PATH and then the already installed MSYS2 UCRT compiler. A runnable, complete toolchain is required.

This run used the workspace-local toolchain profile. The compiler packages came from the [official MSYS2 package repository](https://packages.msys2.org/packages/mingw-w64-ucrt-x86_64-gcc), with published SHA256 checks, because the existing PATH compiler could not start and another installed compiler lacked cc1plus. The working installed assembler/linker were selected with `-B`; `-static` removes toolchain-runtime DLL dependencies from the test executable. No installed toolchain files or system security settings were changed. The validator itself does not download or install a toolchain.

Finite randomized tests support correctness but are not a formal proof. Chapter invariants provide the reasoning. Tests assume each documented input/numeric contract; malformed matrices, invalid adjacency indices, arbitrary arithmetic overflow, allocation failures, and platform-specific memory limits are outside those contracts. Raw-node destructor paths are exercised, but this run is not a dedicated leak-sanitizer audit. Source review is full-caption plus selected-frame review, with the limits stated in the coverage ledger.
