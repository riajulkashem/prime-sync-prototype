import PyInstaller.__main__
import platform
import os
import shutil

def build_app():
    # Determine the platform
    system = platform.system()

    # Common PyInstaller arguments
    args = [
        "main.py",  # Entry point (updated to match your structure)
        "--name", "PrimeSync",  # Name of the executable
        "--windowed",  # GUI mode (no console)
        "--distpath", "dist",  # Output directory
        "--workpath", "build",  # Temporary build directory
    ]

    # Add the icons/ directory and database file
    separator = ";" if system == "Windows" else ":"
    args.extend([
        "--add-data", f"icons{separator}icons",
        "--add-data", f"attendance.db{separator}."
    ])

    # Platform-specific icon
    if system == "Windows":
        args.extend(["--icon", "icons/icon.ico"])  # Updated to match your file name
    elif system == "Darwin":  # macOS
        args.extend(["--icon", "icons/icon.icns"])  # Updated to match your file name
    else:
        print("Unsupported platform for icon setting. Building without icon.")

    # Add the --onefile option if desired (uncomment to use)
    # args.append("--onefile")

    # Clean previous builds
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")

    # Run PyInstaller
    print("Building PrimeSync...")
    PyInstaller.__main__.run(args)
    print(f"Build completed! Executable is in the 'dist' directory.")

if __name__ == "__main__":
    build_app()