# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

"DO NOT FORGET" — a retro CRT-styled memory game wrapped as a native iOS app via Capacitor. The entire game lives in a single `index.html` file (vanilla HTML/CSS/JS, no framework, no build step).

## Commands

### Run in browser
Open `index.html` directly — no server or build needed.

### iOS development
```bash
npm install
npx cap sync ios     # copies www/ to Xcode project and syncs plugins
npx cap open ios     # opens Xcode project
```
Build/run from Xcode with Cmd+R. Requires Xcode 15+ and CocoaPods.

### Capacitor sync workflow
After editing `index.html`, copy it to `www/index.html` then run `npx cap sync ios` before building in Xcode. Capacitor serves from the `www/` directory (configured as `webDir` in `capacitor.config.json`).

## Architecture

### Single-file game (`index.html`)
Everything — CSS, HTML, and JS — is in one file. No external JS/CSS dependencies except Google Fonts (VT323).

**Game state machine** — `state.phase` drives all transitions:
```
off → boot → title → memorize → input → feedback → gameover
                                   ↑                    |
                                   └── next trial ──────┘ (or restart)
```

**Key game parameters:**
- 5×5 grid (25 cells), 12 trials
- `patternSize(trial)`: 3 + floor((trial-1)/2) — cells to memorize grow from 3→8
- `memorizeTime(trial)`: max(1100, 2600 - (trial-1)*130) ms — display time shrinks
- Scoring: 10 pts per correct, -5 per wrong, +50 bonus for perfect round

**Audio** — `sfx` object with Web Audio API oscillator-based sound effects. `ensureAudio()` must be called on user gesture to unlock AudioContext.

**CRT effects** — layered CSS: scanlines (`.screen::after`), vignette (`.screen::before`), flicker animation, noise overlay, interference line, screen glare. All use `pointer-events: none` and z-index layering above game content.

**iOS safe areas** — screen padding uses `env(safe-area-inset-*)` for notch/home indicator.

### Capacitor config (`capacitor.config.json`)
- App ID: `com.thiswholeworldllc.donotforget`
- StatusBar plugin configured for dark style with black background

### iOS native layer (`ios/`)
Standard Capacitor scaffold. `AppDelegate.swift` is the only Swift file; it's the default Capacitor boilerplate.
