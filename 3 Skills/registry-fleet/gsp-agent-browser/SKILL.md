---
name: gsp-agent-browser
description: >-
  Browser automation CLI for AI agents using the agent-browser tool. Provides
  headless browser control for web exploration, data collection, visual testing,
  and screenshot capture. Use when you need to interact with web applications,
  scrape dynamic content, verify UI rendering, or automate browser workflows.
license: MIT
metadata:
  hermes:
    tags: [gsp, browser]
    category: browser
  category: development
  source:
    repository: 'https://github.com/vercel-labs/agent-browser'
    path: skills/agent-browser
---

# Agent Browser Skill

Browser automation using `agent-browser` CLI — a fast native Rust tool for AI agents.

---

## Triggers

Use this skill when:
- "explore a web application"
- "take a screenshot of the app"
- "interact with a web page"
- "collect data from a dynamic website"
- "verify UI rendering"
- "test web application flows"
- "automate browser workflows"
- "scrape JavaScript-rendered content"
- "capture annotated screenshots"

Do NOT use for simple static content retrieval (use `webfetch` instead), or when the user explicitly wants puppeteer-based automation.

---

## Installation

```bash
# Global installation (recommended)
npm install -g agent-browser
agent-browser install  # Download Chrome from Chrome for Testing

# Verify installation
agent-browser doctor
```

---

## Process

### Phase 1: Browser Session Management

**Start a browser session:**
```bash
# Open with URL
agent-browser open <url>

# Open without navigation (for setup)
agent-browser open

# Headless by default, or use --headed for visible browser
agent-browser open <url> --headed
```

**Get current state:**
```bash
agent-browser get title        # Page title
agent-browser get url          # Current URL
agent-browser snapshot         # Full accessibility tree
agent-browser snapshot -i       # Interactive elements only
agent-browser snapshot -c      # Compact view
```

### Phase 2: Element Interaction

**Click and interact:**
```bash
# Click by ref (from snapshot)
agent-browser click @e1

# Click by CSS selector
agent-browser click "#submit"

# Click by semantic locator
agent-browser find role button click --name "Submit"

# Fill input
agent-browser fill @e2 "text to enter"
agent-browser fill "#email" "test@example.com"

# Type character by character
agent-browser type @e2 "text"

# Select dropdown
agent-browser select @e3 "option-value"

# Check/uncheck
agent-browser check @e4
agent-browser uncheck @e5
```

### Phase 3: Information Gathering

**Extract page data:**
```bash
agent-browser get text @e1              # Element text
agent-browser get html @e2              # InnerHTML
agent-browser get value @e3             # Input value
agent-browser get attr @e4 "href"       # Attribute
agent-browser get title                 # Page title
agent-browser get url                   # Current URL
agent-browser get count "a"             # Count elements
agent-browser get box @e1               # Bounding box
```

**Wait for content:**
```bash
agent-browser wait --text "Welcome"    # Wait for text
agent-browser wait --url "**/dashboard" # Wait for URL
agent-browser wait --load networkidle   # Wait for network idle
agent-browser wait 3000                # Wait 3 seconds
```

### Phase 4: Visual Capture

**Screenshots:**
```bash
agent-browser screenshot                    # Basic screenshot
agent-browser screenshot page.png          # Save to file
agent-browser screenshot --annotate        # With numbered element labels
agent-browser screenshot --full            # Full page scroll

# Annotated with element labels (refs visible)
agent-browser screenshot --annotate ./annotated.png
```

**PDF export:**
```bash
agent-browser pdf ./page.pdf
```

### Phase 5: Multi-Step Workflows

**Batch commands (efficient, single invocation):**
```bash
agent-browser batch \
  "open https://example.com" \
  "wait --load networkidle" \
  "snapshot -i" \
  "screenshot result.png"
```

**With error handling:**
```bash
agent-browser batch --bail \
  "open https://example.com" \
  "click @e1" \
  "screenshot"
```

---

## Snapshot Refs System

The snapshot command returns elements with refs like `@e1`, `@e2`:

```
agent-browser snapshot
# Output:
# - heading "Example Domain" [ref=e1]
# - button "Submit" [ref=e2]
# - textbox "Email" [ref=e3]
# - link "Learn more" [ref=e4]
```

Use refs for deterministic interaction:
```bash
agent-browser click @e2
agent-browser fill @e3 "test@example.com"
agent-browser get text @e1
```

---

## Semantic Locators

Alternative to refs and CSS selectors:

```bash
# By ARIA role
agent-browser find role button click --name "Submit"
agent-browser find role link text --name "Learn more"

# By label
agent-browser find label "Email" fill "test@test.com"

# By text content
agent-browser find text "Sign In" click

# By placeholder
agent-browser find placeholder "Search" fill "query"

# By testid
agent-browser find testid "submit-btn" click
```

---

## Tab/Window Management

```bash
agent-browser tab                    # List tabs
agent-browser tab new <url>          # New tab
agent-browser tab t1                 # Switch to tab t1
agent-browser tab close t1           # Close tab
agent-browser window new             # New window
```

---

## Network Interception

```bash
# Block scripts
agent-browser network route "*" --abort --resource-type script

# Mock response
agent-browser network route "/api/*" --body '{"mock": true}'

# Block specific URL
agent-browser network route "https://ads.com/*" --abort
```

---

## State Persistence

```bash
# Save auth state
agent-browser state save auth.json

# Load state on open
agent-browser --state auth.json open https://app.example.com

# Chrome profile reuse
agent-browser --profile Default open https://gmail.com
```

---

## Browser Settings

```bash
# Viewport
agent-browser set viewport 1280 720

# Device emulation
agent-browser set device "iPhone 14"

# Geolocation
agent-browser set geo 37.7749 -122.4194

# Offline mode
agent-browser set offline on
```

---

## Common Workflows

### Web Exploration (for explorer agent)
```bash
agent-browser open <url>
agent-browser snapshot -i
# Analyze structure and refs
```

### Data Collection (for data-collector agent)
```bash
agent-browser open <url>
agent-browser wait --load networkidle
agent-browser snapshot -c
agent-browser get text @eX
agent-browser close
```

### Visual Testing (for verifier/test-expert agents)
```bash
agent-browser open <url>
agent-browser screenshot --annotate baseline.png
# Compare with expected
agent-browser diff screenshot --baseline baseline.png
```

### UAT Simulation
```bash
agent-browser batch \
  "open <url>" \
  "wait --load networkidle" \
  "screenshot" \
  "find role button click --name 'Login'" \
  "fill #username \"testuser\"" \
  "fill #password \"testpass\"" \
  "click #submit" \
  "wait --url '**/dashboard'" \
  "screenshot dashboard.png" \
  "close"
```

---

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Using refs after page navigation | Re-run `snapshot` after every navigation to get fresh refs |
| Clicking without waiting for load | Use `wait --load networkidle` before interacting |
| Ignoring overlay warnings | Dismiss consent banners/modals before clicking target elements |
| Long screenshot filenames | Use `--screenshot-dir ./shots` to set output directory |
| Reusing refs across sessions | Use `state save/load` for session persistence, not refs |

---

## Execution Checklist

```
[ ] Phase 1: Open browser session with URL
[ ] Phase 1: Verify page loaded (get title, get url)
[ ] Phase 2: Get fresh snapshot with refs
[ ] Phase 2: Interact with target elements using refs or selectors
[ ] Phase 3: Extract required data (text, values, attributes)
[ ] Phase 4: Capture screenshot if needed (--annotate for clarity)
[ ] Phase 5: Close browser session
[ ] Verify: All required interactions completed
[ ] Verify: Screenshots captured and saved
[ ] Verify: Data extracted and documented
```

---

## Verification

After browser automation session:
1. Browser session started and closed cleanly (`agent-browser close`)
2. All target elements were found and interacted with
3. Screenshots captured to expected paths (if applicable)
4. Data extracted matches visible page content
5. No overlay/overlay errors reported
6. Session state saved if auth persistence needed
