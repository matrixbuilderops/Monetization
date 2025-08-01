#!/usr/bin/env python3
"""
Test suite for UX fixes in the enhanced Python code generator.
These tests verify that the multi-line input issues identified in the terminal transcript are resolved.
"""

import unittest
from python_code_generator_enhanced import EnhancedPythonCodeGenerator


class TestEnhancedGeneratorUXFixes(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = EnhancedPythonCodeGenerator()
    
    def tearDown(self):
        """Reset generator state after each test."""
        self.generator.multi_line_mode = False
        self.generator.current_input = ""
    
    def test_simple_request_processed_immediately(self):
        """Test that simple requests are processed immediately."""
        simple_requests = [
            "make a hello world program",
            "create a file organizer",
            "generate a web scraper"
        ]
        
        for request in simple_requests:
            with self.subTest(request=request):
                result = self.generator.handle_multi_line_input(request)
                self.assertEqual(result, request, "Simple request should be processed immediately")
                self.assertFalse(self.generator.multi_line_mode, "Should not be in multi-line mode")
    
    def test_complete_cats_dictionary_processed_immediately(self):
        """Test that complete CATS dictionary is processed immediately (main fix)."""
        cats_dict = '''CATS = {
    "productivity": ["imposter_syndrome", "burnout", "workspace_focus"],
    "confidence": ["self_doubt", "public_speaking", "decision_making"],
    "gratitude": ["daily_practice", "gratitude_after_loss", "gratitude_for_body"],
    "healing": ["breakup", "trauma", "loss"],
    "focus": ["ADHD", "study_block", "digital_distraction"],
    "creativity": ["artist_block", "new_idea", "creative_confidence"],
    "happiness": ["moment_to_moment", "joyful_small_things", "inner_child"],
    "resilience": ["setback_recovery", "stress_response", "mental_toughness"],
    "self_love": ["body_image", "self_acceptance", "personal_growth"],
    "stress_relief": ["deep_breathing", "tension_release", "deadline_pressure"],
    "success": ["goals_alignment", "career_vision", "achievement_mindset"],
    "anxiety_relief": ["panic_attack", "social_anxiety", "future_worry"],
    "mindfulness": ["present_awareness", "grounding", "calm_presence"],
    "motivation": ["morning_boost", "daily_grind", "persistence"],
    "relationships": ["toxic_family", "romantic_conflict", "friendship_loss"]
}'''
        
        result = self.generator.handle_multi_line_input(cats_dict)
        self.assertEqual(result, cats_dict, "Complete CATS dictionary should be processed immediately")
        self.assertFalse(self.generator.multi_line_mode, "Should not be in multi-line mode after complete input")
    
    def test_complex_multiline_request_processed_immediately(self):
        """Test that complex multi-line requests are processed immediately."""
        complex_request = '''write generate_sd_images.py: Build a Python script that uses the Hugging Face diffusers library with the model 'stabilityai/stable-diffusion-2-1-base' to generate six images per subcategory from the following CATS dictionary:

CATS = {
    "productivity": ["imposter_syndrome", "burnout", "workspace_focus"],
    "confidence": ["self_doubt", "public_speaking", "decision_making"]
}

Use only CPU-compatible setup. The default image resolution must be 2550x3300 pixels.'''
        
        result = self.generator.handle_multi_line_input(complex_request)
        self.assertEqual(result, complex_request, "Complex multi-line request should be processed immediately")
        self.assertFalse(self.generator.multi_line_mode, "Should not be in multi-line mode after complete input")
    
    def test_incomplete_structure_triggers_multiline_mode(self):
        """Test that truly incomplete structures trigger multi-line mode."""
        incomplete_cases = [
            "CATS = {",
            "data = [",
            "config = {\n    'key':",
            '"unclosed string'
        ]
        
        for incomplete in incomplete_cases:
            with self.subTest(incomplete=incomplete):
                self.tearDown()  # Reset state
                result = self.generator.handle_multi_line_input(incomplete)
                self.assertIsNone(result, f"Incomplete structure should return None: {incomplete}")
                self.assertTrue(self.generator.multi_line_mode, f"Should be in multi-line mode: {incomplete}")
    
    def test_auto_completion_from_multiline_mode(self):
        """Test that completing incomplete input auto-exits multi-line mode."""
        # Start with incomplete input
        incomplete = "CATS = {"
        result = self.generator.handle_multi_line_input(incomplete)
        self.assertIsNone(result)
        self.assertTrue(self.generator.multi_line_mode)
        
        # Complete the input
        completion = '    "test": ["item1", "item2"]\n}'
        result = self.generator.handle_multi_line_input(completion)
        
        self.assertIsNotNone(result, "Completed input should be returned")
        self.assertFalse(self.generator.multi_line_mode, "Should auto-exit multi-line mode")
        self.assertIn("CATS = {", result, "Result should contain original input")
        self.assertIn("test", result, "Result should contain completion")
    
    def test_complete_structure_detection(self):
        """Test the is_complete_structure method."""
        complete_cases = [
            "hello world",
            '{"key": "value"}',
            "[1, 2, 3]",
            "x = [1, 2, 3]",
            '''CATS = {
    "productivity": ["test"],
    "confidence": ["test2"]
}'''
        ]
        
        for case in complete_cases:
            with self.subTest(case=case):
                self.assertTrue(self.generator.is_complete_structure(case), 
                              f"Should detect as complete: {case[:50]}")
    
    def test_incomplete_structure_detection(self):
        """Test the is_incomplete_structure method."""
        incomplete_cases = [
            "CATS = {",
            "data = [",
            "{'key':",
            '"unclosed string',
            "x = {\n    'item':"
        ]
        
        for case in incomplete_cases:
            with self.subTest(case=case):
                self.assertTrue(self.generator.is_incomplete_structure(case), 
                              f"Should detect as incomplete: {case}")
    
    def test_manual_end_still_works(self):
        """Test that manual END/CANCEL commands still work."""
        # Enter multi-line mode
        incomplete = "CATS = {"
        result = self.generator.handle_multi_line_input(incomplete)
        self.assertIsNone(result)
        self.assertTrue(self.generator.multi_line_mode)
        
        # Test END command
        result = self.generator.handle_multi_line_input("END")
        self.assertEqual(result, incomplete, "END should return current input")
        self.assertFalse(self.generator.multi_line_mode, "END should exit multi-line mode")
        
        # Reset and test CANCEL
        self.generator.multi_line_mode = True
        self.generator.current_input = "test"
        result = self.generator.handle_multi_line_input("CANCEL")
        self.assertIsNone(result, "CANCEL should return None")
        self.assertFalse(self.generator.multi_line_mode, "CANCEL should exit multi-line mode")
    
    def test_balanced_brackets_detection(self):
        """Test that balanced brackets are detected correctly."""
        balanced_cases = [
            "{}",
            "[]",
            "()",
            "{'a': [1, 2], 'b': (3, 4)}",
            '''CATS = {
    "test": ["a", "b"],
    "test2": {"nested": "value"}
}'''
        ]
        
        for case in balanced_cases:
            with self.subTest(case=case):
                self.assertTrue(self.generator.is_complete_structure(case), 
                              f"Balanced structure should be complete: {case[:50]}")


class TestRegressionPrevention(unittest.TestCase):
    """Tests to prevent regression of the original terminal transcript issues."""
    
    def setUp(self):
        self.generator = EnhancedPythonCodeGenerator()
    
    def test_cats_dictionary_single_processing(self):
        """Regression test: Ensure CATS dictionary is processed as single unit, not broken up."""
        cats_input = '''CATS = {
    "productivity": ["imposter_syndrome", "burnout"],
    "confidence": ["self_doubt", "public_speaking"]
}'''
        
        # This should be processed immediately, not broken into pieces
        result = self.generator.handle_multi_line_input(cats_input)
        
        # Should get the complete input back immediately
        self.assertEqual(result, cats_input)
        self.assertFalse(self.generator.multi_line_mode)
        
        # Should NOT require additional processing steps
        # (In the original bug, each line would be processed separately)
    
    def test_no_forced_end_cancel_for_complete_input(self):
        """Regression test: Complete input should never require END/CANCEL."""
        complete_inputs = [
            "simple request",
            '{"complete": "dict"}',
            "[1, 2, 3]",
            '''CATS = {
    "test": ["complete", "dictionary"],
    "more": ["data", "here"]
}'''
        ]
        
        for complete_input in complete_inputs:
            with self.subTest(input=complete_input[:30]):
                result = self.generator.handle_multi_line_input(complete_input)
                self.assertIsNotNone(result, "Complete input should be processed immediately")
                self.assertEqual(result, complete_input, "Should get back the complete input")
                self.assertFalse(self.generator.multi_line_mode, "Should not force multi-line mode")


if __name__ == '__main__':
    unittest.main(verbosity=2)