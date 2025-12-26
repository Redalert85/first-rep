# Digital Clock Application

A modern, responsive digital clock application that displays the current time in multiple time zones simultaneously.

## Features

### ✨ Core Features
1. **Display Components**: Clean, modern user interface showing current time with large, readable fonts
2. **Time Zone Support**: View times in different time zones including:
   - Local time (automatically detected)
   - UTC (Coordinated Universal Time)
   - Any other time zone from a comprehensive list
3. **Automatic Refresh**: Time updates dynamically every second
4. **User Time Zone Selection**: Interactive dropdown to add or remove time zones dynamically

### 🎨 Design Features
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Modern UI**: Gradient background, glass-morphism effects, and smooth animations
- **Readable Display**: Large, monospace fonts for easy time reading
- **Interactive Cards**: Hover effects and smooth transitions
- **Color-Coded Actions**: Intuitive color scheme (green for add, red for remove)

## Usage

### Quick Start

1. **Open the application**:
   Simply open `digital_clock.html` in any modern web browser (Chrome, Firefox, Safari, Edge)

2. **View default clocks**:
   The application starts with two default clocks:
   - **Local Time**: Your system's current time zone
   - **UTC**: Coordinated Universal Time

3. **Add a time zone**:
   - Click the dropdown menu labeled "Add Time Zone"
   - Select a time zone from the list
   - Click the "Add" button
   - The new clock will appear instantly

4. **Remove a time zone**:
   - Hover over any added clock card (not Local or UTC)
   - Click the red "×" button in the top-right corner
   - The clock will be removed immediately

### Available Time Zones

The application includes major time zones from around the world:

**Americas**:
- New York, Chicago, Denver, Los Angeles, Phoenix
- Anchorage, Honolulu
- Toronto, Vancouver, Mexico City
- São Paulo, Buenos Aires

**Europe**:
- London, Paris, Berlin, Moscow, Istanbul

**Asia**:
- Dubai, Karachi, Kolkata (India)
- Shanghai, Hong Kong, Tokyo, Seoul, Singapore

**Africa**:
- Cairo, Johannesburg, Lagos, Nairobi

**Oceania**:
- Sydney, Melbourne, Perth, Auckland

## Technical Details

### Implementation

- **Pure JavaScript**: No external dependencies required
- **Modern APIs**: Uses `Intl.DateTimeFormat` for accurate time zone conversions
- **Automatic Detection**: Detects user's local time zone automatically
- **Cross-Browser Compatible**: Works on all modern browsers

### How It Works

1. **Time Zone Management**: 
   - Maintains an array of active time zones
   - Each time zone has a unique ID, label, and IANA time zone identifier

2. **Automatic Updates**:
   - Uses `setInterval()` to update all clocks every 1000ms (1 second)
   - Ensures synchronized updates across all displayed time zones

3. **Time Formatting**:
   - Uses `Intl.DateTimeFormat` for accurate time zone conversions
   - Displays time in 24-hour format (HH:MM:SS)
   - Shows full date with day name, month, and year

4. **Dynamic Rendering**:
   - Clocks are dynamically created and removed from the DOM
   - No page reload required for adding/removing time zones

### Code Structure

```javascript
// Main components:
- init()                    // Initialize the application
- populateTimeZoneDropdown() // Populate time zone options
- addTimeZone()             // Add a new clock
- removeTimeZone(id)        // Remove a clock
- renderClocks()            // Render all clock cards
- updateAllClocks()         // Update all times
- updateClock(tzData)       // Update individual clock
```

## Requirements

- Modern web browser with JavaScript enabled
- Internet connection not required (all code is self-contained)

## Browser Compatibility

- ✅ Chrome 76+
- ✅ Firefox 70+
- ✅ Safari 14+
- ✅ Edge 79+
- ✅ Opera 63+

## Customization

### Adding More Time Zones

Edit the `timeZones` array in the JavaScript section:

```javascript
const timeZones = [
    'UTC',
    'America/New_York',
    // Add your time zone here using IANA format
    'Your/TimeZone'
];
```

### Changing Colors

Modify the CSS gradient in the `body` style:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Adjusting Update Frequency

Change the interval in the `init()` function (value in milliseconds):

```javascript
setInterval(updateAllClocks, 1000); // 1000ms = 1 second
```

## Screenshots

The application displays:
- A gradient purple background
- White glass-morphism cards for each clock
- Large, readable time displays
- Full date information
- Time zone identifiers
- Interactive add/remove controls

## License

This project is open source and available for educational and personal use.

## Support

For issues or questions:
1. Check that JavaScript is enabled in your browser
2. Ensure you're using a modern browser (see compatibility list)
3. Try refreshing the page if clocks don't update

## Future Enhancements (Optional)

Possible future improvements:
- 12/24 hour format toggle
- Alarm functionality
- Time zone search/filter
- Save preferred time zones to localStorage
- Dark/light theme toggle
- Export time zone list
- Meeting time planner across zones
