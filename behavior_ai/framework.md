# Behavior Analysis Framework

### Step 1: Capture Signals
* Track eye movement and gaze directions.
* Track head position and gesture stability.
* Track basic facial engagement patterns (e.g. smile, neutrality, blink frequency).

### Step 2: Normalize Signals
* Normalize raw interaction metadata indicators into standard `[0, 1]` float ranges.

### Step 3: Detect Patterns
* Detect continuous distractions (looking away).
* Measure candidate attentiveness and responsiveness.
* Detect nervous indicators (rapid head nodding/twitching).

### Step 4: Score Calculation
* Apply weight metrics: 30% eye focus, 20% head stability, 30% engagement, 20% distraction aversion.

### Step 5: Generate Insights
* Classify overall candidate focus levels, attention levels, and flags.
