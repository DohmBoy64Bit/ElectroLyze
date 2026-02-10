# 🚀 Quick Start Guide - Electron Decompiler

## Get Started in 3 Minutes!

### Prerequisites Checklist
- [ ] Python 3.9+ installed (3.13.7 recommended)
- [ ] Node.js LTS installed
- [ ] Administrator/sudo access

---

## Step-by-Step Setup

### 1️⃣ Install Python (if not already installed)
**Windows:**
```bash
# Download from python.org or use Windows Store
# Search for "Python 3.13" in Microsoft Store
```

**macOS:**
```bash
brew install python@3.13
# or download from python.org
```

**Linux:**
```bash
sudo apt update
sudo apt install python3.13 python3-tk
```

### 2️⃣ Install Node.js
Visit: https://nodejs.org/
- Download the **LTS version**
- Run the installer
- Verify installation:
```bash
node --version
npm --version
```

### 3️⃣ Install Dependencies
```bash
# Navigate to the tool directory
cd /path/to/electron-decompiler

# Run requirements installer
python requirements.py
# Follow the prompts and type 'y' to install npm packages
```

### 4️⃣ Run the Application
**Windows (as Administrator):**
```bash
# Right-click "Command Prompt" → "Run as administrator"
python electron-decompiler.py
```

**macOS/Linux:**
```bash
sudo python electron-decompiler.py
```

---

## Your First Decompilation

### 1. Select an Electron App
- Click **Browse**
- Select the `.exe` file of your Electron application
- Example locations:
  - `C:\Program Files\AppName\AppName.exe`
  - `C:\Users\YourName\AppData\Local\AppName\AppName.exe`

### 2. Install Tools (First Time Only)
- Click **Install Required Tools**
- Wait for completion (check green success messages)

### 3. Extract the Application
- Click **Extract ASAR Archive**
- Wait for extraction to complete
- Folder will open automatically

### 4. Explore the Code
Your extracted files are now in:
```
electron-decompiler/
└── AppName/
    └── app/
        ├── main.js          ← Main process
        ├── renderer.js      ← UI logic
        ├── index.html       ← Main window
        ├── package.json     ← App config
        └── ...more files
```

### 5. Make Changes (Optional)
- Click **Edit Extracted Files**
- Modify files with any text editor
- Save your changes

### 6. Recompile (If you made changes)
- Click **Recompile & Apply Changes**
- Backup is created automatically
- Original file is replaced

---

## Common Use Cases

### 🔍 Just Exploring
```
1. Extract ASAR Archive
2. Browse the files
3. Done! No need to recompile
```

### ✏️ Making Modifications
```
1. Extract ASAR Archive
2. Edit Extracted Files
3. Make your changes
4. Recompile & Apply Changes
```

### 🛠️ Enabling DevTools
```
1. Extract ASAR Archive
2. Open main.js
3. Add: mainWindow.webContents.openDevTools()
4. Recompile & Apply Changes
5. Run the app - DevTools will open!
```

---

## Troubleshooting Quick Fixes

### ❌ "npm not found"
**Fix:** Install Node.js from https://nodejs.org/

### ❌ "Permission denied"
**Fix:** Run as Administrator (Windows) or with sudo (Linux/macOS)

### ❌ "tkinter not available"
**Linux Fix:**
```bash
sudo apt-get install python3-tk
```

### ❌ "No ASAR files found"
**Fix:** Make sure you selected an Electron application. Check if there's a `resources` folder next to the exe.

---

## File Locations

### Where are my extracted files?
```
electron-decompiler/     ← Tool directory
└── AppName/            ← Your extracted app
    └── app/            ← Actual files
```

### Where are backups saved?
```
OriginalApp/
└── resources/
    ├── app.asar        ← Current version
    └── app.asar.backup ← Your backup
```

---

## Tips for Success

### ✅ DO:
- Always run the tool with admin/sudo privileges
- Keep backups of working applications
- Test modifications in a safe environment
- Read console messages for detailed info

### ❌ DON'T:
- Modify system applications without backups
- Ignore error messages in the console
- Forget to install Node.js first
- Edit files while the app is running

---

## Example Workflow

Here's a real example of customizing Discord (for educational purposes):

```bash
# 1. Install everything
python requirements.py

# 2. Run the tool as admin
python electron-decompiler.py

# 3. In the GUI:
- Browse → Select Discord.exe
- Extract ASAR Archive
- Wait for extraction

# 4. Make changes (example):
- Open: AppName/app/main.js
- Find: mainWindow = new BrowserWindow({...})
- Add after: mainWindow.webContents.openDevTools()
- Save the file

# 5. Recompile:
- Click "Recompile & Apply Changes"
- Wait for success message

# 6. Test:
- Run Discord
- DevTools should open automatically!
```

---

## Next Steps

Once you're comfortable with the basics:

1. **Explore Source Maps** - Click "Analyze Source Maps" to understand code structure
2. **Read the Full README** - Check README.md for advanced features
3. **Experiment Safely** - Try modifications on non-critical applications first
4. **Learn Electron** - Understanding Electron helps you make better modifications

---

## Getting Help

### Console Output
The console shows detailed information:
- 🔵 **Blue** = Info messages
- 🟢 **Green** = Success
- 🔴 **Red** = Errors
- 🟠 **Orange** = Warnings

### Built-in Help
Click **Help → Instructions** in the application menu for detailed instructions.

### Common Files to Look For
- `main.js` - Application startup and main process
- `renderer.js` - UI and frontend logic
- `preload.js` - Bridge between main and renderer
- `index.html` - Main application window
- `package.json` - App configuration and metadata

---

## Safety Reminders

⚠️ **Important:**
- This tool is for educational purposes
- Only modify applications you own
- Always create backups
- Test in safe environments
- Respect software licenses

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Install dependencies | `python requirements.py` |
| Run tool (Windows) | `python electron-decompiler.py` (as admin) |
| Run tool (Linux/Mac) | `sudo python electron-decompiler.py` |
| Check Python version | `python --version` |
| Check Node.js | `node --version` |
| Check npm | `npm --version` |

---

**Ready to go!** 🎉

Start the application and begin exploring Electron apps. Remember to check the console output for helpful messages!

For detailed information, see **README.md**.
