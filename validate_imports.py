#!/usr/bin/env python3
"""
Validate that Python imports match Cargo.toml [lib] configuration
"""

import re
import sys
import subprocess
import os

def get_lib_name_from_cargo():
    """Extract [lib] name from Cargo.toml"""
    try:
        with open('src/Cargo.toml', 'r') as f:
            content = f.read()
        
        # Find [lib] section and extract name
        lib_match = re.search(r'\[lib\].*?name\s*=\s*"([^"]+)"', content, re.DOTALL)
        if lib_match:
            return lib_match.group(1)
        else:
            print("❌ No [lib] section found in src/Cargo.toml")
            return None
    except FileNotFoundError:
        print("❌ src/Cargo.toml not found")
        return None

def check_python_imports(lib_name):
    """Check that Python files use correct import"""
    files_to_check = ['src/main.py', 'app/main.py']
    all_good = True
    
    for filename in files_to_check:
        try:
            with open(filename, 'r') as f:
                content = f.read()
            
            # Look for import statements
            import_pattern = f'import {lib_name}'
            if import_pattern in content:
                print(f"✅ {filename}: Found correct import: {import_pattern}")
            else:
                print(f"❌ {filename}: No import statement found for {lib_name}")
                all_good = False
        except FileNotFoundError:
            print(f"❌ {filename} not found")
            all_good = False
    
    return all_good

def test_import(lib_name):
    """Test that import actually works"""
    try:
        # Add refinery_core_src to path for testing
        sys.path.insert(0, './refinery_core_src')
        result = subprocess.run([
            sys.executable, '-c', f'import {lib_name}; print("Import successful")'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(f"✅ Import test successful: {lib_name}")
            return True
        else:
            print(f"❌ Import test failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"❌ Import test timed out")
        return False
    except Exception as e:
        print(f"❌ Import test error: {e}")
        return False

def main():
    print("🔍 Validating Rust-Python module imports...")
    
    # Get lib name from Cargo.toml
    lib_name = get_lib_name_from_cargo()
    if not lib_name:
        sys.exit(1)
    
    print(f"📦 Found lib name: {lib_name}")
    
    # Check Python imports
    if not check_python_imports(lib_name):
        sys.exit(1)
    
    # Test actual import
    if not test_import(lib_name):
        sys.exit(1)
    
    print("✅ All import validations passed!")
    sys.exit(0)

if __name__ == "__main__":
    main()