# Episode 50 — What is the BOM (Browser Object Model) in JavaScript?

> **One-Line Mental Model:** If your HTML page is a passenger, the BOM (`window`) is the airplane cockpit: it controls the flight path (URL), checks the atmospheric instruments (screen/browser info), and logs the flight history—while the passenger sits inside the cabin (`document`).

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete JavaScript Course | ProCodrr)  
> **Instructor:** Anurag Singh  
> **Episode:** #50  
> **Video ID:** `hyIBB48aAws`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=hyIBB48aAws)  
> **Duration:** 55:57  
> **Status:** AUDITED  

---

## 🎯 What You Will Learn
- The architectural distinction between **ECMAScript**, the **BOM (Browser Object Model)**, and the **DOM (Document Object Model)**.
- The dual role of the **`window` object**: The ECMAScript Global Object AND the browser viewport interface.
- Navigating and reading URLs using **`window.location`** (`href`, `pathname`, `search`, `hash`, `assign()`, `replace()`).
- Controlling session navigation with **`window.history`** (`back()`, `forward()`, `go()`, and modern SPA `pushState`).
- Inspecting browser metadata with **`window.navigator`** (device platform, online status, language, user agent).
- Display dimensions: Demystifying **`window.innerWidth/innerHeight`** vs. **`outerWidth/outerHeight`** vs. **`screen.width/height`**.
- Window controls and synchronous blocking dialogs: `alert()`, `confirm()`, `prompt()`, `open()`, and `close()`.
- The direct bridge from Episode 50 into the DOM in [Episode 51](./51-what-is-dom-in-javascript.md).

---

## 1. The Idea in Simple Words

### Simple Explanation
Until now (Episodes 01 to 49), everything we studied was pure **ECMAScript**: variables, loops, functions, closures, objects, arrays, and scopes. Those exist in *any* JavaScript environment, whether running inside Node.js, on a smartwatch, or in a web browser.

When JavaScript runs inside a web browser, the browser hands it extra superpower tools to interact with the browser application itself. This collection of browser-provided tools is called the **BOM (Browser Object Model)**.

Through the BOM, JavaScript can:
- Look at the URL bar and change it (`location`)
- Go back and forward in browser tabs (`history`)
- Find out if the user is connected to Wi-Fi (`navigator.onLine`)
- Check how large the user's physical screen is (`screen`)
- Pop up alerts and open new browser tabs (`window.open`)

### Technical Explanation
The Browser Object Model (BOM) consists of the host objects exposed by browser user agents to JavaScript scripts. While ECMAScript defines the syntax and standard built-in objects, the Web Hypertext Application Technology Working Group (WHATWG) HTML specification standardizes the BOM interfaces under the `Window` interface and related specifications.

---

## 2. 🧠 Mental Model: The JavaScript Web Triad

```
┌─────────────────────────────────────────────────────────────┐
│                       WINDOW OBJECT                         │
│                    (The Root of the BOM)                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────────┐   ┌───────────────────────────────┐ │
│  │   ECMAScript Core  │   │       BOM Sub-Systems         │ │
│  │                    │   │                               │ │
│  │  • Variables       │   │  • location  (URL bar)        │ │
│  │  • Functions       │   │  • history   (Back/Forward)   │ │
│  │  • Objects/Arrays  │   │  • navigator (Browser/Device) │ │
│  │  • Built-ins (Math)│   │  • screen    (Hardware display│ │
│  └────────────────────┘   └───────────────────────────────┘ │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                DOM (Document Object Model)             │ │
│  │            window.document (The HTML Web Page)         │ │
│  │            (Covered starting in Episode 51!)           │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

> **Key Takeaway:** The DOM is actually a child property of the BOM! The web page document lives at `window.document`.

---

## 3. The `window` Object — The Global Commander

In client-side JavaScript, `window` is the **Global Execution Context** object:

1. **Implicit Global Namespace:** Any global property on `window` can be called without typing `window.`:
   ```javascript
   window.alert("Hello"); // Explicit
   alert("Hello");        // Implicit (exact same thing!)
   
   window.setTimeout(...); // Same as setTimeout(...)
   ```

2. **The `var` vs `let`/`const` Global Difference (from [Ep.30](./30-execution-context-in-javascript.md) & [Ep.33](./33-global-scope-vs-local-scope.md)):**
   ```javascript
   var course = "JavaScript";
   let instructor = "Anurag";

   console.log(window.course);     // "JavaScript" (var attaches to window)
   console.log(window.instructor); // undefined (let lives in Declarative Record!)
   ```

3. **Universal Access via `globalThis` (ES2020):**
   In browsers, `globalThis === window`. In Node.js, `globalThis === global`. `globalThis` provides a single universal standard keyword across all JavaScript environments.

---

## 4. Key Sub-Objects of the BOM

### 4.1 `window.location` — The URL Control Center
The `location` object represents the current URL of the document and enables programmatic navigation:

```javascript
// Current URL: https://example.com:8080/products/search?q=laptop#specs

console.log(location.href);     // Full URL
console.log(location.protocol); // "https:"
console.log(location.host);     // "example.com:8080" (hostname + port)
console.log(location.hostname); // "example.com"
console.log(location.port);     // "8080"
console.log(location.pathname); // "/products/search"
console.log(location.search);   // "?q=laptop" (Query string)
console.log(location.hash);     // "#specs" (Fragment identifier)
```

#### Navigation Methods:
```javascript
// 1. Assign: Navigates to a new URL and adds an entry to History (user can hit 'Back')
location.assign("https://google.com");

// 2. Replace: Replaces current URL in History (user CANNOT hit 'Back' to return!)
location.replace("https://google.com"); // Useful for login redirects!

// 3. Reload: Refreshes current page
location.reload();
```

---

### 4.2 `window.history` — Session Navigation
Tracks the browsing history of the current tab or frame:

```javascript
console.log(history.length); // Number of entries in session history

history.back();    // Same as clicking browser Back button (history.go(-1))
history.forward(); // Same as clicking browser Forward button (history.go(1))
history.go(-2);    // Go back 2 pages
```

> **Modern Single Page Apps (SPAs):**  
> Modern frameworks (React Router, Next.js, Vue Router) utilize `history.pushState()` and `history.replaceState()` to update the URL bar dynamically without triggering a full page reload!

---

### 4.3 `window.navigator` — Browser & Hardware Identity
Provides metadata about the browser software and user device:

```javascript
console.log(navigator.userAgent);  // Browser & OS identity string
console.log(navigator.language);   // "en-US", "hi-IN", etc.
console.log(navigator.onLine);     // true (connected) | false (offline)
console.log(navigator.cookieEnabled); // true if cookies allowed

// Clipboard API (Async):
navigator.clipboard.writeText("Copied code snippet!");

// Geolocation API (requires user permission):
navigator.geolocation.getCurrentPosition(position => {
  console.log(position.coords.latitude, position.coords.longitude);
});
```

---

### 4.4 `window.screen` — Physical Hardware Display
Represents the physical screen/monitor of the user's device:

```javascript
console.log(screen.width);       // Physical screen width (e.g., 1920)
console.log(screen.height);      // Physical screen height (e.g., 1080)
console.log(screen.availWidth);  // Available width excluding OS taskbars
console.log(screen.availHeight); // Available height excluding OS taskbars
console.log(screen.colorDepth);  // Bit depth (e.g., 24 or 32 bit)
```

---

## 5. Viewport vs. Window vs. Screen Dimensions

Understanding which dimension to measure is a classic interview question and a crucial responsive design skill:

```
┌────────────────────────────────────────────────────────┐
│ SCREEN (screen.width x screen.height)                  │
│  ┌──────────────────────────────────────────────────┐  │
│  │ BROWSER WINDOW (outerWidth x outerHeight)        │  │
│  │ [ Tabs, Titlebar, Address Bar, Bookmarks ]       │  │
│  │  ┌────────────────────────────────────────────┐  │  │
│  │  │ VIEWPORT (innerWidth x innerHeight)        │  │  │
│  │  │                                            │  │  │
│  │  │  [ The actual rendered web page content ]  │  │  │
│  │  │                                            │  │  │
│  │  └────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
│  [ OS Taskbar / Dock ]                                 │
└────────────────────────────────────────────────────────┘
```

| Dimension Property | What It Actually Measures |
| :--- | :--- |
| `window.innerWidth` / `innerHeight` | The visible **HTML viewport** where your page renders (includes scrollbars). |
| `window.outerWidth` / `outerHeight` | The **entire browser application window**, including tabs, address bar, and borders. |
| `screen.width` / `height` | The physical **hardware monitor** resolution. |
| `screen.availWidth` / `availHeight` | Physical monitor resolution minus OS UI (such as the Windows Taskbar or macOS Dock). |

---

## 6. Browser Dialogs & Window Control

### 6.1 Synchronous Blocking Dialogs
JavaScript provides three built-in modal dialogs:

```javascript
// 1. Alert: Displays a message with an OK button (returns undefined)
alert("Download complete!");

// 2. Confirm: Displays message with OK and Cancel (returns true or false)
const deleteConfirmed = confirm("Are you sure you want to delete this file?");
if (deleteConfirmed) {
  console.log("Deleting...");
}

// 3. Prompt: Displays input field (returns string or null if canceled)
const userName = prompt("Enter your name:", "Guest");
console.log(userName);
```

> ⚠️ **Critical Production Note:**  
> These dialogs are **synchronous and thread-blocking**. While an `alert()` or `prompt()` modal is open, the JavaScript Event Loop is paused, all CSS animations freeze, timers stop firing, and user interaction on the tab is completely paralyzed. Modern web applications almost exclusively use custom HTML/CSS modal dialogs (such as `<dialog>`) instead.

### 6.2 Window Control Methods
```javascript
// Open a new tab/window:
const newTab = window.open("https://example.com", "_blank");

// Close the tab programmatically (only works if opened via window.open):
newTab.close();

// Programmatic scrolling:
window.scrollTo({ top: 0, behavior: "smooth" });
window.scrollBy({ top: 200, behavior: "smooth" });
```

---

## 7. ❓ Confusion Checks

### Q1: Is the DOM part of the BOM?
**Yes, structurally in browsers.**  
The DOM root (`document`) is an object property mounted directly on the `window` object (`window.document`). However, conceptually they are defined by different specifications:
- DOM is standardized by the W3C/WHATWG DOM specification.
- BOM features are standardized by the WHATWG HTML specification under `Window`.

### Q2: Why does `window.name` have surprising behavior?
`window.name` is a built-in property on `window` used for iframe targeting. It **automatically converts whatever value you assign to it into a string**!
```javascript
window.name = 123;
console.log(typeof window.name); // "string"! (Not number!)
```
This is why creating a global variable `var name = 123;` in sloppy mode causes subtle bugs.

### Q3: What is the difference between `location.href = url` and `location.replace(url)`?
- `location.href = url` (or `location.assign(url)`): Adds the current page to the session history. When the user hits the browser **Back** button, they return to where they were.
- `location.replace(url)`: Overwrites the current entry in the session history. The user **cannot** hit the Back button to return to the original page. Perfect for redirects after unauthorized login attempts!

---

## 8. 🧠 Brain Triggers (Memory Hooks)

- **Window = The Universe:** In the browser, everything global is a child or method of `window`.
- **Location = The GPS:** Reads coordinates (`pathname`, `search`, `hash`) and drives the browser (`assign`, `replace`).
- **History = The Breadcrumbs:** Back, forward, and steps through the current session.
- **Navigator = The ID Card:** Who am I? Which browser? Am I online?
- **Screen = The Hardware TV:** The glass panel in front of your eyes.
- **Inner = Webpage, Outer = Browser Window, Screen = Monitor.**

---

## 9. 🔥 Interview Deep Dive

### Q1: Why do Single Page Applications (SPAs) use the History API (`pushState`) instead of hash routing (`#`)?
**Answer:**
1. **Clean URLs:** Hash routing produces URLs like `example.com/#/dashboard`, which looks dated and causes issues with server analytics and SEO crawlers.
2. **Server-Side Rendering (SSR) & SEO:** URLs created via `history.pushState()` look like standard standard paths (`example.com/dashboard`), allowing search engine spiders and server-side renderers to serve real HTML documents directly.
3. **State Storage:** `history.pushState(stateObject, "", url)` can attach an arbitrary serializable state object to the history entry, which is preserved and accessible via `history.state` or the `popstate` event when the user navigates back and forth!

### Q2: Can you access cross-origin properties on `window.open()`?
**Answer:**
**Almost none!**  
Due to the **Same-Origin Policy (SOP)**, if your page opens a window pointing to a different origin (different protocol, domain, or port), your script cannot access `newWindow.document`, `newWindow.location.href`, or any variables inside that window. The browser will throw a fatal `SecurityError: Blocked a frame with origin from accessing a cross-origin frame`. You are only permitted to call `.close()`, `.postMessage()`, and inspect `.closed`.

---

## 10. 🔬 Layered Concept Classification

### 🟢 MUST KNOW
- `window` is the global object in browser JavaScript; methods like `setTimeout` and `alert` live on it.
- `location.href` to read or navigate URLs.
- `location.assign()` vs `location.replace()` navigation mechanics.
- `history.back()` and `history.forward()`.
- Difference between `window.innerWidth/innerHeight` (viewport) and `screen.width/height` (hardware).
- That `document` lives on `window.document` (the gateway to the DOM).

### 🟡 SHOULD KNOW
- `navigator.onLine` and `navigator.userAgent`.
- Using `history.pushState()` for client-side routing.
- Synchronous blocking nature of `alert()`, `confirm()`, and `prompt()`.
- `globalThis` as the environment-agnostic global identifier.

### 🔵 DEEP DIVE
- Parsing query parameters cleanly using `new URLSearchParams(window.location.search)`.
- Same-Origin Policy restrictions on `window.open` and cross-origin iframes.
- The `window.name` string coercion quirk.

### ⚫ IMPLEMENTATION DETAIL
- Browsers isolate each tab into separate OS processes (Site Isolation) so heavy BOM operations or crashes in one tab do not compromise the renderer of another origin.

---

## 11. ⚡ 30-Second Revision

1. BOM (Browser Object Model) gives JavaScript control over the browser window outside of HTML content.
2. `window` is the root: every global variable (`var`), function, and BOM object lives on it.
3. `window.location` reads and controls the current URL (`href`, `pathname`, `search`).
4. `location.replace()` navigates without leaving a history back-entry.
5. `window.history` controls tab navigation (`back()`, `forward()`, `go()`).
6. `window.navigator` reports browser/device capabilities (`onLine`, `userAgent`).
7. `innerWidth`/`innerHeight` measures the visible HTML viewport; `screen.width`/`height` measures the physical monitor.
8. `window.document` is the BOM's direct bridge to the DOM (Episode 51).

---

## 12. 🛠️ Tiny Practice Tasks

1. **Query Param Parser:** In your browser console, navigate to a URL with queries (e.g. `google.com/search?q=javascript&hl=en`), and use `new URLSearchParams(window.location.search)` to extract the query parameters.
2. **Online Status Monitor:** Write a small script that listens to the `window` events `"online"` and `"offline"` and logs the user's connection status.
3. **Viewport Dimension Logger:** Write a one-liner in the console that logs the current viewport size (`innerWidth` x `innerHeight`) whenever the browser window is resized (`window.onresize`).

---

## 13. 📋 Interview Readiness Checklist

- [ ] Can clearly articulate the difference between ECMAScript, BOM, and DOM.
- [ ] Understand why `location.replace()` is preferred over `location.assign()` for authentication redirects.
- [ ] Know the difference between `window.innerHeight`, `window.outerHeight`, and `screen.height`.
- [ ] Understand why `alert()`, `confirm()`, and `prompt()` should be avoided in modern production web apps.
- [ ] Ready to transition into Episode 51: The Document Object Model (DOM)!
