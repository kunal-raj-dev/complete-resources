# Topic 16: Queues & Deques — Master Index

> **Domain:** FIFO Queues, Circular Buffers, Modulo Indexing, Monotonic Deques, and Circular Greedy Routing

---

## 📋 Topic Overview

This module covers linear FIFO structures and Deques: array modulo wrapping in circular queues, stack-queue emulation, sliding window maximum via monotonic deques, and circular circuit greedy tours.

---

## 📑 Lecture Index

| # | Lecture Title | Focus Areas | Notes Link | Status |
|---|---|---|---|---|
| **79** | Queue Data Structure Intro | FIFO ADT, array false-overflow, linked list pointer chaining | [01_introduction_to_queues.md](./01_introduction_to_queues.md) | **AUDITED** |
| **80** | Circular Queue | Modulo arithmetic `(idx + 1) % cap`, bounded memory reuse | [02_circular_queue_implementation.md](./02_circular_queue_implementation.md) | **AUDITED** |
| **81** | Queue via Stacks & Stack via Queues | Two-stack transfer amortized $O(1)$, single-queue cyclic rotation | [03_queue_using_stacks_and_stack_using_queues.md](./03_queue_using_stacks_and_stack_using_queues.md) | **AUDITED** |
| **82** | First Unique Character | Frequency table + FIFO queue streaming | [04_first_unique_character_in_string.md](./04_first_unique_character_in_string.md) | **AUDITED** |
| **83** | Sliding Window Maximum | Monotonic decreasing `std::deque` storing indices, $O(N)$ linear time | [05_sliding_window_maximum_deque.md](./05_sliding_window_maximum_deque.md) | **AUDITED** |
| **84** | Gas Station | Total deficit balance check, greedy starting point reset | [06_gas_station_greedy_circular.md](./06_gas_station_greedy_circular.md) | **AUDITED** |

---

## 🎯 Topic Revision & Interview Preparation
- **Topic Quick Revision:** [topic_revision.md](./topic_revision.md)
- **Topic Interview Question Bank:** [topic_interview_questions.md](./topic_interview_questions.md)
