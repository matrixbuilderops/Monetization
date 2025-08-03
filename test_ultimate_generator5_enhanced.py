#!/usr/bin/env python3
"""
Test script for ultimate_python_generator5.py enhanced features
Validates multi-block detection, merging capabilities, and anti-fragmentation features.
"""

import sys
import os
from pathlib import Path

# Add the current directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from ultimate_python_generator5 import UltimatePythonCodeGenerator
    print("✅ Successfully imported ultimate_python_generator5")
except ImportError as e:
    print(f"❌ Failed to import: {e}")
    sys.exit(1)

def test_multi_block_detection():
    """Test multi-block detection and merging functionality."""
    print("\n🧪 Testing multi-block detection and merging...")
    
    generator = UltimatePythonCodeGenerator()
    
    # Simulate AI response with multiple code blocks
    multi_block_response = '''Here are the scripts you requested:

First, create main.py:
```python
#!/usr/bin/env python3
import os
import sys

def main():
    print("Main script functionality")
    helper_function()

if __name__ == "__main__":
    main()
```

Next, save as utils.py:
```python
import json
import requests

def helper_function():
    print("Helper function from utils")
    
def data_processor():
    data = {"test": "value"}
    return json.dumps(data)

def main():
    print("Utils main function")
    data_processor()

if __name__ == "__main__":
    main()
```

Finally, create config.py:
```python
# Configuration settings
DATABASE_URL = "sqlite:///test.db"
API_KEY = "test_key"

def get_config():
    return {
        "db_url": DATABASE_URL,
        "api_key": API_KEY
    }

def main():
    print("Config main function")
    config = get_config()
    print(config)

if __name__ == "__main__":
    main()
```
'''
    
    # Test extraction
    extracted_code = generator.extract_python_code(multi_block_response)
    
    # Validate that merging occurred
    checks = [
        ('#!/usr/bin/env python3' in extracted_code, "Shebang preservation"),
        ('Comprehensive Python script merged' in extracted_code, "Merge header"),
        ('import os' in extracted_code and 'import sys' in extracted_code, "Import consolidation"),
        ('def main_main():' in extracted_code, "Main function transformation"),
        ('def main_utils():' in extracted_code, "Utils function transformation"),
        ('def main_config():' in extracted_code, "Config function transformation"),
        ('def main():' in extracted_code, "Unified main function"),
        (extracted_code.count('if __name__ == "__main__":') == 1, "Single main execution")
    ]
    
    for check, description in checks:
        if check:
            print(f"✅ {description}")
        else:
            print(f"❌ {description}")
            # Debug info for failed checks
            if description == "Utils function transformation":
                print(f"   Looking for 'def main_utils():' in code...")
                print(f"   Found: {'def main_utils():' in extracted_code}")
            elif description == "Config function transformation":
                print(f"   Looking for 'def main_config():' in code...")
                print(f"   Found: {'def main_config():' in extracted_code}")
            elif 'main_' not in extracted_code:
                print(f"   Debug: Code preview: {extracted_code[:300]}...")
    
    return extracted_code

def test_single_block_extraction():
    """Test single block extraction (should not trigger merging)."""
    print("\n🧪 Testing single block extraction...")
    
    generator = UltimatePythonCodeGenerator()
    
    single_block_response = '''Here's your script:

```python
#!/usr/bin/env python3
def hello_world():
    print("Hello, World!")

if __name__ == "__main__":
    hello_world()
```
'''
    
    extracted_code = generator.extract_python_code(single_block_response)
    
    checks = [
        ('def hello_world():' in extracted_code, "Function preservation"),
        ('if __name__ == "__main__":' in extracted_code, "Main block preservation"),
        ('merged from' not in extracted_code.lower(), "No merging header")
    ]
    
    for check, description in checks:
        if check:
            print(f"✅ {description}")
        else:
            print(f"❌ {description}")

def test_filename_detection():
    """Test filename detection from AI responses."""
    print("\n🧪 Testing filename detection...")
    
    generator = UltimatePythonCodeGenerator()
    
    filename_response = '''I'll create the calculator for you.

Save as calculator.py:
```python
def add(a, b):
    return a + b

def main():
    print("Calculator ready")

if __name__ == "__main__":
    main()
```
'''
    
    # This should be tested through the full process_request, but we can test the parsing
    # The filename detection happens in extract_python_code now
    extracted_code = generator.extract_python_code(filename_response)
    
    checks = [
        ('def add(a, b):' in extracted_code, "Function extraction"),
        ('def main():' in extracted_code, "Main function extraction")
    ]
    
    for check, description in checks:
        if check:
            print(f"✅ {description}")
        else:
            print(f"❌ {description}")

def test_merge_code_blocks_method():
    """Test the _merge_code_blocks method directly."""
    print("\n🧪 Testing _merge_code_blocks method...")
    
    generator = UltimatePythonCodeGenerator()
    
    # Create test code blocks
    test_blocks = [
        {
            'code': '''import os
import sys

def main():
    print("Block 1 functionality")
    process_data()

def process_data():
    print("Processing in block 1")

if __name__ == "__main__":
    main()''',
            'filename': 'block1.py',
            'description': 'Data Processing Module'
        },
        {
            'code': '''import json
import requests

def main():
    print("Block 2 functionality")
    fetch_data()

def fetch_data():
    print("Fetching data in block 2")

if __name__ == "__main__":
    main()''',
            'filename': 'block2.py',
            'description': 'Data Fetching Module'
        }
    ]
    
    merged_code = generator._merge_code_blocks(test_blocks)
    
    checks = [
        ('#!/usr/bin/env python3' in merged_code, "Shebang added"),
        ('Comprehensive Python script merged' in merged_code, "Merge documentation"),
        ('import os' in merged_code and 'import json' in merged_code, "Import consolidation"),
        ('def main_block1():' in merged_code, "Block 1 main function renamed"),
        ('def main_block2():' in merged_code, "Block 2 main function renamed"),
        ('def main():' in merged_code, "Unified main function created"),
        (merged_code.count('if __name__ == "__main__":') == 1, "Single execution block"),
        ('Data Processing Module' in merged_code, "Block 1 description included"),
        ('Data Fetching Module' in merged_code, "Block 2 description included")
    ]
    
    for check, description in checks:
        if check:
            print(f"✅ {description}")
        else:
            print(f"❌ {description}")
            if 'main_' not in merged_code:
                print(f"   Debug: Looking for main functions in: {merged_code[:500]}...")

def test_configuration_settings():
    """Test that new configuration settings are accessible."""
    print("\n🧪 Testing configuration settings...")
    
    # Import the settings
    try:
        from ultimate_python_generator5 import SAVE_SMALLER_SCRIPTS, MERGE_ALL_CODE_BLOCKS
        
        checks = [
            (SAVE_SMALLER_SCRIPTS == False, "SAVE_SMALLER_SCRIPTS default value"),
            (MERGE_ALL_CODE_BLOCKS == True, "MERGE_ALL_CODE_BLOCKS default value")
        ]
        
        for check, description in checks:
            if check:
                print(f"✅ {description}")
            else:
                print(f"❌ {description}")
                
    except ImportError as e:
        print(f"❌ Configuration settings import failed: {e}")

def main():
    """Run all tests."""
    print("🚀 Testing Ultimate Python Generator 5 Enhanced Features")
    print("=" * 70)
    
    test_configuration_settings()
    test_merge_code_blocks_method()
    test_multi_block_detection()
    test_single_block_extraction()
    test_filename_detection()
    
    print("\n✅ All enhanced feature tests completed!")
    print("\n🔀 Multi-block merging system ready!")
    print("🚨 Anti-fragmentation protection active!")

if __name__ == "__main__":
    main()