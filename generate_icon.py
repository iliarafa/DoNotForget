#!/usr/bin/env python3
"""Generate app icon for DO NOT FORGET — a CRT-styled memory game.

Renders a 5x5 grid with a "?" pattern in phosphor green on a dark CRT
background, with glow effects, scanlines, and vignette.

Outputs:
  - 1024x1024 iOS app icon
  - 180x180 apple-touch-icon for web
"""

from PIL import Image, ImageDraw, ImageFilter
import math

# --- Config ---
SIZE = 1024
GRID_N = 5
BG_COLOR = (0, 13, 0)          # #000d00
PHOSPHOR = (51, 255, 0)        # #33ff00
PHOSPHOR_BRIGHT = (127, 255, 51)  # #7fff33
PHOSPHOR_DIM = (10, 38, 0)     # #0a2600
GLOW_COLOR = (51, 255, 0, 80)  # phosphor with alpha for glow

# "?" pattern on 5x5 grid (row, col) — 0-indexed
LIT_CELLS = {
    (0, 1), (0, 2), (0, 3),
    (1, 3),
    (2, 2),
    (4, 2),
}

# --- Output paths ---
IOS_ICON_PATH = "ios/App/App/Assets.xcassets/AppIcon.appiconset/AppIcon-512@2x.png"
WEB_ICON_PATH = "www/apple-touch-icon.png"


def draw_vignette(img):
    """Apply a radial vignette darkening edges."""
    vignette = Image.new("L", (SIZE, SIZE), 0)
    draw = ImageDraw.Draw(vignette)
    cx, cy = SIZE // 2, SIZE // 2
    max_r = SIZE * 0.72
    steps = 80
    for i in range(steps, 0, -1):
        frac = i / steps
        r = int(max_r * frac)
        brightness = int(255 * (frac ** 0.5))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=brightness)
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=40))
    # Composite: multiply original by vignette mask
    r, g, b = img.split()
    r = Image.composite(r, Image.new("L", (SIZE, SIZE), 0), vignette)
    g = Image.composite(g, Image.new("L", (SIZE, SIZE), 0), vignette)
    b = Image.composite(b, Image.new("L", (SIZE, SIZE), 0), vignette)
    return Image.merge("RGB", (r, g, b))


def draw_grid(img):
    """Draw the 5x5 grid with lit/unlit cells and glow effects."""
    grid_size = int(SIZE * 0.65)
    gap = 10
    cell_size = (grid_size - (GRID_N - 1) * gap) // GRID_N
    total = cell_size * GRID_N + gap * (GRID_N - 1)
    offset_x = (SIZE - total) // 2
    offset_y = (SIZE - total) // 2

    # Glow layer — drawn on a separate RGBA image, then blurred and composited
    glow_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)

    draw = ImageDraw.Draw(img)

    for row in range(GRID_N):
        for col in range(GRID_N):
            x = offset_x + col * (cell_size + gap)
            y = offset_y + row * (cell_size + gap)
            r = 8  # corner radius

            if (row, col) in LIT_CELLS:
                # Draw glow halo (larger, blurred)
                pad = 18
                glow_draw.rounded_rectangle(
                    [x - pad, y - pad, x + cell_size + pad, y + cell_size + pad],
                    radius=r + 6,
                    fill=GLOW_COLOR,
                )
                # Sharp lit cell
                draw.rounded_rectangle(
                    [x, y, x + cell_size, y + cell_size],
                    radius=r,
                    fill=PHOSPHOR,
                )
                # Bright center highlight
                inset = cell_size // 5
                draw.rounded_rectangle(
                    [x + inset, y + inset, x + cell_size - inset, y + cell_size - inset],
                    radius=max(1, r // 2),
                    fill=PHOSPHOR_BRIGHT,
                )
            else:
                # Unlit cell
                draw.rounded_rectangle(
                    [x, y, x + cell_size, y + cell_size],
                    radius=r,
                    fill=PHOSPHOR_DIM,
                )

    # Blur and composite glow
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=22))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, glow_layer)
    return img_rgba.convert("RGB")


def draw_scanlines(img):
    """Overlay horizontal scanlines."""
    scanlines = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(scanlines)
    line_spacing = 6
    line_alpha = 28  # ~11% opacity
    for y in range(0, SIZE, line_spacing):
        draw.line([(0, y), (SIZE, y)], fill=(0, 0, 0, line_alpha), width=2)
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, scanlines)
    return img_rgba.convert("RGB")


def generate():
    # 1. Base image
    img = Image.new("RGB", (SIZE, SIZE), BG_COLOR)

    # 2. Draw grid with glow
    img = draw_grid(img)

    # 3. Vignette
    img = draw_vignette(img)

    # 4. Scanlines
    img = draw_scanlines(img)

    # 5. Save 1024x1024 iOS icon
    img.save(IOS_ICON_PATH, "PNG")
    print(f"Saved {IOS_ICON_PATH} ({SIZE}x{SIZE})")

    # 6. Resize to 180x180 for web
    web_icon = img.resize((180, 180), Image.LANCZOS)
    web_icon.save(WEB_ICON_PATH, "PNG")
    print(f"Saved {WEB_ICON_PATH} (180x180)")


if __name__ == "__main__":
    generate()
