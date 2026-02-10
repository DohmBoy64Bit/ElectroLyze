"""
Requirements Installer for Electron Decompiler
Compatible with Python 3.13.7
Installs necessary Node.js packages and verifies Python environment
"""

import subprocess
import sys
import os
import platform
from pathlib import Path
from typing import List, Tuple


class RequirementsInstaller:
    """Handle installation of required dependencies"""
    
    def __init__(self):
        self.python_version = sys.version_info
        self.platform = platform.system()
        
    def check_python_version(self) -> bool:
        """Verify Python version meets requirements"""
        print("=" * 60)
        print("Python Environment Check")
        print("=" * 60)
        print(f"Python Version: {sys.version}")
        print(f"Platform: {self.platform}")
        print(f"Architecture: {platform.machine()}")
        print()
        
        if self.python_version < (3, 9):
            print("❌ ERROR: Python 3.9 or higher is required")
            print(f"   Current version: {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}")
            return False
        
        print("✓ Python version is compatible")
        return True
    
    def verify_builtin_modules(self) -> bool:
        """Verify that required built-in modules are available"""
        print("\n" + "=" * 60)
        print("Verifying Built-in Python Modules")
        print("=" * 60)
        
        required_modules = [
            ('tkinter', 'GUI framework'),
            ('pathlib', 'Path handling'),
            ('ctypes', 'C library interface (Windows)'),
            ('subprocess', 'Process management'),
            ('json', 'JSON parsing'),
            ('platform', 'Platform information'),
            ('tempfile', 'Temporary files'),
            ('re', 'Regular expressions'),
        ]
        
        all_available = True
        
        for module_name, description in required_modules:
            try:
                __import__(module_name)
                print(f"✓ {module_name:<15} - {description}")
            except ImportError:
                print(f"❌ {module_name:<15} - {description} (NOT FOUND)")
                all_available = False
                
                if module_name == 'tkinter':
                    print(f"   Install tkinter using:")
                    if self.platform == 'Linux':
                        print(f"   sudo apt-get install python3-tk")
                    elif self.platform == 'Darwin':
                        print(f"   Python from python.org includes tkinter")
        
        return all_available
    
    def check_nodejs(self) -> Tuple[bool, str]:
        """Check if Node.js is installed"""
        print("\n" + "=" * 60)
        print("Node.js Environment Check")
        print("=" * 60)
        
        try:
            # Check Node.js
            node_result = subprocess.run(
                ['node', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if node_result.returncode == 0:
                node_version = node_result.stdout.strip()
                print(f"✓ Node.js found: {node_version}")
            else:
                print("❌ Node.js not responding properly")
                return False, ""
            
            # Check npm
            npm_result = subprocess.run(
                ['npm', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if npm_result.returncode == 0:
                npm_version = npm_result.stdout.strip()
                print(f"✓ npm found: {npm_version}")
                return True, npm_version
            else:
                print("❌ npm not found")
                return False, ""
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("❌ Node.js not found!")
            print("\n📥 Install Node.js from: https://nodejs.org/")
            print("   Recommended: LTS (Long Term Support) version")
            return False, ""
    
    def install_node_packages(self) -> bool:
        """Install required Node.js packages"""
        print("\n" + "=" * 60)
        print("Installing Node.js Packages")
        print("=" * 60)
        
        # Essential packages for Electron decompilation
        packages = [
            ('asar', 'ASAR archive packing/unpacking'),
            ('electron-devtools-installer', 'Development tools installer'),
            ('source-map-explorer', 'Source map analysis'),
        ]
        
        success_count = 0
        
        for package_name, description in packages:
            print(f"\n📦 Installing {package_name}...")
            print(f"   Description: {description}")
            
            try:
                result = subprocess.run(
                    ['npm', 'install', '-g', package_name],
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                
                if result.returncode == 0:
                    print(f"   ✓ {package_name} installed successfully")
                    success_count += 1
                else:
                    print(f"   ❌ Failed to install {package_name}")
                    if result.stderr:
                        print(f"   Error: {result.stderr[:200]}")
                    
            except subprocess.TimeoutExpired:
                print(f"   ❌ Installation timed out for {package_name}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print(f"\n{'=' * 60}")
        print(f"Installation Summary: {success_count}/{len(packages)} packages installed")
        print("=" * 60)
        
        return success_count == len(packages)
    
    def check_pip_packages(self) -> None:
        """Check if any optional pip packages would be useful"""
        print("\n" + "=" * 60)
        print("Optional Python Packages")
        print("=" * 60)
        
        optional_packages = [
            ('pillow', 'Image processing (if working with icons)'),
            ('beautifulsoup4', 'HTML parsing (if analyzing HTML)'),
            ('requests', 'HTTP requests (for downloading resources)'),
        ]
        
        print("\nOptional packages that may enhance functionality:")
        for package, description in optional_packages:
            try:
                __import__(package)
                print(f"✓ {package:<20} - {description} [INSTALLED]")
            except ImportError:
                print(f"○ {package:<20} - {description} [NOT INSTALLED]")
        
        print("\nTo install optional packages:")
        print(f"python -m pip install pillow beautifulsoup4 requests")
    
    def run_installation(self) -> bool:
        """Run complete installation process"""
        print("\n")
        print("╔══════════════════════════════════════════════════════════╗")
        print("║   Electron Decompiler - Requirements Installer          ║")
        print("║   Python 3.13.7 Compatible                              ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print()
        
        # Check Python version
        if not self.check_python_version():
            return False
        
        # Verify built-in modules
        if not self.verify_builtin_modules():
            print("\n⚠️  Some built-in modules are missing.")
            print("   Please install them before continuing.")
            return False
        
        # Check Node.js
        nodejs_available, npm_version = self.check_nodejs()
        if not nodejs_available:
            return False
        
        # Install Node.js packages
        print("\n⚠️  This will install npm packages globally.")
        response = input("Continue with npm package installation? (y/n): ")
        
        if response.lower() != 'y':
            print("Installation cancelled by user.")
            return False
        
        packages_installed = self.install_node_packages()
        
        # Show optional packages
        self.check_pip_packages()
        
        # Final summary
        print("\n" + "=" * 60)
        print("Installation Complete!")
        print("=" * 60)
        
        if packages_installed:
            print("✓ All required packages installed successfully")
            print("\nYou can now run: python electron-decompiler.py")
        else:
            print("⚠️  Some packages failed to install")
            print("   The application may still work with limited functionality")
        
        return packages_installed


def main():
    """Main entry point"""
    try:
        installer = RequirementsInstaller()
        success = installer.run_installation()
        
        print("\n" + "=" * 60)
        input("Press Enter to exit...")
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
