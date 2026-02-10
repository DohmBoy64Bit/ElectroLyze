"""
Electron Application Decompiler
Compatible with Python 3.13.7
A tool for extracting, analyzing, and modifying Electron applications
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path
from typing import Optional, List, Set, Dict, Callable
from dataclasses import dataclass
from enum import Enum
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import platform
import tempfile
import re

# Platform-specific imports
if platform.system() == 'Windows':
    import winreg
    import ctypes


class Theme(Enum):
    """Color theme constants"""
    BG = '#1a1a1a'
    FG = '#ffffff'
    BUTTON_BG = '#2d2d2d'
    BUTTON_HOVER = '#3d3d3d'
    ACCENT = '#4a9eff'
    FRAME_BG = '#202020'
    CONSOLE_BG = '#000000'
    CONSOLE_FG = '#4a9eff'
    ERROR = '#ff4a4a'
    SUCCESS = '#4aff4a'


@dataclass
class AppConfig:
    """Application configuration"""
    script_dir: Path
    app_path: Optional[Path] = None
    output_dir: Optional[Path] = None
    npm_path: Optional[Path] = None


def is_admin() -> bool:
    """Check if running with administrator privileges (Windows only)"""
    if platform.system() != 'Windows':
        return True  # Assume sufficient privileges on non-Windows
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except (AttributeError, OSError):
        return False


class ElectronAnalyzer:
    """Main application class for Electron decompilation and analysis"""
    
    def __init__(self):
        """Initialize the Electron Analyzer application"""
        try:
            # Determine script directory
            if getattr(sys, 'frozen', False):
                script_dir = Path(sys.executable).parent
            else:
                script_dir = Path(__file__).parent.resolve()
            
            # Initialize configuration
            self.config = AppConfig(script_dir=script_dir)
            self.extracted_files: List[Path] = []
            self.modified_files: Set[Path] = set()
            
            # Initialize GUI
            self._init_gui()
            
            # Find NPM installation
            self.find_and_setup_npm()
            
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Error during startup: {e}")
            raise

    def _init_gui(self) -> None:
        """Initialize the graphical user interface"""
        self.root = tk.Tk()
        self.root.title("Electron Decompiler - Python 3.13.7")
        self.root.geometry("900x700")
        self.root.configure(bg=Theme.BG.value)
        
        # Configure styles
        self._configure_styles()
        
        # Setup UI components
        self._setup_ui()

    def _configure_styles(self) -> None:
        """Configure modern dark theme styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame style
        style.configure('Dark.TFrame', background=Theme.FRAME_BG.value)
        
        # Label style
        style.configure('Dark.TLabel',
                       background=Theme.FRAME_BG.value,
                       foreground=Theme.FG.value)
        
        # Button style
        style.configure('Dark.TButton',
                       background=Theme.BUTTON_BG.value,
                       foreground=Theme.FG.value,
                       borderwidth=0,
                       focuscolor=Theme.ACCENT.value,
                       relief='flat',
                       padding=10)
        
        style.map('Dark.TButton',
                 background=[('active', Theme.BUTTON_HOVER.value)])
        
        # LabelFrame style
        style.configure('Dark.TLabelframe',
                       background=Theme.FRAME_BG.value,
                       foreground=Theme.FG.value,
                       bordercolor=Theme.BUTTON_BG.value)
        
        style.configure('Dark.TLabelframe.Label',
                       background=Theme.FRAME_BG.value,
                       foreground=Theme.ACCENT.value,
                       font=('Segoe UI', 10, 'bold'))

    def _setup_ui(self) -> None:
        """Setup the user interface components"""
        # Configure menu
        self.root.option_add('*Menu.background', Theme.BUTTON_BG.value)
        self.root.option_add('*Menu.foreground', Theme.FG.value)
        self.root.option_add('*Menu.selectColor', Theme.ACCENT.value)
        
        # Menu bar
        menubar = tk.Menu(self.root, bg=Theme.BUTTON_BG.value, fg=Theme.FG.value)
        self.root.config(menu=menubar)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg=Theme.BUTTON_BG.value, fg=Theme.FG.value)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Instructions", command=self.show_instructions)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Main frame
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Application selection
        self._create_app_selection_frame(main_frame)
        
        # Tools installation
        self._create_tools_frame(main_frame)
        
        # Analysis options
        self._create_analysis_frame(main_frame)
        
        # Modification options
        self._create_modification_frame(main_frame)
        
        # Console output
        self._create_console_frame(main_frame)

    def _create_app_selection_frame(self, parent: ttk.Frame) -> None:
        """Create application selection frame"""
        app_frame = ttk.LabelFrame(parent, text="📱 Application Selection", style='Dark.TLabelframe', padding=10)
        app_frame.pack(fill=tk.X, pady=5)
        
        self.app_path_var = tk.StringVar()
        entry = tk.Entry(app_frame,
                        textvariable=self.app_path_var,
                        bg=Theme.BUTTON_BG.value,
                        fg=Theme.FG.value,
                        insertbackground=Theme.FG.value,
                        relief='flat',
                        font=('Consolas', 10))
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(app_frame,
                              text="Browse",
                              command=self.browse_app,
                              style='Dark.TButton')
        browse_btn.pack(side=tk.LEFT)

    def _create_tools_frame(self, parent: ttk.Frame) -> None:
        """Create tools installation frame"""
        tools_frame = ttk.LabelFrame(parent, text="🔧 Tools Installation", style='Dark.TLabelframe', padding=10)
        tools_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(tools_frame,
                  text="Install Required Tools",
                  command=self.install_tools,
                  style='Dark.TButton').pack(fill=tk.X)

    def _create_analysis_frame(self, parent: ttk.Frame) -> None:
        """Create analysis options frame"""
        analysis_frame = ttk.LabelFrame(parent, text="🔍 Analysis Options", style='Dark.TLabelframe', padding=10)
        analysis_frame.pack(fill=tk.X, pady=5)
        
        buttons = [
            ("Extract ASAR Archive", self.extract_asar),
            ("Analyze Source Maps", self.analyze_source_maps),
            ("Setup Development Tools", self.setup_devtools)
        ]
        
        for text, command in buttons:
            ttk.Button(analysis_frame,
                      text=text,
                      command=command,
                      style='Dark.TButton').pack(fill=tk.X, pady=3)

    def _create_modification_frame(self, parent: ttk.Frame) -> None:
        """Create modification options frame"""
        mod_frame = ttk.LabelFrame(parent, text="✏️ Modification Options", style='Dark.TLabelframe', padding=10)
        mod_frame.pack(fill=tk.X, pady=5)
        
        buttons = [
            ("Edit Extracted Files", self.edit_files),
            ("Recompile & Apply Changes", self.recompile_changes)
        ]
        
        for text, command in buttons:
            ttk.Button(mod_frame,
                      text=text,
                      command=command,
                      style='Dark.TButton').pack(fill=tk.X, pady=3)

    def _create_console_frame(self, parent: ttk.Frame) -> None:
        """Create console output frame"""
        console_frame = ttk.LabelFrame(parent, text="📋 Console Output", style='Dark.TLabelframe', padding=10)
        console_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create text widget with scrollbar
        text_frame = tk.Frame(console_frame, bg=Theme.CONSOLE_BG.value)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.console = tk.Text(text_frame,
                             bg=Theme.CONSOLE_BG.value,
                             fg=Theme.CONSOLE_FG.value,
                             insertbackground=Theme.FG.value,
                             relief='flat',
                             padx=10,
                             pady=10,
                             font=('Consolas', 9),
                             yscrollcommand=scrollbar.set)
        self.console.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.console.yview)
        
        # Add clear button
        clear_btn = ttk.Button(console_frame,
                              text="Clear Console",
                              command=self.clear_console,
                              style='Dark.TButton')
        clear_btn.pack(fill=tk.X, pady=(5, 0))

    def log(self, message: str, level: str = 'info') -> None:
        """
        Add message to console with optional color coding
        
        Args:
            message: The message to log
            level: Message level ('info', 'success', 'error', 'warning')
        """
        if not hasattr(self, 'console'):
            print(message)
            return
        
        # Color mapping
        colors = {
            'info': Theme.CONSOLE_FG.value,
            'success': Theme.SUCCESS.value,
            'error': Theme.ERROR.value,
            'warning': '#ffa500'
        }
        
        color = colors.get(level, Theme.CONSOLE_FG.value)
        
        self.console.insert(tk.END, f"{message}\n")
        # Apply color to the last line
        last_line = self.console.index('end-1c linestart')
        self.console.tag_add(level, last_line, 'end-1c')
        self.console.tag_config(level, foreground=color)
        self.console.see(tk.END)
        self.root.update()

    def clear_console(self) -> None:
        """Clear the console output"""
        self.console.delete('1.0', tk.END)
        self.log("Console cleared", 'info')

    def find_and_setup_npm(self) -> None:
        """Locate npm installation on the system"""
        self.log("Searching for npm installation...", 'info')
        
        npm_locations: List[str] = []
        
        if platform.system() == 'Windows':
            # Check common Windows locations
            npm_locations = [
                r'C:\Program Files\nodejs\npm.cmd',
                r'C:\Program Files (x86)\nodejs\npm.cmd',
                str(Path.home() / 'AppData' / 'Roaming' / 'npm' / 'npm.cmd'),
            ]
            
            # Check PATH environment variable
            try:
                npm_in_path = shutil.which('npm')
                if npm_in_path:
                    npm_locations.insert(0, npm_in_path)
            except Exception:
                pass
        else:
            # Unix-like systems
            npm_locations = [
                '/usr/local/bin/npm',
                '/usr/bin/npm',
                str(Path.home() / '.nvm' / 'versions' / 'node' / '*' / 'bin' / 'npm'),
            ]
            npm_in_path = shutil.which('npm')
            if npm_in_path:
                npm_locations.insert(0, npm_in_path)
        
        # Find npm
        for location in npm_locations:
            path = Path(location)
            if path.exists():
                self.config.npm_path = path
                self.log(f"✓ Found npm at: {path}", 'success')
                return
        
        self.log("⚠ npm not found. Please install Node.js from https://nodejs.org/", 'warning')

    def browse_app(self) -> None:
        """Open file dialog to select Electron application"""
        filetypes = [("Executable files", "*.exe"), ("All files", "*.*")] if platform.system() == 'Windows' else [("All files", "*.*")]
        
        filename = filedialog.askopenfilename(
            title="Select Electron Application",
            filetypes=filetypes
        )
        
        if filename:
            self.config.app_path = Path(filename)
            self.app_path_var.set(str(self.config.app_path))
            
            # Set output directory
            app_name = self.config.app_path.stem
            self.config.output_dir = self.config.script_dir / app_name
            
            self.log(f"Selected application: {self.config.app_path}", 'success')
            self.log(f"Output directory: {self.config.output_dir}", 'info')

    def install_tools(self) -> None:
        """Install required npm packages"""
        if not self.config.npm_path:
            messagebox.showerror("Error", "npm not found. Please install Node.js first.")
            return
        
        packages = [
            'asar',
            'electron-devtools-installer',
            'source-map-explorer'
        ]
        
        self.log("Installing required npm packages...", 'info')
        
        for package in packages:
            try:
                self.log(f"Installing {package}...", 'info')
                result = subprocess.run(
                    [str(self.config.npm_path), 'install', '-g', package],
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                
                if result.returncode == 0:
                    self.log(f"✓ {package} installed successfully", 'success')
                else:
                    self.log(f"✗ Failed to install {package}: {result.stderr}", 'error')
                    
            except subprocess.TimeoutExpired:
                self.log(f"✗ Installation of {package} timed out", 'error')
            except Exception as e:
                self.log(f"✗ Error installing {package}: {e}", 'error')
        
        self.log("Installation complete!", 'success')

    def extract_asar(self) -> None:
        """Extract ASAR archive from Electron application"""
        if not self.config.app_path or not self.config.app_path.exists():
            messagebox.showerror("Error", "Please select a valid application first")
            return
        
        try:
            self.log("Searching for ASAR files...", 'info')
            
            # Find resources directory
            app_dir = self.config.app_path.parent
            resources_dir = app_dir / 'resources'
            
            if not resources_dir.exists():
                self.log("✗ Resources directory not found", 'error')
                return
            
            # Find ASAR files
            asar_files = list(resources_dir.glob('*.asar'))
            
            if not asar_files:
                self.log("✗ No ASAR files found", 'error')
                return
            
            self.log(f"Found {len(asar_files)} ASAR file(s)", 'success')
            
            # Extract each ASAR file
            for asar_file in asar_files:
                output_path = self.config.output_dir / asar_file.stem
                output_path.mkdir(parents=True, exist_ok=True)
                
                self.log(f"Extracting {asar_file.name}...", 'info')
                
                # Use asar npm package
                cmd = [str(self.config.npm_path), 'exec', 'asar', 'extract', 
                       str(asar_file), str(output_path)]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.log(f"✓ Extracted to: {output_path}", 'success')
                    self.extracted_files = list(output_path.rglob('*'))
                    
                    # Open output directory
                    if platform.system() == 'Windows':
                        os.startfile(output_path)
                    elif platform.system() == 'Darwin':
                        subprocess.run(['open', str(output_path)])
                    else:
                        subprocess.run(['xdg-open', str(output_path)])
                else:
                    self.log(f"✗ Extraction failed: {result.stderr}", 'error')
                    
        except Exception as e:
            self.log(f"✗ Error during extraction: {e}", 'error')
            messagebox.showerror("Error", f"Extraction failed: {e}")

    def analyze_source_maps(self) -> None:
        """Analyze source maps in extracted files"""
        if not self.config.output_dir or not self.config.output_dir.exists():
            messagebox.showerror("Error", "Please extract ASAR first")
            return
        
        self.log("Analyzing source maps...", 'info')
        
        # Find .map files
        map_files = list(self.config.output_dir.rglob('*.map'))
        
        if not map_files:
            self.log("⚠ No source map files found", 'warning')
            return
        
        self.log(f"Found {len(map_files)} source map file(s)", 'success')
        
        for map_file in map_files:
            self.log(f"  • {map_file.relative_to(self.config.output_dir)}", 'info')

    def setup_devtools(self) -> None:
        """Setup development tools for Electron app"""
        self.log("Development tools setup instructions:", 'info')
        self.log("1. Extract the ASAR archive", 'info')
        self.log("2. Modify main.js to enable DevTools", 'info')
        self.log("3. Add: mainWindow.webContents.openDevTools()", 'info')
        self.log("4. Recompile the changes", 'info')

    def edit_files(self) -> None:
        """Open extracted files for editing"""
        if not self.config.output_dir or not self.config.output_dir.exists():
            messagebox.showerror("Error", "Please extract ASAR first")
            return
        
        # Open output directory
        try:
            if platform.system() == 'Windows':
                os.startfile(self.config.output_dir)
            elif platform.system() == 'Darwin':
                subprocess.run(['open', str(self.config.output_dir)])
            else:
                subprocess.run(['xdg-open', str(self.config.output_dir)])
            
            self.log(f"Opened directory: {self.config.output_dir}", 'success')
            self.log("Edit your files and then click 'Recompile & Apply Changes'", 'info')
            
        except Exception as e:
            self.log(f"✗ Error opening directory: {e}", 'error')

    def recompile_changes(self) -> None:
        """Recompile modified files back into ASAR"""
        if not self.config.output_dir or not self.config.output_dir.exists():
            messagebox.showerror("Error", "No extracted files found")
            return
        
        if not self.config.app_path:
            messagebox.showerror("Error", "Original application path not found")
            return
        
        try:
            self.log("Starting recompilation...", 'info')
            
            # Find original ASAR
            app_dir = self.config.app_path.parent
            resources_dir = app_dir / 'resources'
            asar_files = list(resources_dir.glob('*.asar'))
            
            if not asar_files:
                raise FileNotFoundError("Original ASAR file not found")
            
            original_asar = asar_files[0]
            
            # Create backup
            backup_path = original_asar.with_suffix('.asar.backup')
            if not backup_path.exists():
                shutil.copy2(original_asar, backup_path)
                self.log(f"✓ Created backup: {backup_path.name}", 'success')
            
            # Pack new ASAR
            source_dir = self.config.output_dir / original_asar.stem
            new_asar = self.config.output_dir / 'app.asar'
            
            self.log(f"Packing {source_dir.name}...", 'info')
            
            cmd = [str(self.config.npm_path), 'exec', 'asar', 'pack',
                   str(source_dir), str(new_asar)]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"Packing failed: {result.stderr}")
            
            self.log("✓ Successfully created new ASAR", 'success')
            
            # Replace original ASAR
            if self._replace_asar(new_asar, original_asar):
                self.log("✓ Successfully replaced original ASAR", 'success')
                messagebox.showinfo("Success",
                                  f"Changes have been applied!\n"
                                  f"Backup saved as: {backup_path.name}")
            else:
                raise Exception("Failed to replace ASAR file")
                
        except Exception as e:
            self.log(f"✗ Recompilation failed: {e}", 'error')
            messagebox.showerror("Error", f"Recompilation failed: {e}")

    def _replace_asar(self, new_asar: Path, original_asar: Path) -> bool:
        """
        Replace original ASAR file with new one
        
        Args:
            new_asar: Path to new ASAR file
            original_asar: Path to original ASAR file
            
        Returns:
            True if successful, False otherwise
        """
        methods: List[Callable[[], None]] = [
            # Method 1: Direct replacement
            lambda: shutil.copy2(new_asar, original_asar),
        ]
        
        # Windows-specific methods
        if platform.system() == 'Windows':
            methods.extend([
                # Method 2: Take ownership
                lambda: self._take_ownership_and_replace(new_asar, original_asar),
                # Method 3: PowerShell elevated copy
                lambda: subprocess.run(
                    f'powershell Start-Process cmd -Verb RunAs -ArgumentList '
                    f'"/c copy /Y \\"{new_asar}\\" \\"{original_asar}\\""',
                    shell=True,
                    check=True
                )
            ])
        
        for i, method in enumerate(methods, 1):
            try:
                self.log(f"Attempting replacement method {i}...", 'info')
                method()
                if original_asar.exists():
                    return True
            except Exception as e:
                self.log(f"Method {i} failed: {e}", 'warning')
                continue
        
        return False

    def _take_ownership_and_replace(self, new_asar: Path, original_asar: Path) -> None:
        """Take ownership of file and replace it (Windows only)"""
        if platform.system() != 'Windows':
            raise OSError("This method is only available on Windows")
        
        subprocess.run(['takeown', '/F', str(original_asar)], shell=True, check=True)
        subprocess.run(['icacls', str(original_asar), '/grant', 'administrators:F'],
                      shell=True, check=True)
        shutil.copy2(new_asar, original_asar)

    def show_instructions(self) -> None:
        """Show instructions window"""
        readme = tk.Toplevel(self.root)
        readme.title("Instructions - Electron Decompiler")
        readme.geometry("700x500")
        readme.configure(bg=Theme.BG.value)
        
        # Create frame
        frame = tk.Frame(readme, bg=Theme.BG.value)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Text widget
        text = tk.Text(frame,
                      wrap=tk.WORD,
                      padx=15,
                      pady=15,
                      bg=Theme.CONSOLE_BG.value,
                      fg=Theme.FG.value,
                      insertbackground=Theme.FG.value,
                      font=('Segoe UI', 10))
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(frame, command=text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text.config(yscrollcommand=scrollbar.set)
        
        instructions = """
╔══════════════════════════════════════════════════════════╗
║        Electron Application Decompiler v2.0              ║
║        Compatible with Python 3.13.7                     ║
╚══════════════════════════════════════════════════════════╝

📋 PREREQUISITES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Install Node.js from https://nodejs.org/
2. Run as Administrator (Windows) or with sudo (Linux/Mac)
3. Click "Install Required Tools" before first use

📖 STEP-BY-STEP GUIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. APPLICATION SELECTION
   • Click "Browse" to select your Electron .exe file
   • Output directory will be created automatically

2. TOOLS INSTALLATION
   • Click "Install Required Tools"
   • Wait for npm packages to install
   • Check console for success messages

3. EXTRACTION
   • Click "Extract ASAR Archive"
   • Files will be extracted to: [app_name]/
   • Directory will open automatically

4. ANALYSIS
   • "Analyze Source Maps" - View available source maps
   • "Setup Development Tools" - Get DevTools instructions

5. MODIFICATION
   • Click "Edit Extracted Files" to open the directory
   • Modify files using your preferred text editor
   
   Common files to edit:
   ├── main.js          → Main process code
   ├── renderer.js      → Renderer process code
   ├── index.html       → Application UI
   └── package.json     → App configuration

6. RECOMPILATION
   • Click "Recompile & Apply Changes"
   • Backup created automatically (.asar.backup)
   • Original file will be replaced

🔧 TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• npm not found → Install Node.js and restart
• Extraction fails → Check app directory structure
• Recompile fails → Run as administrator
• Console shows detailed error messages

⚠️ IMPORTANT NOTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Always backup before modifying applications
• Some apps may have additional protection
• Modifications might break functionality
• Use for educational purposes only

💡 TIPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Use a good code editor (VS Code, Sublime Text)
• Test modifications in a safe environment
• Keep backups of working versions
• Check console output for detailed information
"""
        
        text.insert('1.0', instructions)
        text.config(state='disabled')
        
        # Close button
        close_btn = ttk.Button(readme, text="Close", command=readme.destroy, style='Dark.TButton')
        close_btn.pack(pady=10)

    def show_about(self) -> None:
        """Show about dialog"""
        about_text = (
            "Electron Application Decompiler\n\n"
            "Version: 2.0\n"
            "Python: 3.13.7 Compatible\n\n"
            "A tool for extracting, analyzing, and modifying\n"
            "Electron-based applications.\n\n"
            "Features:\n"
            "• ASAR extraction and packing\n"
            "• Source map analysis\n"
            "• File modification support\n"
            "• Automatic backup creation\n\n"
            "Use responsibly and ethically."
        )
        messagebox.showinfo("About", about_text)

    def run(self) -> None:
        """Start the application main loop"""
        try:
            self.log("Electron Decompiler started successfully", 'success')
            self.log("Python 3.13.7 compatible version", 'info')
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Runtime Error", f"Error during execution: {e}")
            raise


def main():
    """Main entry point for the application"""
    try:
        # Check Python version
        if sys.version_info < (3, 9):
            print("ERROR: This application requires Python 3.9 or higher")
            print(f"Current version: {sys.version}")
            input("Press Enter to exit...")
            sys.exit(1)
        
        # Create and run application
        app = ElectronAnalyzer()
        app.run()
        
    except KeyboardInterrupt:
        print("\nApplication terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"Startup error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
