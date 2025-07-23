"""
Dependency Management Module
Handles automatic installation of required Python packages.
"""

import subprocess
import sys


def install_required_packages():
    """Install required dependencies if they are not already available."""
    required_packages = ['markdown', 'beautifulsoup4']
    
    for package in required_packages:
        try:
            # Try to import the package (adjust for package naming differences)
            import_name = package.replace('-', '_')
            if package == 'beautifulsoup4':
                import_name = 'bs4'
            
            __import__(import_name)
            print(f"✓ {package} is already installed")
            
        except ImportError:
            print(f"Installing {package}...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✓ Successfully installed {package}")
            except subprocess.CalledProcessError as e:
                print(f"✗ Failed to install {package}: {e}")
                raise Exception(f"Could not install required package: {package}")


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 6):
        raise Exception("Python 3.6 or higher is required")
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def initialize_dependencies():
    """Initialize all dependencies and perform system checks."""
    print("Checking system requirements...")
    check_python_version()
    
    print("\nChecking required packages...")
    install_required_packages()
    
    print("\n" + "="*50)
    print("All dependencies satisfied!")
    print("="*50 + "\n")
