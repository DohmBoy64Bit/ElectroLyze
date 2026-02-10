# Electron Decompiler v2.0
### Python 3.13.7 Optimized Version

A modern, cross-platform tool for extracting, analyzing, and modifying Electron applications.

## 🚀 What's New in v2.0

### Python 3.13.7 Compatibility
- ✅ Fully compatible with Python 3.13.7
- ✅ Backward compatible with Python 3.9+
- ✅ Modern type hints throughout
- ✅ Optimized for latest Python features

### Major Improvements

#### Code Quality
- **Type Hints**: Full type annotations for better IDE support and code quality
- **Dataclasses**: Using `@dataclass` for configuration management
- **Enums**: Color themes defined as enums for better maintainability
- **PathLib**: Consistent use of `pathlib.Path` instead of string paths
- **Error Handling**: Enhanced exception handling with specific error types

#### Architecture
- **Class-based Design**: Better organized with separate methods for UI components
- **Separation of Concerns**: UI, logic, and file operations properly separated
- **Cross-platform Support**: Improved support for Windows, macOS, and Linux
- **Resource Management**: Better handling of file operations and processes

#### User Interface
- **Modern Dark Theme**: Enhanced visual design with emoji icons
- **Better Console Output**: Color-coded messages (info, success, error, warning)
- **Clear Console**: Added button to clear console output
- **Improved Logging**: Better structured log messages with visual indicators
- **About Dialog**: New about window with version information

#### Features
- **Enhanced Error Messages**: More descriptive error messages
- **Better Progress Indication**: Clear feedback for long-running operations
- **Automatic Backup**: Always creates backup before modifying files
- **Multiple Replacement Methods**: Fallback strategies for file replacement
- **Cross-platform File Opening**: Proper handling for Windows, macOS, Linux

#### Requirements Installer
- **Environment Validation**: Checks Python version and platform
- **Built-in Module Verification**: Validates all required built-in modules
- **Better npm Detection**: Improved Node.js and npm detection
- **Optional Packages**: Suggests useful optional packages
- **Interactive Installation**: User-friendly installation process
- **Detailed Feedback**: Clear status messages for each step

## 📋 Requirements

### System Requirements
- **Python**: 3.9 or higher (optimized for 3.13.7)
- **Node.js**: Latest LTS version (includes npm)
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux

### Python Built-in Modules
These come with Python and don't need installation:
- tkinter (GUI framework)
- pathlib (path handling)
- subprocess (process management)
- json (JSON parsing)
- platform (platform detection)
- tempfile (temporary files)
- re (regular expressions)
- ctypes (Windows-specific features)

### Node.js Packages
Automatically installed by the requirements script:
- asar (ASAR archive handling)
- electron-devtools-installer (development tools)
- source-map-explorer (source map analysis)

## 🔧 Installation

### Step 1: Install Python
Download and install Python 3.13.7 (or 3.9+) from:
- **Official**: https://www.python.org/downloads/
- **Windows Store**: Search for "Python 3.13"

### Step 2: Install Node.js
Download and install Node.js LTS from:
- https://nodejs.org/

### Step 3: Install Dependencies
Run the requirements installer:
```bash
python requirements.py
```

This will:
1. Verify your Python installation
2. Check for Node.js and npm
3. Install required npm packages globally
4. Show optional package recommendations

### Step 4: Run the Application
```bash
python electron-decompiler.py
```

**Note**: On Windows, run as Administrator for full functionality.

## 📖 Usage Guide

### 1. Select Application
- Click **Browse** to select an Electron `.exe` file
- The tool will automatically set up the output directory

### 2. Install Tools (First Time Only)
- Click **Install Required Tools**
- Wait for npm packages to install
- Check console for confirmation messages

### 3. Extract ASAR Archive
- Click **Extract ASAR Archive**
- Files will be extracted to a folder next to the script
- The folder will open automatically

### 4. Analyze (Optional)
- **Analyze Source Maps**: View available source maps
- **Setup Development Tools**: Get instructions for enabling DevTools

### 5. Modify Files
- Click **Edit Extracted Files** to open the directory
- Edit files using your preferred text editor
- Common files to modify:
  - `main.js` - Main process code
  - `renderer.js` - Renderer process code
  - `index.html` - Application UI
  - `package.json` - Configuration

### 6. Recompile & Apply
- Click **Recompile & Apply Changes**
- Automatic backup created (`.asar.backup`)
- Original file will be replaced
- Requires administrator/sudo privileges

## 🎨 Features

### Modern User Interface
- **Dark Theme**: Easy on the eyes during long sessions
- **Color-coded Output**: Info (blue), success (green), error (red), warning (orange)
- **Emoji Icons**: Visual indicators for different sections
- **Responsive Layout**: Adapts to window size

### File Operations
- **ASAR Extraction**: Unpack Electron app archives
- **Source Map Analysis**: View and analyze source maps
- **File Modification**: Edit any extracted file
- **Automatic Backup**: Never lose the original
- **Smart Recompilation**: Multiple fallback methods

### Developer Tools
- **Console Output**: Real-time feedback
- **Error Tracking**: Detailed error messages
- **Instructions**: Built-in help system
- **Cross-platform**: Works on Windows, macOS, Linux

## 🔍 Technical Details

### Code Structure
```
electron-decompiler.py
├── Theme (Enum)              # Color constants
├── AppConfig (dataclass)     # Configuration data
├── is_admin()                # Check privileges
└── ElectronAnalyzer (class)  # Main application
    ├── __init__()
    ├── _init_gui()
    ├── _configure_styles()
    ├── _setup_ui()
    ├── _create_*_frame()     # UI components
    ├── browse_app()
    ├── install_tools()
    ├── extract_asar()
    ├── analyze_source_maps()
    ├── setup_devtools()
    ├── edit_files()
    ├── recompile_changes()
    └── run()
```

### Key Improvements Over v1.0

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Type Hints | ❌ | ✅ |
| Dataclasses | ❌ | ✅ |
| PathLib | Partial | Full |
| Cross-platform | Limited | Full |
| Error Handling | Basic | Enhanced |
| UI Theme | Basic | Modern |
| Console Output | Plain | Color-coded |
| Code Organization | Mixed | Separated |
| Python 3.13 Compatible | ⚠️ | ✅ |

## ⚠️ Important Notes

### Legal & Ethical Use
- **Educational purposes only**
- Only modify applications you own or have permission to modify
- Respect software licenses and terms of service
- Some applications may have anti-tampering protections

### Limitations
- Some Electron apps use additional protections
- Code obfuscation may limit readability
- Modifications may break application functionality
- Always keep backups of working versions

### Security
- Run with appropriate privileges (admin/sudo)
- Be cautious when modifying system applications
- Scan extracted files if from untrusted sources
- Use in isolated/test environments when possible

## 🐛 Troubleshooting

### npm not found
**Solution**: Install Node.js from https://nodejs.org/ and restart terminal

### tkinter not available (Linux)
**Solution**: Install with package manager
```bash
sudo apt-get install python3-tk  # Debian/Ubuntu
sudo dnf install python3-tkinter  # Fedora
```

### Permission denied during recompilation
**Solution**: Run as administrator (Windows) or with sudo (Linux/macOS)

### ASAR extraction fails
**Solution**: 
- Verify the selected file is an Electron app
- Check that resources/app.asar exists
- Try running as administrator

### Files not opening
**Solution**: Set default programs for file types in your OS

## 📝 Changelog

### Version 2.0 (2024)
- Complete rewrite for Python 3.13.7 compatibility
- Added type hints throughout
- Implemented dataclasses and enums
- Enhanced UI with modern dark theme
- Improved error handling and logging
- Better cross-platform support
- Color-coded console output
- Added clear console button
- Enhanced requirements installer
- Better documentation

### Version 1.0 (Original)
- Initial release
- Basic ASAR extraction
- Simple UI
- Windows-focused

## 🤝 Contributing

Suggestions and improvements are welcome! When contributing:
1. Maintain Python 3.13.7 compatibility
2. Use type hints for all functions
3. Follow PEP 8 style guidelines
4. Add docstrings to new functions
5. Test on multiple platforms

## 📄 License

This tool is provided as-is for educational purposes. Use responsibly and ethically.

## 🙏 Credits

Built with:
- Python 3.13.7
- tkinter (GUI)
- Node.js & npm
- asar (Electron archive tool)

---

**Version**: 2.0  
**Python**: 3.13.7 Compatible  
**Last Updated**: 2026 
**Status**: Active Development
