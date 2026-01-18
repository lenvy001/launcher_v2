#!/usr/bin/env python3
"""
Script de execução do Launcher V2
Use: python run.py [web|cli]
"""

import sys
import os
import subprocess

# Mudar para pasta src
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
os.chdir(SRC_DIR)

print("=" * 40)
print("  LAUNCHER V2 - App Manager")
print("=" * 40)
print()

if len(sys.argv) > 1:
    choice = sys.argv[1].lower()
else:
    print("[1] Web Interface (Flask)")
    print("[2] CLI Menu")
    print("[0] Exit")
    print()
    choice = input("Choose: ").strip()

if choice in ["1", "web"]:
    print()
    print("🌐 Starting Flask server...")
    print("📍 Access: http://localhost:5000")
    print()
    subprocess.run([sys.executable, "serve.py"])

elif choice in ["2", "cli"]:
    print()
    print("💻 Starting CLI Menu...")
    print()
    subprocess.run([sys.executable, "main.py"])

elif choice in ["0", "exit"]:
    print("Goodbye!")
    sys.exit(0)

else:
    print("❌ Invalid choice")
    sys.exit(1)
