// Tests the definitions extracted from the Markdown, not separate solver copies.
#include "notes.hpp"
#include <algorithm>
#include <climits>
#include <deque>
#include <functional>
#include <iostream>
#include <numeric>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>

using V = std::vector<int>;
using Matrix = std::vector<V>;
long long checks = 0;
std::mt19937 rng(20261009);

void check(bool value, const std::string& message) {
    ++checks;
    if (!value) throw std::runtime_error(message);
}
template <typename Exception, typename F>
void throws(F function, const std::string& message) {
    bool caught = false;
    try { function(); } catch (const Exception&) { caught = true; }
    check(caught, message);
}
int randomInt(int low, int high) {
    return std::uniform_int_distribution<int>(low, high)(rng);
}
V nearestBrute(const V& a, bool previous, bool smaller, bool strict) {
    const int n = static_cast<int>(a.size());
    V answer(n, -1);
    for (int i = 0; i < n; ++i) {
        for (int j = i + (previous ? -1 : 1); j >= 0 && j < n; j += previous ? -1 : 1) {
            const bool valid = smaller ? (strict ? a[j] < a[i] : a[j] <= a[i])
                                       : (strict ? a[j] > a[i] : a[j] >= a[i]);
            if (valid) { answer[i] = j; break; }
        }
    }
    return answer;
}
V toValues(const V& a, const V& positions) {
    V answer;
    for (int position : positions) answer.push_back(position < 0 ? -1 : a[position]);
    return answer;
}
V circularBrute(const V& a) {
    const int n = static_cast<int>(a.size());
    V answer(n, -1);
    for (int i = 0; i < n; ++i) for (int step = 1; step < n; ++step) {
        const int j = (i + step) % n;
        if (a[j] > a[i]) { answer[i] = a[j]; break; }
    }
    return answer;
}
int celebrityBrute(const Matrix& a) {
    for (int c = 0; c < static_cast<int>(a.size()); ++c) {
        bool valid = true;
        for (int i = 0; i < static_cast<int>(a.size()); ++i)
            if (i != c && (a[i][c] != 1 || a[c][i] != 0)) valid = false;
        if (valid) return c;
    }
    return -1;
}
long long contributionBrute(const V& a, bool ranges) {
    long long total = 0;
    for (int i = 0; i < static_cast<int>(a.size()); ++i) {
        int minimum = a[i], maximum = a[i];
        for (int j = i; j < static_cast<int>(a.size()); ++j) {
            minimum = std::min(minimum, a[j]); maximum = std::max(maximum, a[j]);
            total += ranges ? static_cast<long long>(maximum) - minimum : minimum;
        }
    }
    return total;
}
long long matrixBrute(const std::vector<std::string>& a) {
    if (a.empty()) return 0;
    const int rows = static_cast<int>(a.size()), cols = static_cast<int>(a[0].size());
    long long best = 0;
    for (int top = 0; top < rows; ++top) for (int bottom = top; bottom < rows; ++bottom)
        for (int left = 0; left < cols; ++left) for (int right = left; right < cols; ++right) {
            bool valid = true;
            for (int i = top; i <= bottom; ++i) for (int j = left; j <= right; ++j)
                if (a[i][j] != '1') valid = false;
            if (valid) best = std::max(best, 1LL * (bottom - top + 1) * (right - left + 1));
        }
    return best;
}
V asteroidBrute(V a) {
    bool changed = true;
    while (changed) {
        changed = false;
        for (std::size_t i = 0; i + 1 < a.size(); ++i) if (a[i] > 0 && a[i+1] < 0) {
            const long long left = a[i], right = -static_cast<long long>(a[i+1]);
            if (left == right) a.erase(a.begin() + static_cast<int>(i), a.begin() + static_cast<int>(i) + 2);
            else if (left < right) a.erase(a.begin() + static_cast<int>(i));
            else a.erase(a.begin() + static_cast<int>(i) + 1);
            changed = true; break;
        }
    }
    return a;
}
std::string normalized(const std::string& number) {
    const auto position = number.find_first_not_of('0');
    return position == std::string::npos ? "0" : number.substr(position);
}
std::string digitBrute(const std::string& a, int k) {
    const int n = static_cast<int>(a.size());
    std::string best;
    for (unsigned mask = 0; mask < (1U << n); ++mask) {
        int count = 0;
        std::string kept;
        for (int i = 0; i < n; ++i) if (mask & (1U << i)) { ++count; kept += a[i]; }
        if (count != n-k) continue;
        kept = normalized(kept);
        if (best.empty() || kept.size() < best.size() || (kept.size() == best.size() && kept < best)) best = kept;
    }
    return best;
}
V recursiveDFS(const Matrix& graph, int start) {
    const int n = static_cast<int>(graph.size());
    if (start < 0 || start >= n) return {};
    std::vector<bool> visited(n, false);
    V order;
    std::function<void(int)> visit = [&](int vertex) {
        visited[vertex] = true; order.push_back(vertex);
        for (int neighbor : graph[vertex]) if (!visited[neighbor]) visit(neighbor);
    };
    visit(start);
    return order;
}

void arrayChecks(const V& a) {
    check(l68::stockSpan(a) == l68::stockSpanBrute(a), "stock span oracle");
    l68::StockSpanner stream;
    const V spans = l68::stockSpanBrute(a);
    for (std::size_t i = 0; i < a.size(); ++i) check(stream.next(a[i]) == spans[i], "online span prefix");
    const V next = nearestBrute(a, false, false, true);
    const V previous = nearestBrute(a, true, true, true);
    check(l69::nextGreaterValues(a) == toValues(a, next), "NGE oracle");
    check(l69::nextGreaterBrute(a) == toValues(a, next), "NGE documented baseline");
    check(l70::previousSmallerIndices(a) == previous, "previous smaller indices oracle");
    check(l70::previousSmallerValues(a) == toValues(a, previous), "previous smaller values oracle");
    check(l73::nextGreaterCircular(a) == circularBrute(a), "circular oracle");
    check(l73::nextGreaterCircularBrute(a) == circularBrute(a), "circular documented baseline");
    check(patterns::nextGreaterForwardIndices(a) == next, "forward NGE oracle");
    for (bool before : {false, true}) for (bool smaller : {false, true}) for (bool strict : {false, true})
        check(patterns::nearestIndices(a, before, smaller, strict) == nearestBrute(a, before, smaller, strict), "eight-rule oracle");
    check(applications::sumSubarrayRanges(a) == contributionBrute(a, true), "range contributions oracle");
    V heights;
    for (int value : a) heights.push_back(value < 0 ? -value : value);
    const long long rectangle = l72::largestRectangleBrute(heights);
    check(l72::largestRectangle(heights) == rectangle, "histogram two arrays oracle");
    check(l72::largestRectangleOnePass(heights) == rectangle, "histogram flush/equality oracle");
    auto [left, right] = l72::histogramBounds(heights);
    V expectedRight = nearestBrute(heights, false, true, true);
    for (int& value : expectedRight) if (value < 0) value = static_cast<int>(heights.size());
    check(left == nearestBrute(heights, true, true, true) && right == expectedRight, "histogram boundary indices");
    const long long water = l74::trapBrute(heights);
    check(l74::trapPrefix(heights) == water, "water prefix oracle");
    check(l74::trapTwoPointers(heights) == water, "water maxima pointer oracle");
    check(l74::trapStack(heights) == water, "water layers oracle");
    check(applications::sumSubarrayMinimums(heights) == contributionBrute(heights, false) % 1000000007LL, "minimum contributions oracle");
}

template <typename Stack>
void simpleStackChecks(const std::string& label) {
    Stack stack;
    V model;
    throws<std::underflow_error>([&] { stack.top(); }, label + " empty top");
    throws<std::underflow_error>([&] { stack.pop(); }, label + " empty pop");
    for (int operation = 0; operation < 4000; ++operation) {
        if (model.empty() || (model.size() < 30 && randomInt(0, 1))) {
            const int value = randomInt(-20, 20); model.push_back(value); stack.push(value);
        } else { model.pop_back(); stack.pop(); }
        check(stack.empty() == model.empty(), label + " empty state");
        check(stack.size() == model.size(), label + " size");
        if (!model.empty()) check(stack.top() == model.back(), label + " top");
    }
    // Any remaining nodes are intentionally freed through the destructor path.
}
template <typename Stack>
void minStackChecks(const std::string& label) {
    Stack stack;
    V model;
    throws<std::underflow_error>([&] { stack.top(); }, label + " empty top");
    throws<std::underflow_error>([&] { stack.pop(); }, label + " empty pop");
    throws<std::underflow_error>([&] { stack.getMin(); }, label + " empty minimum");
    const V extremes{INT_MAX, INT_MIN, INT_MIN, INT_MAX, 0, -1, INT_MIN};
    for (int value : extremes) { stack.push(value); model.push_back(value); }
    while (!model.empty()) {
        check(stack.top() == model.back(), label + " extreme top");
        check(stack.getMin() == *std::min_element(model.begin(), model.end()), label + " extreme min");
        stack.pop(); model.pop_back();
    }
    for (int operation = 0; operation < 12000; ++operation) {
        if (model.empty() || (model.size() < 100 && randomInt(0, 1))) {
            const int selector = randomInt(0, 9);
            const int value = selector == 0 ? INT_MIN : selector == 1 ? INT_MAX : randomInt(-8, 8);
            model.push_back(value); stack.push(value);
        } else { model.pop_back(); stack.pop(); }
        check(stack.empty() == model.empty(), label + " empty state");
        if (!model.empty()) {
            check(stack.top() == model.back(), label + " top after mutation");
            check(stack.getMin() == *std::min_element(model.begin(), model.end()), label + " prefix minimum model");
        }
    }
}

void statefulTests() {
    simpleStackChecks<l66::VectorStack>("vector stack");
    simpleStackChecks<l66::ListStack>("list stack");
    simpleStackChecks<l66::LinkedStack>("owned nodes stack");
    simpleStackChecks<l66::FixedStack<32>>("fixed stack");
    l66::FixedStack<0> zero;
    check(zero.empty() && zero.size() == 0, "zero capacity state");
    throws<std::overflow_error>([&] { zero.push(1); }, "zero capacity overflow");
    l66::FixedStack<2> fixed;
    fixed.push(7); fixed.push(8);
    throws<std::overflow_error>([&] { fixed.push(9); }, "fixed capacity overflow");
    check(fixed.size() == 2 && fixed.top() == 8, "overflow preserves old state");
    fixed.pop(); fixed.push(10); check(fixed.top() == 10, "capacity reusable after pop");
    minStackChecks<l71::PairMinStack>("pair minimum stack");
    minStackChecks<l71::EncodedMinStack>("encoded minimum stack");
    minStackChecks<l71::TwoMinStack>("two-stack minimum history");
    applications::TwoStackQueue queue;
    std::deque<int> model;
    throws<std::underflow_error>([&] { queue.front(); }, "queue empty front");
    throws<std::underflow_error>([&] { queue.pop(); }, "queue empty pop");
    for (int i = 0; i < 15000; ++i) {
        const int operation = randomInt(0, 2);
        if (model.empty() || operation == 0) { const int value = randomInt(-100, 100); queue.push(value); model.push_back(value); }
        else if (operation == 1) { queue.pop(); model.pop_front(); }
        else check(queue.front() == model.front(), "queue FIFO front");
        check(queue.empty() == model.empty(), "queue empty state");
        if (!model.empty()) check(queue.front() == model.front(), "queue interleaved transfer ordering");
    }
}

void sourceExamplesAndTraces() {
    check(l66::lifoOrder({4,9,2}) == V({2,9,4}), "LIFO usage");
    l66::VectorStack basic;
    V stack;
    for (int value : {4,9,2}) { basic.push(value); stack.push_back(value); check(basic.top() == stack.back(), "LIFO intermediate push"); }
    for (int value : {2,9,4}) { check(basic.top() == value, "LIFO intermediate pop"); basic.pop(); }
    check(basic.empty(), "LIFO final empty");
    for (const auto& text : {"", "({[]})", "[](){}", "([]){}", "([{}])", "()[]"}) check(l67::isValid(text), "valid bracket checkpoints");
    for (const auto& text : {"([)]", "(]", "())", "(()", ")", "(((", "]", "a"}) check(!l67::isValid(text), "invalid bracket checkpoints");
    check(l68::stockSpan({100,80,60,70,60,75,85}) == V({1,1,1,2,1,4,6}), "span lecture checkpoint");
    check(l68::stockSpan({40,30,35,35,20,45}) == V({1,1,2,3,1,6}), "span original checkpoint");
    check(l68::stockSpan({7,3,6,8}).back() == 4, "nonmonotone no blocker");
    check(l69::nextGreaterValues({6,8,0,1,3}) == V({8,-1,1,3,-1}), "NGE lecture checkpoint");
    check(l69::nextGreaterValues({4,7,2,2,6}) == V({7,-1,6,6,-1}), "NGE original checkpoint");
    check(l69::nextGreaterElementI({4,1,2}, {1,3,4,2}) == V({-1,3,-1}), "NGE I lecture checkpoint");
    check(l69::nextGreaterElementI({7,4,2}, {4,7,2,6}) == V({-1,7,6}), "NGE I original checkpoint");
    check(l70::previousSmallerValues({3,1,0,8,6}) == V({-1,-1,-1,0,0}), "previous smaller lecture checkpoint");
    check(l70::previousSmallerValues({5,2,2,6,4}) == V({-1,-1,-1,2,2}), "previous smaller original checkpoint");
    check(l70::previousSmallerIndices({8,3,7}) == V({-1,-1,1}), "previous smaller index example");
    check(l70::previousSmallerValues({8,3,7}) == V({-1,-1,3}), "previous smaller value example");
    l71::PairMinStack pairs;
    l71::EncodedMinStack encoded;
    for (int value : {7,4,4,9}) { pairs.push(value); encoded.push(value); }
    for (int minimum : {4,4,4,7}) { check(pairs.getMin() == minimum && encoded.getMin() == minimum, "duplicate minimum dry run"); pairs.pop(); encoded.pop(); }
    encoded.push(7); check(encoded.top() == 7 && encoded.getMin() == 7, "encoded reuse after empty");
    const auto [left, right] = l72::histogramBounds({3,1,3,3});
    check(left == V({-1,-1,1,1}) && right == V({1,4,4,4}), "histogram dry-run boundaries");
    V areas;
    const V heights{3,1,3,3};
    for (int i = 0; i < 4; ++i) areas.push_back(heights[i] * (right[i] - left[i] - 1));
    check(areas == V({3,4,6,6}), "histogram dry-run areas");
    const auto [homeLeft, homeRight] = l72::histogramBounds({2,1,5,6,2,3});
    check(homeLeft == V({-1,-1,1,2,1,4}) && homeRight == V({1,6,4,4,6,6}), "lecture histogram homework boundaries");
    const V homeHeight{2,1,5,6,2,3};
    V homeArea;
    for (int i = 0; i < 6; ++i) homeArea.push_back(homeHeight[i] * (homeRight[i] - homeLeft[i] - 1));
    check(homeArea == V({2,6,10,6,8,3}), "lecture histogram homework areas");
    check(l73::nextGreaterCircular({1,2,3,4,3}) == V({2,3,4,-1,4}), "circular lecture first example");
    check(l73::nextGreaterCircular({3,6,5,4,2}) == V({6,-1,6,6,3}), "circular lecture second example");
    check(l73::nextGreaterCircular({2,5,3}) == V({5,-1,5}), "circular original dry run");
    check(l74::trapPrefix({4,2,0,3,2,5}) == 9, "rainwater lecture checkpoint");
    check(l74::trapTwoPointers({3,0,2,0,4}) == 7 && l74::trapStack({3,0,2,0,4}) == 7, "rainwater original checkpoint");
    const Matrix celebrity{{0,1,1,0},{0,0,1,0},{0,0,0,0},{1,0,1,0}};
    check(l75::celebrityStack(celebrity) == 2 && l75::celebrityConstantSpace(celebrity) == 2, "celebrity dry run");
    Matrix invalid = celebrity; invalid[2][0] = 1;
    check(l75::celebrityStack(invalid) == -1, "celebrity mandatory row check");
    check(patterns::nearestIndices({4,2,2,5,1}, true, true, true) == V({-1,-1,-1,2,-1}), "strict pattern trace");
    check(patterns::nearestIndices({4,2,2,5,1}, true, true, false) == V({-1,-1,1,2,-1}), "nonstrict pattern trace");
    check(patterns::nextGreaterForwardIndices({2,2,4}) == V({2,2,-1}), "forward waiting equality");
    check(applications::asteroidCollision({5,10,-12,4,-4}) == V({-12}), "simulation trace");
    check(applications::removeKdigits("3521", 2) == "21", "digit deletion trace");
    check(applications::dfsOrder({{1,2},{3},{3},{}}, 0) == V({0,1,3,2}), "DFS resume trace");
    check(applications::maximalRectangle({"101","111","011"}) == 4, "matrix trace final");
    check(l72::largestRectangle({1,0,1}) == 1 && l72::largestRectangle({2,1,2}) == 3 && l72::largestRectangle({0,2,3}) == 4, "matrix intermediate row histograms");
    check(applications::sumSubarrayMinimums({2,2}) == 6 && applications::sumSubarrayMinimums({3,1,2}) == 9, "minimum contributions examples");
    check(applications::sumSubarrayRanges({1,3,2}) == 5, "range contribution example");

    // Independently reconstruct the tabulated candidate states for selected scans.
    const V prices{40,30,35,35,20,45};
    const std::vector<V> spanStates{{0},{0,1},{0,2},{0,3},{0,3,4},{5}};
    V candidateIndices;
    for (int i = 0; i < 6; ++i) {
        while (!candidateIndices.empty() && prices[candidateIndices.back()] <= prices[i]) candidateIndices.pop_back();
        candidateIndices.push_back(i); check(candidateIndices == spanStates[i], "span intermediate index state");
    }
    const V nge{4,7,2,2,6};
    const std::vector<V> ngeStates{{7,4},{7},{6,2},{6,2},{6}};
    stack.clear();
    for (int i = 4; i >= 0; --i) {
        while (!stack.empty() && stack.back() <= nge[i]) stack.pop_back();
        stack.push_back(nge[i]); check(stack == ngeStates[i], "NGE intermediate stack state");
    }
    const V circular{2,5,3};
    const std::vector<V> circularStates{{1,0},{1},{1,2},{1,0},{1},{2}};
    stack.clear();
    for (int k = 5; k >= 0; --k) {
        const int i = k % 3;
        while (!stack.empty() && circular[stack.back()] <= circular[i]) stack.pop_back();
        stack.push_back(i); check(stack == circularStates[k], "circular intermediate mapped stack");
    }
    const V waterHeights{3,0,2,0,4};
    V waterContributions;
    for (int i = 0; i < 5; ++i) {
        const int lm = *std::max_element(waterHeights.begin(), waterHeights.begin()+i+1);
        const int rm = *std::max_element(waterHeights.begin()+i, waterHeights.end());
        waterContributions.push_back(std::min(lm,rm)-waterHeights[i]);
    }
    check(waterContributions == V({0,3,1,3,0}), "prefix dry-run contributions");
}

void expressionTests() {
    check(applications::evaluateRPN({"8","3","2","*","-"}) == 2, "RPN example");
    check(applications::evaluateRPN({"8","3","-"}) == 5, "RPN left/right subtraction");
    check(applications::evaluateRPN({"-7","3","/"}) == -2, "RPN negative division truncation");
    check(applications::evaluateRPN({"2147483647","2147483647","+"}) == 4294967294LL, "RPN wide arithmetic");
    throws<std::domain_error>([] { applications::evaluateRPN({"1","0","/"}); }, "division by zero");
    throws<std::invalid_argument>([] { applications::evaluateRPN({"1","+"}); }, "RPN missing operand");
    throws<std::invalid_argument>([] { applications::evaluateRPN({"1","2"}); }, "RPN leftover operand");
    throws<std::invalid_argument>([] { applications::evaluateRPN({"12x"}); }, "RPN invalid token");
    check(applications::infixToPostfix({"a","+","b","*","(","c","-","d",")"}) == std::vector<std::string>({"a","b","c","d","-","*","+"}), "infix precedence trace");
    check(applications::infixToPostfix({"8","-","3","-","2"}) == std::vector<std::string>({"8","3","-","2","-"}), "left associativity");
    check(applications::evaluateRPN(applications::infixToPostfix({"8","-","(","3","*","2",")"})) == 2, "conversion evaluation composition");
    check(applications::postfixToPrefix({"8","3","2","*","-"}) == "- 8 * 3 2", "prefix example");
    check(applications::postfixToPrefix({"a","b","c","d","-","*","+"}) == "+ a * b - c d", "prefix nested example");
    throws<std::invalid_argument>([] { applications::infixToPostfix({"(","1"}); }, "unmatched opener");
    throws<std::invalid_argument>([] { applications::infixToPostfix({"1",")"}); }, "unmatched closer");
    throws<std::invalid_argument>([] { applications::postfixToPrefix({"+"}); }, "prefix conversion missing operand");
    for (int i = 0; i < 1000; ++i) {
        const int x = randomInt(-50,50), y = randomInt(-50,50), z = randomInt(-50,50);
        const auto tx = std::to_string(x), ty = std::to_string(y), tz = std::to_string(z);
        check(applications::evaluateRPN(applications::infixToPostfix({tx,"-",ty,"*",tz})) == x - 1LL*y*z, "random precedence");
        check(applications::evaluateRPN(applications::infixToPostfix({"(",tx,"-",ty,")","*",tz})) == 1LL*(x-y)*z, "random parentheses");
    }
}

void randomizedTests() {
    for (const V& a : std::vector<V>{{},{0},{7},{2,2},{4,4,4},{1,2,3,4},{4,3,2,1},{-2,-1,-3},{1,0,1},{2,3,4}}) arrayChecks(a);
    for (int trial = 0; trial < 1800; ++trial) {
        V a(randomInt(0,20));
        for (int& value : a) value = randomInt(-5,8);
        arrayChecks(a);
    }
    // Exhaustive short duplicate-rich arrays complement random sampling.
    for (int n = 0; n <= 6; ++n) {
        int possibilities = 1; for (int i = 0; i < n; ++i) possibilities *= 3;
        for (int code = 0; code < possibilities; ++code) {
            int remaining = code; V a(n);
            for (int& value : a) { value = remaining % 3; remaining /= 3; }
            arrayChecks(a);
        }
    }
    for (int trial = 0; trial < 800; ++trial) {
        V reference(randomInt(0,20)); std::iota(reference.begin(), reference.end(), 0);
        std::shuffle(reference.begin(), reference.end(), rng);
        V queries = reference; std::shuffle(queries.begin(), queries.end(), rng);
        queries.resize(randomInt(0,static_cast<int>(queries.size())));
        V expected;
        const auto answers = toValues(reference, nearestBrute(reference,false,false,true));
        for (int value : queries) {
            const auto position = std::find(reference.begin(), reference.end(), value) - reference.begin();
            expected.push_back(answers[static_cast<std::size_t>(position)]);
        }
        check(l69::nextGreaterElementI(queries,reference) == expected, "NGE I independent query order");
        check(l69::nextGreaterElementIBrute(queries,reference) == expected, "NGE I documented baseline");
        const int n = randomInt(0,10); Matrix matrix(n,V(n));
        for (auto& row : matrix) for (int& value : row) value = randomInt(0,1);
        if (n && trial % 3 == 0) {
            const int c = randomInt(0,n-1);
            for (int i = 0; i < n; ++i) if (i != c) { matrix[i][c]=1; matrix[c][i]=0; }
        }
        check(l75::celebrityStack(matrix) == celebrityBrute(matrix), "celebrity stack oracle");
        check(l75::celebrityConstantSpace(matrix) == celebrityBrute(matrix), "celebrity scalar oracle");
        const int rows = randomInt(0,5), columns = randomInt(0,5);
        std::vector<std::string> binary(rows,std::string(columns,'0'));
        for (auto& row : binary) for (char& value : row) value = randomInt(0,1) ? '1' : '0';
        check(applications::maximalRectangle(binary) == matrixBrute(binary), "matrix rectangle oracle");
        Matrix graph(n);
        for (int i = 0; i < n; ++i) for (int j = 0; j < n; ++j) if (randomInt(0,4) == 0) graph[i].push_back(j);
        for (int i = 0; i < n; ++i) std::shuffle(graph[i].begin(), graph[i].end(),rng);
        const int start = n ? randomInt(0,n-1) : 0;
        check(applications::dfsOrder(graph,start) == recursiveDFS(graph,start), "explicit-frame recursive DFS order");
        V asteroids(randomInt(0,14));
        for (int& value : asteroids) { do { value = randomInt(-6,6); } while (value == 0); }
        check(applications::asteroidCollision(asteroids) == asteroidBrute(asteroids), "adjacent simulation oracle");
        std::string digits;
        for (int i = randomInt(1,9); i > 0; --i) digits += static_cast<char>('0'+randomInt(0,9));
        const int k = randomInt(0,static_cast<int>(digits.size()));
        check(applications::removeKdigits(digits,k) == digitBrute(digits,k), "digit exhaustive-subsequence oracle");
    }
    const V huge(4,1000000000);
    check(l72::largestRectangle(huge) == 4000000000LL, "histogram large area");
    check(l72::largestRectangleOnePass(huge) == 4000000000LL, "histogram one-pass large area");
    const V basin{INT_MAX,0,0,0,INT_MAX};
    const long long largeWater = 3LL*INT_MAX;
    check(l74::trapBrute(basin) == largeWater && l74::trapPrefix(basin) == largeWater && l74::trapTwoPointers(basin) == largeWater && l74::trapStack(basin) == largeWater, "large water accumulation");
    check(applications::asteroidCollision({INT_MAX,INT_MIN}) == V({INT_MIN}), "INT_MIN negation widening");
    check(applications::sumSubarrayRanges({-1000000000,1000000000}) == 2000000000LL, "signed range widening");
    check(applications::sumSubarrayMinimums(V(30000,30000)) == (30000LL*30000*30001/2)%1000000007LL, "large minimum contribution modulo");
    check(l75::celebrityStack({{1}}) == 0 && l75::celebrityStack({{0}}) == 0, "singleton diagonal conventions");
}

int main() {
    try {
        sourceExamplesAndTraces();
        expressionTests();
        statefulTests();
        randomizedTests();
        std::cout << "PASS: " << checks << " assertions.\n"
                  << "2,903 small array cases (1,800 random + 1,093 exhaustive + 10 fixed); all eight neighbor rules.\n"
                  << "800 randomized query/matrix/celebrity/DFS/simulation/digit cases per family.\n"
                  << "16,000 ordinary-stack, 36,000 min-stack, and 15,000 queue model operations.\n"
                  << "1,000 randomized expression pairs; named examples, intermediate states, and large arithmetic checks.\n";
    } catch (const std::exception& error) {
        std::cerr << "FAIL after " << checks << " assertions: " << error.what() << '\n';
        return 1;
    }
}
