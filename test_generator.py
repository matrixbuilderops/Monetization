#!/usr/bin/env python3
"""
Test script for the Python Code Generator
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from python_code_generator import PythonCodeGenerator

def test_generator():
    """Test the code generator with a simple request."""
    print("Testing Python Code Generator...")
    
    generator = PythonCodeGenerator()
    
    # Test without actually calling the model (since Ollama might not be available)
    print(f"Output directory: {generator.output_dir}")
    
    # Test filename generation
    test_requests = [
        "make a hello world program",
        "create a calculator",
        "generate a file organizer script"
    ]
    
    for request in test_requests:
        filename = generator.generate_filename(request)
        print(f"Request: '{request}' -> Filename: '{filename}'")
    
    # Test code extraction
    sample_response = """Here's a simple hello world program:

```python
print("Hello, World!")
print("This is a generated script")
```

This code will print a greeting message."""
    
    extracted_code = generator.extract_python_code(sample_response)
    print(f"\nExtracted code:\n{extracted_code}")
    
    # Test saving functionality
    test_code = 'print("Hello, World!")\nprint("Test successful!")'
    success = generator.save_code(test_code, "test_hello_world.py")
    print(f"Save test: {'✓ Success' if success else '❌ Failed'}")
    
    return True

if __name__ == "__main__":
    test_generator()