# GUI Layout Changes - Quick Reference

## What Changed

The main GUI layout has been redesigned from a **left-right layout** to a **top-middle-bottom layout** with visualizations below the periodic table.

## Layout Before vs After

### Before
```
┌─────────────────────────────────┐
│    Search & Controls            │
├──────────────────┬──────────────┤
│                  │              │
│  Periodic Table  │   Element    │
│  + Details Tabs  │   Details    │
│                  │   + Analysis │
│                  │   + Tabs     │
└──────────────────┴──────────────┘
```

### After
```
┌─────────────────────────────────┐
│    Search & Controls            │
├──────────────────┬──────────────┤
│  Periodic Table  │  Element     │
│  (Vertical       │  Details     │
│   Scroll)        │  (Tabs)      │
├──────────────────┴──────────────┤
│  Visualizations (Horizontal)    │
│  [3D...] [Spectral...] [Heatmap]│
│  ◀─────────────────────────────▶│
└─────────────────────────────────┘
```

## Key Improvements

| Aspect | Before | After |
|--------|--------|-------|
| Visualization Access | Tabs in details panel | Dedicated horizontal panel below |
| Small Screens | Limited space | Horizontal scrolling |
| Workflow | Multi-click to visualize | Single click from button row |
| Button Count | Hidden in tabs | All visible/accessible |
| Responsive | Fixed layout | Resizable, min 1000x800 |

## New Features

### Visualization Panel
- **Location**: Bottom of window
- **Scroll Direction**: Horizontal (left/right)
- **Height**: 300px fixed
- **Responsive**: Buttons stay in single row

### Button Groups
1. **3D Visualizations** (4 buttons)
   - Atomic Structure
   - Ionization Energies
   - Electron Shells
   - Thermal Properties

2. **HyperSpectral** (3 buttons)
   - Spectral Signature
   - Band Ratios
   - Wavelength Map

3. **Analysis** (3 buttons)
   - Li Mineral Detection
   - Heatmap
   - Distributions

## Usage Guide

### View a 3D Visualization
1. Click an element in the periodic table
2. Click "Atomic Structure" (or other 3D button)
3. Matplotlib window opens with visualization

### Compare Multiple Elements
1. Click first element → Click second element → etc.
2. Elements appear in "Selected Elements" list
3. Click "Band Ratios" to compare
4. Comparison visualization opens

### Analyze Entire Periodic Table
1. (No selection needed)
2. Click "Heatmap" or "Distributions"
3. Full table analysis displays

## Scrolling

### Periodic Table
- **Direction**: Vertical
- **Method**: Mousewheel or scrollbar
- **When**: Table taller than window

### Visualizations
- **Direction**: Horizontal
- **Method**: Mousewheel or scrollbar
- **When**: Buttons wider than window

## Window Sizing

```
Default:      1600 x 1000 pixels
Minimum:      1000 x 800 pixels
Resizable:    Yes (drag edges)
Fullscreen:   Yes (F11)
```

## Code Changes Summary

### Modified File
- `src/app/main_app.py`

### Changes Made

1. **Restructured `_create_widgets()`**
   - Added `bottom_frame` for visualizations
   - Organized content into 3 sections
   - Added horizontal scrolling canvas

2. **New Method `_populate_visualization_buttons()`**
   - Creates all visualization buttons
   - Organizes by category
   - Adds separators between groups

3. **Enhanced `_show_visualization()`**
   - Supports HyperSpectral methods
   - Handles multi-element visualizations
   - Better error checking

4. **Updated Window Settings**
   - Geometry: 1600x1000
   - Minimum size: 1000x800

## Visualization Requirements

| Button | Single Element | Multiple | Standalone | Notes |
|--------|----------------|----------|-----------|-------|
| Atomic Structure | ✓ | - | - | Requires 1 element |
| Ionization | ✓ | - | - | Requires 1 element |
| Shells | ✓ | - | - | Requires 1 element |
| Thermal | ✓ | - | - | Requires 1 element |
| Spectral | ✓ | - | - | Requires 1 element |
| Band Ratios | - | ✓ | - | Requires 2+ elements |
| Wavelength | ✓ | ✓ | - | Works with 1+ elements |
| Li Minerals | - | - | ✓ | No selection needed |
| Heatmap | - | - | ✓ | No selection needed |
| Distributions | - | - | ✓ | No selection needed |

## Visual Layout Details

### Top Frame (Search Bar)
- Height: Auto (fits content)
- Contains: Title, search box, clear button
- Fixed at top

### Content Frame (Table + Details)
- Height: Remaining space minus bottom
- Left: Periodic table (scrollable)
- Right: Element details tabs

### Bottom Frame (Visualizations)
- Height: 300px fixed
- Horizontal scrollbar when needed
- Buttons in single row

## Responsive Behavior

### 1600px+ Width
- All buttons visible
- No horizontal scroll needed
- Full details panel

### 1200-1600px Width
- Some buttons need scroll
- Horizontal scroll active
- Partial button visibility

### 1000-1200px Width
- Most buttons need scroll
- Significant horizontal scroll
- Compact layout

## Tips for Users

1. **Small Screen?** → Maximize window or go fullscreen
2. **Can't see buttons?** → Use horizontal scrollbar below visualizations
3. **Periodic table too tall?** → Use vertical scrollbar on left
4. **Too many selections?** → Click "Clear Selection" to reset
5. **Wrong visualization?** → Try others or adjust selections

## Performance Notes

- Periodic table: 119 elements loaded on startup (~500ms)
- Each visualization: Generated on demand (200-500ms)
- 3D visualizations: High resolution (50x50 mesh)
- Heatmap: May take 1-2 seconds for large analysis

## Known Limitations

1. Matplotlib windows open separately (not embedded)
2. No real-time preview in main window
3. Visualizations not cached between calls
4. Button tooltips not yet implemented

## Future Improvements

- Embed matplotlib canvas in GUI
- Save visualization sets
- Real-time preview
- Export multiple formats (PNG, PDF, SVG)
- Element comparison side-by-side
