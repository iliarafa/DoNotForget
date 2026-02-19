# DO NOT FORGET

A retro CRT memory game. Glowing cells flash on a phosphor-green grid — memorize the pattern, then tap to recall it. Patterns grow longer and faster across 12 trials. Earn points for accuracy, bonus for perfect rounds.

## Features

- Authentic CRT monitor aesthetic: scanlines, flicker, vignette, screen glare, noise
- Boot sequence with POST-style system check
- 12 increasingly difficult trials (3→8 cells to memorize, shrinking display time)
- Scoring system with perfect round bonuses
- Retro sound effects via Web Audio API
- Fully self-contained — single HTML file, no external dependencies

## iOS App

The game is wrapped as a native iOS app using [Capacitor](https://capacitorjs.com).

### Prerequisites

- Node.js 18+
- Xcode 15+
- CocoaPods

### Setup

```bash
npm install
npx cap sync ios
npx cap open ios
```

Build and run from Xcode (Cmd+R).

### Browser

Open `index.html` directly in any modern browser — no build step needed.

## Tech

- Vanilla HTML/CSS/JS
- Web Audio API for sound
- Capacitor for iOS native wrapper
- CSS `env(safe-area-inset-*)` for notch/home indicator handling

## License

MIT
