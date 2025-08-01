#!/usr/bin/env python3
"""
Test suite to verify the code generator is truly command-agnostic and makes no assumptions.
This addresses the core issue where the tool was making unwanted assumptions about user intent.
"""

import unittest
from unittest.mock import patch, MagicMock
from python_code_generator_enhanced import EnhancedPythonCodeGenerator


class TestCommandAgnosticBehavior(unittest.TestCase):
    """Test that the generator doesn't make assumptions about user intent."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = EnhancedPythonCodeGenerator()
    
    def test_no_domain_specific_assumptions_in_detection(self):
        """Test that detect_data_structure_type doesn't make domain assumptions."""
        test_cases = [
            ("CATS = {'productivity': ['focus']}", "dictionary structure"),
            ("cats_data = ['big cats', 'small cats']", "list structure"),  # Fixed: should detect as list
            ("productivity_data = {...}", "dictionary structure"),  # Fixed: should detect as dict
            ("wellness_categories = []", "list structure"),  # Fixed: should detect as list
            ("stable_diffusion_prompt = 'test'", "code structure"),
            ("{'productivity': ['burnout']}", "dictionary structure"),
            ("[1, 2, 3]", "list structure"),
        ]
        
        for input_text, expected_type in test_cases:
            with self.subTest(input_text=input_text):
                detected_type = self.generator.detect_data_structure_type(input_text)
                self.assertEqual(detected_type, expected_type, 
                    f"Should detect as generic '{expected_type}', not domain-specific")
    
    def test_no_special_prompts_for_any_input(self):
        """Test that all inputs use the same generic prompt structure."""
        test_inputs = [
            "make a hello world program",
            "CATS = {'productivity': ['focus'], 'wellness': ['meditation']}",
            "create a stable diffusion image generator",
            "build an affirmation script",
            "generate wellness content",
            "productivity_data = ['task1', 'task2']",
        ]
        
        # Mock the call_model method to capture the prompts
        with patch.object(self.generator, 'call_model') as mock_call:
            mock_call.return_value = "print('hello world')"
            
            for test_input in test_inputs:
                with self.subTest(input_text=test_input[:30]):
                    # Mock other methods to avoid file operations
                    with patch.object(self.generator, 'extract_python_code', return_value="print('test')"), \
                         patch.object(self.generator, 'save_code', return_value=True), \
                         patch('builtins.print'):  # Suppress output
                        
                        self.generator.process_request(test_input)
                        
                        # Verify the prompt structure is generic
                        call_args = mock_call.call_args[0][0]  # Get the prompt
                        
                        # Should contain the generic prompt structure
                        self.assertIn('Generate a complete Python script based on this request:', call_args)
                        self.assertIn('Please provide only the Python code without any explanations', call_args)
                        self.assertIn('Make sure the code is complete, well-commented, and ready to run', call_args)
                        
                        # Should NOT contain domain-specific assumptions about what to do with the data
                        # (but the user's actual input words may appear in the prompt)
                        domain_assumptions = [
                            'for image generation', 'as intended', 'categories and subcategories',
                            'comprehensive script that:', 'uses the data structure as intended'
                        ]
                        
                        for assumption in domain_assumptions:
                            self.assertNotIn(assumption.lower(), call_args.lower(),
                                f"Should not assume '{assumption}' for input: {test_input}")
                        
                        # Should contain the user's actual request
                        self.assertIn(test_input, call_args)
    
    def test_cats_dictionary_treated_generically(self):
        """Test that CATS dictionary is treated like any other data structure."""
        cats_input = '''CATS = {
    "productivity": ["imposter_syndrome", "burnout"],
    "confidence": ["self_doubt", "public_speaking"]
}

Create a simple data processor for this dictionary.'''
        
        with patch.object(self.generator, 'call_model') as mock_call:
            mock_call.return_value = "print('data processor')"
            
            with patch.object(self.generator, 'extract_python_code', return_value="print('test')"), \
                 patch.object(self.generator, 'save_code', return_value=True), \
                 patch('builtins.print'):
                
                self.generator.process_request(cats_input)
                
                # Get the actual prompt sent to the model
                prompt = mock_call.call_args[0][0]
                
                # Should use generic prompt, not special CATS handling
                self.assertIn('Generate a complete Python script based on this request:', prompt)
                
                # Should NOT contain the old special handling text
                self.assertNotIn('Create a comprehensive script that:', prompt)
                self.assertNotIn('Uses the data structure as intended', prompt)
                self.assertNotIn('image generation', prompt.lower())
                self.assertNotIn('ONE complete script that handles ALL the data', prompt)
    
    def test_no_assumptions_about_user_intent(self):
        """Test that the tool doesn't assume what users want to do with their data."""
        ambiguous_inputs = [
            "process this data: {'cats': ['big', 'small']}",
            "use this dictionary: {'wellness': ['meditation']}",
            "handle this list: ['productivity', 'focus', 'burnout']",
        ]
        
        for ambiguous_input in ambiguous_inputs:
            with self.subTest(input_text=ambiguous_input):
                with patch.object(self.generator, 'call_model') as mock_call:
                    mock_call.return_value = "print('generic script')"
                    
                    with patch.object(self.generator, 'extract_python_code', return_value="print('test')"), \
                         patch.object(self.generator, 'save_code', return_value=True), \
                         patch('builtins.print'):
                        
                        self.generator.process_request(ambiguous_input)
                        
                        prompt = mock_call.call_args[0][0]
                        
                        # Should only ask for what the user explicitly requested
                        self.assertIn(ambiguous_input, prompt)
                        
                        # Should NOT invent assumptions about what to do
                        assumption_phrases = [
                            'image generation', 'affirmations', 'wellness content',
                            'stable diffusion', 'big cats', 'categories and subcategories',
                            'as intended', 'for image/content generation'
                        ]
                        
                        for phrase in assumption_phrases:
                            self.assertNotIn(phrase.lower(), prompt.lower(),
                                f"Should not assume '{phrase}' for input: {ambiguous_input}")


class TestFlexibilityRequirements(unittest.TestCase):
    """Test that the tool meets the flexibility requirements from the issue."""
    
    def setUp(self):
        self.generator = EnhancedPythonCodeGenerator()
    
    def test_accepts_any_command_or_code_block(self):
        """Test that the tool accepts any type of input without forcing workflows."""
        diverse_inputs = [
            "print('hello world')",
            "def calculate_tax(income): return income * 0.25",
            "import requests\nresponse = requests.get('https://api.example.com')",
            "CREATE TABLE users (id INTEGER, name TEXT);",
            "docker run --rm -it python:3.9",
            "npm install express mongoose",
            "SELECT * FROM products WHERE price > 100;",
            "curl -X POST https://api.example.com/data",
        ]
        
        for diverse_input in diverse_inputs:
            with self.subTest(input_text=diverse_input[:30]):
                # Should process immediately without forcing it into a specific workflow
                result = self.generator.handle_multi_line_input(diverse_input)
                
                if self.generator.is_complete_structure(diverse_input):
                    self.assertEqual(result, diverse_input, 
                        "Should return input as-is for processing")
                    self.assertFalse(self.generator.multi_line_mode, 
                        "Should not force multi-line mode for complete input")
    
    def test_no_guessing_or_inventing_jobs(self):
        """Test that the tool doesn't invent jobs or guess user intent."""
        # These inputs should be processed exactly as requested, not transformed
        exact_inputs = [
            ("make a calculator", "should build exactly what's requested"),
            ("list files in directory", "should not assume file operations beyond listing"),
            ("connect to database", "should not assume specific database type"),
            ("process user input", "should not assume specific processing type"),
        ]
        
        for user_input, expectation in exact_inputs:
            with self.subTest(input_text=user_input):
                with patch.object(self.generator, 'call_model') as mock_call:
                    mock_call.return_value = f"# Script for: {user_input}"
                    
                    with patch.object(self.generator, 'extract_python_code', return_value="print('test')"), \
                         patch.object(self.generator, 'save_code', return_value=True), \
                         patch('builtins.print'):
                        
                        self.generator.process_request(user_input)
                        
                        prompt = mock_call.call_args[0][0]
                        
                        # Should ask for exactly what user requested
                        self.assertIn(user_input, prompt)
                        
                        # Should not add extra assumptions or requirements
                        extra_assumptions = [
                            'image generation', 'stable diffusion', 'wellness',
                            'affirmations', 'categories', 'subcategories'
                        ]
                        
                        for assumption in extra_assumptions:
                            self.assertNotIn(assumption.lower(), prompt.lower(),
                                f"Should not add assumption '{assumption}' to '{user_input}'")


if __name__ == '__main__':
    unittest.main(verbosity=2)