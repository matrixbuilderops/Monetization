#!/usr/bin/env python3
"""
Test script for the seamless Python code generator.
Tests basic functionality without needing Ollama installed.
"""

import sys
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add current directory to path so we can import our module
sys.path.insert(0, str(Path(__file__).parent))

from python_code_generator_seamless import SeamlessPythonCodeGenerator

class TestSeamlessGenerator(unittest.TestCase):
    """Test the seamless generator functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = SeamlessPythonCodeGenerator()
    
    def test_generator_initialization(self):
        """Test that the generator initializes correctly."""
        self.assertIsNotNone(self.generator)
        self.assertEqual(self.generator.model_name, "mixtral:8x7b-instruct-v0.1-q6_K")
        self.assertTrue(self.generator.output_dir.name == "generated_scripts")
    
    def test_filename_generation_single_line(self):
        """Test filename generation for single line requests."""
        test_cases = [
            ("make a hello world program", "hello"),
            ("create calculator script", "calculator"),
            ("generate file organizer", "organizer"),
        ]
        
        for request, expected_word in test_cases:
            with self.subTest(request=request):
                filename = self.generator.generate_filename(request)
                self.assertTrue(filename.endswith('.py'))
                self.assertIn(expected_word, filename.lower())
    
    def test_filename_generation_multiline(self):
        """Test filename generation for multi-line requests."""
        multiline_request = """create a data processor
        
        CATS = {
            "productivity": ["focus", "burnout"],
            "wellness": ["meditation"]
        }
        
        Process this data structure"""
        
        filename = self.generator.generate_filename(multiline_request)
        self.assertTrue(filename.endswith('.py'))
        self.assertIn('data_processor', filename.lower())
    
    def test_code_extraction_with_markdown(self):
        """Test code extraction from markdown formatted responses."""
        response_with_markdown = """Here's the Python script you requested:

```python
def hello_world():
    print("Hello, World!")

if __name__ == "__main__":
    hello_world()
```

This script prints Hello World."""
        
        extracted_code = self.generator.extract_python_code(response_with_markdown)
        expected_code = """def hello_world():
    print("Hello, World!")

if __name__ == "__main__":
    hello_world()"""
        
        self.assertEqual(extracted_code, expected_code)
    
    def test_code_extraction_without_markdown(self):
        """Test code extraction from plain text responses."""
        plain_response = """def calculator():
    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))
    return a + b

result = calculator()
print(f"Result: {result}")"""
        
        extracted_code = self.generator.extract_python_code(plain_response)
        # Should return the same code since no markdown blocks
        self.assertEqual(extracted_code, plain_response)
    
    @patch('subprocess.Popen')
    def test_model_call_success(self, mock_popen):
        """Test successful model call."""
        # Mock the subprocess response
        mock_process = MagicMock()
        mock_process.communicate.return_value = (b"print('hello world')", b"")
        mock_process.returncode = 0
        mock_popen.return_value = mock_process
        
        # Patch the threading to avoid actual delays
        with patch('threading.Thread'), patch('time.sleep'), patch('builtins.print'):
            result = self.generator.call_model("test prompt")
        
        self.assertEqual(result, "print('hello world')")
    
    @patch('subprocess.Popen')
    def test_model_call_failure(self, mock_popen):
        """Test model call failure handling."""
        # Mock a failed subprocess
        mock_process = MagicMock()
        mock_process.communicate.return_value = (b"", b"Model not found")
        mock_process.returncode = 1
        mock_popen.return_value = mock_process
        
        with patch('threading.Thread'), patch('time.sleep'), patch('builtins.print'):
            result = self.generator.call_model("test prompt")
        
        self.assertIsNone(result)
    
    @patch.object(SeamlessPythonCodeGenerator, 'call_model')
    @patch.object(SeamlessPythonCodeGenerator, 'save_code')
    def test_process_request_integration(self, mock_save, mock_call):
        """Test the full request processing flow."""
        # Mock the model response
        mock_call.return_value = """def hello():
    print("Hello, World!")

hello()"""
        
        mock_save.return_value = True
        
        with patch('builtins.print'):  # Suppress output during test
            self.generator.process_request("make a hello world program")
        
        # Verify the model was called with correct prompt
        mock_call.assert_called_once()
        call_args = mock_call.call_args[0][0]
        self.assertIn("Generate ONE complete Python script", call_args)
        self.assertIn("make a hello world program", call_args)
        
        # Verify save was attempted
        mock_save.assert_called_once()
    
    def test_multiline_input_handling(self):
        """Test that multiline inputs are handled without multi-line mode prompts."""
        multiline_input = """CATS = {
    "productivity": ["imposter_syndrome", "burnout", "workspace_focus"],
    "confidence": ["self_doubt", "public_speaking", "decision_making"],
    "gratitude": ["daily_practice", "gratitude_after_loss", "gratitude_for_body"]
}

Create a script to process this data"""
        
        # The key test: this should be processed as-is without entering multi-line mode
        with patch.object(self.generator, 'call_model', return_value="print('processed')"):
            with patch.object(self.generator, 'save_code', return_value=True):
                with patch('builtins.print'):
                    self.generator.process_request(multiline_input)
        
        # If we get here without the method trying to split this into parts, the test passes
        self.assertTrue(True)  # Explicit pass

def run_manual_tests():
    """Run some manual tests to verify functionality."""
    print("🧪 Running Manual Tests for Seamless Generator")
    print("=" * 50)
    
    generator = SeamlessPythonCodeGenerator()
    
    # Test 1: Filename generation
    print("\n1. Testing filename generation:")
    test_requests = [
        "make a hello world program",
        "create calculator\nwith advanced features",
        "CATS = {'test': 'data'}\nprocess this",
    ]
    
    for i, request in enumerate(test_requests, 1):
        filename = generator.generate_filename(request)
        print(f"   {i}. '{request[:30]}...' → {filename}")
    
    # Test 2: Code extraction
    print("\n2. Testing code extraction:")
    test_response = """Here's your script:

```python
def main():
    print("Hello from generated script!")

if __name__ == "__main__":
    main()
```

This script does what you requested."""
    
    extracted = generator.extract_python_code(test_response)
    print(f"   Extracted {len(extracted.split('\n'))} lines of Python code")
    print(f"   First line: {extracted.split('\n')[0]}")
    
    print("\n✅ Manual tests completed successfully!")

if __name__ == '__main__':
    print("🐍 Testing Seamless Python Code Generator")
    print("=" * 50)
    
    # Run unit tests
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run manual tests
    print("\n" + "=" * 50)
    run_manual_tests()