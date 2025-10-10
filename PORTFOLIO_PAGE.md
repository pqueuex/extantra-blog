# Portfolio Page Documentation

## Overview
The portfolio page (`portfolio.html`) is a hidden, immersive showcase for animations and drawings with an integrated contact form. It features a unique proximity-based navigation system and full-screen content display.

## Features

### 1. **Desktop Experience**
- **Full-screen immersive display**: Content takes up the entire viewport
- **Proximity-based side panel**: 
  - Appears on the right side
  - Expands when mouse moves within 150px of the right edge
  - Items scale up smoothly based on mouse proximity
  - Auto-collapses when mouse moves away
- **Smooth animations**: CSS transforms and cubic-bezier easing for fluid interactions
- **Keyboard navigation**: Arrow keys to navigate through items

### 2. **Mobile Experience**
- **Top sliding panel**: Touch-friendly navigation at the top
- **Toggle menu**: Tap to open/close the navigation
- **Grid layout**: Items displayed in a responsive grid
- **Optimized touch targets**: Larger tap areas for better usability

### 3. **Content Sections**

#### Animations
- Displays videos from `videos-database.json`
- Full-screen video player with controls
- Auto-play on selection
- Shows duration, resolution, and date

#### Drawings
- Displays artwork from `drawings-database.json`
- Full-screen image viewer
- Shows date and category
- Lazy loading for performance

#### Contact
- Clean, minimal contact form
- Fields: Name, Email, Subject, Message
- Submits via mailto: link to `pq@extantra.net`
- Direct email link provided as alternative

### 4. **Design Elements**
- **Color scheme**: Black background with red (#cc0000) accents
- **Typography**: DotGothic16 monospace font (consistent with site)
- **Borders**: Red pixel-style borders throughout
- **Shadows**: Glowing red shadows on hover/active states
- **Animations**: Smooth scale transforms and opacity transitions

## Technical Implementation

### Proximity Detection (Desktop)
```javascript
// Detects mouse distance from right edge
const distanceFromRight = windowWidth - mouseX;
const threshold = 150;

if (distanceFromRight < threshold) {
    sideNav.classList.add('expanded');
}
```

### Item Scaling Based on Mouse Position
```javascript
// Items grow when mouse is near them
const distance = Math.abs(mouseY - itemCenterY);
const scale = 1 + (proximityFactor * 0.15);
item.style.transform = `scale(${scale})`;
```

### Responsive Breakpoint
- Desktop: Full side panel with proximity detection
- Mobile (≤768px): Top panel with toggle menu

## File Structure
```
portfolio.html           # Main portfolio page
videos-database.json     # Animations data source
drawings-database.json   # Drawings data source
videos/                  # Video files
drawings/                # Drawing files
```

## Usage

### Accessing the Page
Since this is a hidden page, access it directly via:
```
https://extantra.net/portfolio.html
```

### Navigation
- **Desktop**: Move mouse to right edge to reveal menu
- **Mobile**: Tap menu icon at top
- **Keyboard**: Use arrow keys to navigate items
- **Sections**: Switch between Animations, Drawings, and Contact

### Integration Points
The page uses existing infrastructure:
- Same database JSON files as other pages
- Consistent styling with `styles.css`
- Same file structure for media assets

## Customization

### Adjusting Proximity Threshold
Change the threshold value (currently 150px):
```javascript
const threshold = 150; // Increase for earlier expansion
```

### Modifying Scale Effect
Adjust the scale multiplier (currently 0.15):
```javascript
const finalScale = 1 + (scale * 0.15); // Increase for more dramatic effect
```

### Changing Colors
Update the color variables in the `<style>` section:
```css
border: 1px solid #cc0000;  /* Border color */
background: #000;            /* Background color */
```

## Browser Compatibility
- Modern browsers (Chrome, Firefox, Safari, Edge)
- CSS Grid and Flexbox support required
- RequestAnimationFrame for smooth animations
- Fetch API for loading JSON data

## Performance Optimizations
- Lazy loading for images
- RequestAnimationFrame for mouse tracking
- Minimal DOM manipulations
- CSS transforms (GPU-accelerated)
- Conditional event listeners based on viewport

## Future Enhancements
- [ ] Add filtering/sorting options
- [ ] Implement swipe gestures for mobile
- [ ] Add full-screen lightbox mode
- [ ] Include download options
- [ ] Add social sharing buttons
- [ ] Implement search functionality

## Notes
- The page is intentionally not linked from main navigation (hidden)
- Email submission uses mailto: links (no backend required)
- All data loaded from existing JSON databases
- Fully responsive design
- No external dependencies (pure HTML/CSS/JS)
