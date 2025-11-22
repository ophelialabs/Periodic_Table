# Resizable Element Details Panel - User Guide

## Overview
The element details panel can now be resized by dragging the divider between the periodic table and element details sections.

## How to Use

### Adjusting Panel Width

1. **Locate the Divider**
   - Look for the vertical line between the periodic table (left) and element details (right)
   - The divider appears as a slightly darker gray line
   - It has a sash grip that becomes visible when you hover over it

2. **Drag to Resize**
   - Click and drag the divider left or right
   - The divider will move smoothly
   - Periodic table gets wider → element details get narrower
   - Element details get wider → periodic table gets narrower

3. **Release to Lock**
   - Release the mouse button to lock the new position
   - Your adjustment is immediately saved during the session

### Constraints

The divider respects minimum sizes:
- **Periodic Table minimum**: 400 pixels wide
- **Element Details minimum**: 250 pixels wide

This ensures:
- Periodic table remains readable with element buttons visible
- Element details can always display at least one column of content
- You can't make either panel too small to be unusable

### Default Widths

When you start the application:
- **Periodic Table**: ~700 pixels (wider, more visible elements)
- **Element Details**: ~300 pixels (compact, shows essentials)

You can adjust these to match your preferences!

## Use Cases

### Wide Element Details
Drag the divider left if you want:
- More text visible in the properties tab
- Better readability of element information
- Wider display of the details notebook tabs
- More comfortable reading of long property values

### Wide Periodic Table
Drag the divider right if you want:
- More element buttons visible at once
- Larger element symbols and atomic mass
- Easier navigation of the periodic table
- Better overview of element groupings

### Balanced View
Keep roughly equal widths if you want:
- Both panels equally prominent
- Good balance between exploration and detail
- Natural workflow (table on left, details on right)

## Responsive Behavior

The resizable panel works with the responsive design:

- **Small screens** (<1000px): 
  - Both panels may stack if dragged too far
  - Maintain 400px and 250px minimums

- **Medium screens** (1000-1400px):
  - Plenty of room to adjust either way
  - Good for balanced workflows

- **Large screens** (>1400px):
  - Lots of flexibility
  - Can make both panels very wide

## Keyboard Shortcuts

Currently, the resizing is mouse/trackpad only. You can:
- Click and drag the divider
- Use scrollbars within each panel independently

## Tips

1. **Find the sweet spot**: Experiment with different widths to see what works best for you

2. **Maximize readability**: Make the periodic table wider if you're mostly exploring elements

3. **Detail focus**: Make the element details wider if you're carefully reading property values

4. **Remember your preference**: The width adjustment stays during your session (until you close the app)

5. **Reset to defaults**: Close and reopen the application to return to default widths

## Technical Details

The resizable panel uses tkinter's `PanedWindow` widget, which provides:
- Smooth dragging experience
- Automatic constraint enforcement (minimum sizes)
- Visual feedback (sash appears when hovering)
- Responsive to all screen sizes

## Troubleshooting

### Can't find the divider?
- Look for a slightly darker vertical line between the two panels
- Hover over the area where they meet
- The cursor should change to a resize cursor (↔)

### Panel won't resize?
- Make sure you're clicking on the divider itself, not on the panels
- Try moving your mouse until you see the resize cursor
- Then click and drag

### Can't make a panel wide enough?
- The application enforces minimum sizes for usability
- If you need more space, try on a larger monitor or maximizing the window
- Adjust the other panel to give more room

### Divider position resets when I reopen?
- This is normal - positions aren't saved between sessions
- You can adjust it again to your preference

---

**Enjoy customizing your view!** The resizable panel makes it easy to tailor the interface to your workflow.
