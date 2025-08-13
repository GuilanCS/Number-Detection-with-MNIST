# Rice Grain Analyzer GUI - Cleaned Version

A comprehensive GUI application for analyzing rice grain properties including dimensional measurements, shape characteristics, and classification. This is a cleaned and refactored version of the original code with improved structure, maintainability, and documentation.

## Features

- **Dimensional Analysis**: Measure length, width, and thickness of rice grains
- **Shape Analysis**: Calculate roundness and aspect ratio
- **Classification**: Categorize grains by size (complete, very long, long, medium, short)
- **Fracture Analysis**: Identify broken grains and fragments
- **Visual Features**: Detect chalky, red, spotted, and other visual characteristics
- **Grading System**: Grade rice according to Iranian standard 127
- **Single Grain Analysis**: Detailed analysis of individual grains
- **Persian/Farsi UI**: Full RTL support with proper font rendering

## Code Improvements

### 🏗️ Structure Improvements

1. **Object-Oriented Design**: Refactored from procedural to OOP approach
2. **Separation of Concerns**: UI logic separated from business logic
3. **Modular Architecture**: Code organized into focused classes and methods
4. **Constants Management**: All magic numbers and strings extracted to constants

### 🎨 Code Quality

1. **Type Hints**: Added comprehensive type annotations
2. **Documentation**: Added docstrings for all classes and methods
3. **Error Handling**: Improved error handling with proper fallbacks
4. **Code Formatting**: Consistent formatting following Python standards

### 🧩 Class Structure

#### `FontManager`
- Manages font loading and configuration
- Platform-specific font selection (Windows/Linux)
- Fallback mechanisms for missing fonts
- Centralized font size management

#### `StatusIndicator`
- Custom widget for visual status indicators
- Color-coded status display
- Dynamic color updates

#### `UIComponents`
- Factory class for creating common UI elements
- Standardized component creation
- Consistent styling and behavior

#### `RiceGrainAnalyzer`
- Main application class
- Organized UI creation into focused methods
- Clean separation of different UI sections

### 📊 Constants Organization

All configuration values are now centralized:

- **Layout Configuration**: Frame positions and sizes
- **Color Schemes**: Background and UI colors
- **Font Sizes**: Standardized font size categories
- **Text Content**: All Persian text strings
- **Data Categories**: Grain types, features, and classifications

## Build Instructions

### Prerequisites

```bash
pip install tkinter arabic-reshaper python-bidi
```

### Building Executable

```bash
pyinstaller --onefile --noconsole --add-data "fonts/Vazirmatn.ttf;fonts" rice_grain_analyzer_gui_cleaned.py
```

## File Structure

```
├── rice_grain_analyzer_gui_cleaned.py    # Main application file
├── fonts/
│   ├── Vazirmatn.ttf                     # Persian font for Windows
│   └── B Nazanin.ttf                     # Persian font for Linux
└── README.md                             # This documentation
```

## Usage

### Running the Application

```python
python rice_grain_analyzer_gui_cleaned.py
```

### Key Features

1. **Fullscreen Mode**: Application starts in fullscreen (press Escape to exit)
2. **Persian Text Support**: Proper RTL text rendering and reshaping
3. **Status Indicators**: Color-coded status for different operations
4. **Data Input Fields**: Readonly fields for displaying analysis results
5. **Interactive Controls**: Buttons for various analysis operations

## Technical Details

### Font Handling

The application automatically selects appropriate fonts based on the platform:
- **Windows**: Uses Vazir font family with Vazirmatn.ttf
- **Linux**: Uses B Nazanin font family
- **Fallback**: Arial font if Persian fonts are unavailable

### DPI Awareness

Windows DPI awareness is automatically enabled for better display on high-DPI screens.

### Layout System

The UI uses absolute positioning with predefined layout configurations for consistent appearance across different systems.

## Code Comparison

### Before (Original)
- Single monolithic `main()` function (~300+ lines)
- Hardcoded values throughout the code
- No type hints or documentation
- Procedural programming approach
- Repeated code patterns

### After (Cleaned)
- Modular class-based architecture
- Centralized configuration management
- Comprehensive documentation and type hints
- Reusable components and utilities
- Clean separation of concerns

## Development Guidelines

### Adding New Features

1. Add constants to the appropriate constant sections
2. Create new methods in the relevant class
3. Use the `UIComponents` factory for standard widgets
4. Follow the established naming conventions
5. Add proper type hints and docstrings

### Modifying UI Layout

1. Update `LAYOUT_CONFIG` for position changes
2. Modify color constants for theme changes
3. Use `FontManager` for font-related changes
4. Update text constants for content changes

## Dependencies

- `tkinter`: GUI framework (built-in with Python)
- `arabic_reshaper`: Persian text reshaping
- `python-bidi`: Bidirectional text support
- `typing`: Type hints support (Python 3.5+)

## License

This code is provided as-is for educational and development purposes.

## Contributing

When contributing to this codebase:

1. Maintain the established code structure
2. Add appropriate documentation
3. Use type hints for all new functions
4. Follow the existing naming conventions
5. Test on both Windows and Linux platforms