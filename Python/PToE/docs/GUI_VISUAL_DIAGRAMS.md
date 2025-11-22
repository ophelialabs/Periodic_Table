# GUI Layout Visual Diagrams

## Overall Layout Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                       │
│  ┌──────────────────────── TOP FRAME ────────────────────────────┐  │
│  │                                                                 │  │
│  │ Periodic Table Explorer        [Search: ________] [Clear]     │  │
│  │                                                                 │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌──────────────────── CONTENT FRAME ───────────────────────────┐  │
│  │                                                                 │  │
│  │ ┌────────────────────────┐  ┌─────────────────────────────┐  │  │
│  │ │   PERIODIC TABLE       │  │  ELEMENT DETAILS            │  │  │
│  │ │   (Left Frame)         │  │  (Right Frame)              │  │  │
│  │ │                        │  │ ┌─────────────────────────┐ │  │  │
│  │ │ ┌──────────────────┐   │  │ │ Basic Info │ Properties │ │  │  │
│  │ │ │ H  He            │   │  │ │            │            │ │  │  │
│  │ │ │ Li Be ... Ne     │   │  │ │ Symb: H    │ EN: 2.20   │ │  │  │
│  │ │ │ ... (119 total)  │   │  │ │ Numb: 1    │ Mass: 1.01 │ │  │  │
│  │ │ │                  │ ▲ │  │ │            │            │ │  │  │
│  │ │ │                  │ ▼ │  │ │ Selected   │            │ │  │  │
│  │ │ └──────────────────┘   │  │ │ Elements   │            │ │  │  │
│  │ │     Vert Scroll ───┐   │  │ └─────────────────────────┘ │  │  │
│  │ └────────────────────────┘  │                              │  │  │
│  │                             │ [Clear Selection] [Compare]  │  │  │
│  │                             └──────────────────────────────┘  │  │
│  │                                                                 │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌──────────────────── BOTTOM FRAME ────────────────────────────┐  │
│  │                                                                 │  │
│  │ Visualizations                                                 │  │
│  │ ┌─────────────────────────────────────────────────────────┐   │  │
│  │ │ 3D Visualizations:                                      │   │  │
│  │ │ [Atomic...] [Ionization...] [Electron...] [Thermal...]   │   │  │
│  │ │                                                             │   │  │
│  │ │ HyperSpectral: [Spectral...] [Band...] [Wavelength...]   │   │  │
│  │ │                                                             │   │  │
│  │ │ Analysis: [Li Minerals] [Heatmap] [Distributions]...     │   │  │
│  │ └─────────────────────────────────────────────────────────┘   │  │
│  │ ◀────────────────────────────────────────────────────────────▶  │  │
│  │          Horiz Scroll (when buttons overflow)                    │  │
│  │                                                                 │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Frame Hierarchy

```
tk.Tk (Root Window)
│
├─ top_frame (Pack: TOP, fill X)
│  ├─ Title Label
│  ├─ Search Label + Entry
│  └─ Clear Button
│
├─ content_frame (Pack: TOP, fill BOTH, expand True)
│  │
│  ├─ left_frame (Pack: LEFT, fill BOTH, expand True)
│  │  ├─ Table Label
│  │  ├─ Canvas (for scrollable periodic table)
│  │  │  └─ scrollable_frame (periodic_table_frame)
│  │  │     └─ 119 Element Buttons (in grid)
│  │  └─ Vertical Scrollbar
│  │
│  └─ right_frame (Pack: RIGHT, fill BOTH, expand False)
│     ├─ Details Label
│     ├─ Notebook (tabs)
│     │  ├─ Basic Info Tab
│     │  ├─ Properties Tab
│     │  ├─ Visualization Tab (deprecated)
│     │  └─ Analysis Tab (deprecated)
│     ├─ Selected Elements Display
│     └─ Action Buttons (Clear, Compare)
│
└─ bottom_frame (Pack: BOTTOM, fill BOTH, expand False)
   ├─ Visualizations Label
   ├─ Canvas (for horizontal scroll)
   │  └─ vis_buttons_frame
   │     ├─ Label: "3D Visualizations:"
   │     ├─ Button: Atomic Structure
   │     ├─ Button: Ionization Energies
   │     ├─ Button: Electron Shells
   │     ├─ Button: Thermal Properties
   │     │
   │     ├─ Separator (vertical)
   │     │
   │     ├─ Label: "HyperSpectral:"
   │     ├─ Button: Spectral Signature
   │     ├─ Button: Band Ratios
   │     ├─ Button: Wavelength Map
   │     │
   │     ├─ Separator (vertical)
   │     │
   │     ├─ Label: "Analysis:"
   │     ├─ Button: Li Mineral Detection
   │     ├─ Button: Heatmap
   │     └─ Button: Distributions
   │
   └─ Horizontal Scrollbar
```

## Responsive Breakpoints

### Large Screen (1600px+)

```
┌─────────────────────────────────────────────────────┐
│ Search Bar                                          │
├───────────────────┬───────────────────────────────┤
│                   │                               │
│  Periodic Table   │  Element Details              │
│  (No V-scroll)    │  (All visible)                │
│                   │                               │
├─────────────────────────────────────────────────────┤
│ [3D Buttons] [HyperSpectral] [Analysis] (No H-scroll)│
└─────────────────────────────────────────────────────┘
```

### Medium Screen (1200-1600px)

```
┌──────────────────────────────────────────────────┐
│ Search Bar                                       │
├──────────────────┬───────────────────────────────┤
│                  │                              │
│ Periodic Table   │ Element Details              │
│ (May V-scroll)   │ (Visible)                    │
│                  │                              │
├──────────────────────────────────────────────────┤
│ [3D...] [Hyper...] [Analys...] ◀──▶ (H-scroll) │
└──────────────────────────────────────────────────┘
```

### Small Screen (1000-1200px)

```
┌──────────────────────────────────────┐
│ Search Bar                           │
├──────────────┬──────────────────────┤
│              │                      │
│ Table        │ Element Details      │
│ (V-scroll)   │ (Compact)            │
│              │                      │
├──────────────────────────────────────┤
│ [3D..] [Hyper.] ... ◀─────────────▶ │
│                 (Significant H-scroll)│
└──────────────────────────────────────┘
```

## Visualization Button Layout

### Full Width Display (No Scrolling)

```
3D Visualizations:
┌─────────────┬──────────────────┬─────────────┬─────────────┐
│   Atomic    │  Ionization      │  Electron   │  Thermal    │
│ Structure   │  Energies        │  Shells     │  Properties │
└─────────────┴──────────────────┴─────────────┴─────────────┘
│
HyperSpectral:
┌──────────────┬───────────────┬──────────────┐
│  Spectral    │   Band        │  Wavelength  │
│  Signature   │   Ratios      │  Map         │
└──────────────┴───────────────┴──────────────┘
│
Analysis:
┌──────────────┬──────────────┬───────────────┐
│  Li Mineral  │  Heatmap     │  Distributions│
│  Detection   │              │               │
└──────────────┴──────────────┴───────────────┘
```

### With Horizontal Scrolling

```
┌─ Visible Area ────────────────────┐
│ 3D:       │ HyperSpectral:        │ Analysis:
│ [Atomic]  │ [Spectral] [Band]     │ [Li Mineral]
│ [Ionization                       │ [Heatmap]
│ [Electron]│ [Wavelength] ────────[More→]
│ [Thermal] │
└─ Scrollable Content ──────────────┴──────┐
                                            │
                                  [Distributions]
```

## Data Flow: Element Selection to Visualization

```
User clicks Element Button
    ↓
Element selected/deselected
    ↓
_on_element_selected(element)
    ├─ Toggle element in selected_elements list
    ├─ Update current_element
    └─ Call _update_element_display()
         └─ Populate Basic Info & Properties tabs
    └─ Call _update_selected_display()
         └─ Show selected elements list
    ↓
User clicks Visualization Button
    ↓
_show_visualization(viz_type)
    ├─ Check requirements (selection count)
    ├─ Call appropriate visualizer method
    ├─ Pass current_element or selected_elements
    └─ Display matplotlib figure in new window
    ↓
Figure Window Opens
    ├─ User can zoom, pan, rotate (3D)
    ├─ User can save, print, interact
    └─ User closes window or returns to main GUI
```

## Event Handling Flow

```
User Interaction → Event Handler → Data Update → UI Refresh

Element Click → _on_element_selected() → Add/remove from list → 
    → _update_element_display() & _update_selected_display() → 
    → Display updated info

Visualization Click → _show_visualization() → Call visualizer method → 
    → Figure generation → matplotlib.pyplot.show() → New window

Search Input → _on_search_changed() → Filter elements → Highlight matching

Clear Button → _clear_search() → Reset search → Show all elements

Compare Button → _compare_elements() → Show comparison window → Properties table

Selection Clear → _clear_selection() → Empty selected list → Reset displays
```

## Screen Size Impact

### Periodic Table Visibility

```
Large Screen:    Entire periodic table visible (118 Elements)
                 ┌──────────────────────┐
                 │  H        He         │
                 │  Li Be B  C N  O  F Ne
                 │  ... (full grid)     │
                 └──────────────────────┘

Medium Screen:   Most of periodic table visible
                 ┌──────────────────┐
                 │  H    He         │
                 │  Li Be ... F Ne  │ ◄ Vertical
                 │  ... ▼ ...       │  Scroll
                 │      ▼           │
                 └──────────────────┘

Small Screen:    Portion visible + scroll required
                 ┌──────────────┐
                 │  H  He       │ ◄ Both
                 │  Li Be  ... F│  Vertical
                 │  ... ▼ ...  │  & Horizontal
                 │      ▼   ▶   │  Scroll
                 └──────────────┘
```

### Visualization Button Visibility

```
Large Screen:    All buttons visible
                 [Atomic] [Ionization] [Shells] [Thermal] │ [Spectral] [Band] [Wavelength] │ [Li] [Heat] [Dist]

Medium Screen:   Most buttons visible, some scroll
                 [Atomic] [Ionization] [Shells] [Thermal] │ [Spectral] [Band] ... ▶

Small Screen:    Significant scroll required
                 [Atomic] [Ionization] ... ▶
                 
                 ◄ Scroll to see Thermal, HyperSpectral, Analysis buttons
```

## Summary

The GUI now provides:
- **Clear visual hierarchy**: Top → Middle → Bottom
- **Responsive design**: Adapts to screen size
- **Horizontal scrolling**: For buttons overflow
- **Organized buttons**: Grouped by functionality
- **Intuitive workflow**: Select → Visualize → Analyze

All elements are logically positioned and easily accessible regardless of screen size.
