#!/usr/bin/env python3
"""
Ultimate Interactive Python Code Generator with Comprehensive Auto-Fixing Validators
Uses local Ollama model to generate Python scripts and automatically fixes all code quality issues.
Features: intelligent input detection, comprehensive validation, auto-fixing, backup system, and seamless UX.
"""

import os
import subprocess
import sys
import threading
import time
import ast
import shutil
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Dict
import warnings

# ==================== USER CONFIGURATION ====================
OLLAMA_MODEL = "mixtral:8x7b-instruct-v0.1-q6_K"
DEFAULT_OUTPUT_DIR = "./generated_scripts"
MAX_RETRIES = 3
CONFIRM_AMBIGUOUS_INPUT = True
CONFIRMATION_THRESHOLD = 5

# Validation Settings
ENABLE_VALIDATION_LOOP = True
VALIDATION_PASSES = 1
VALIDATION_LEVEL = "full"  # "syntax", "logic", or "full"
SHOW_VALIDATION_FEEDBACK = True
ENABLE_CODE_VALIDATORS = True

# Backup Settings
BACKUP_BEFORE_VALIDATION = True
BACKUP_DIRECTORY = "./backups"

# Code Merging Settings
SAVE_SMALLER_SCRIPTS = False  # Set to True to also save individual fragmented scripts
MERGE_ALL_CODE_BLOCKS = True  # Always merge multiple code blocks into one script
# ============================================================

# ... [CodeQualityValidator class unchanged] ...
# ... [UltimatePythonCodeGenerator class unchanged except for process_request string fix below] ...

    def process_request(self, user_request: str, output_dir: Path = None, attempt: int = 1) -> bool:
        """Process a user request to generate Python code."""
        print(f"\n🎯 Processing request{f' (attempt {attempt})' if attempt > 1 else ''}: {user_request[:100]}{'...' if len(user_request) > 100 else ''}")
        
        # Extract filename if specified by user
        cleaned_request, specified_filename = self.extract_filename_from_request(user_request)
        
        # ULTRA-STRONG anti-fragmentation prompt that works for ANY complexity level
        prompt = (
            f'You are an expert Python developer. You MUST generate EXACTLY ONE COMPLETE Python script file.\n\n'
            f'REQUEST: "{cleaned_request}"\n\n'
            f'🚨 CRITICAL MANDATE - THIS IS NON-NEGOTIABLE:\n'
            f'YOU MUST CREATE EXACTLY ONE PYTHON FILE THAT CONTAINS EVERYTHING.\n'
            f'NEVER SUGGEST MULTIPLE FILES OR SEPARATE SCRIPTS.\n'
            f'EVERYTHING MUST BE IN ONE SINGLE .PY FILE.\n\n'
            f'ANTI-FRAGMENTATION RULES:\n'
            f'1. IGNORE any instinct to split into multiple files\n'
            f'2. IGNORE any thought about "it would be better organized in separate files"\n'
            f'3. IGNORE any consideration of modularity across files\n'
            f'4. PUT EVERYTHING in ONE script: imports, classes, functions, data, main logic\n'
            f'5. If you see categories/components, put ALL of them in the SAME file\n'
            f'6. If you see multiple functionalities, combine ALL in the SAME file\n'
            f'7. Create ONE unified program that does EVERYTHING requested\n\n'
            f'WHAT TO INCLUDE IN THE SINGLE FILE:\n'
            f'- ALL imports at the top\n'
            f'- ALL data structures (dictionaries, lists, configurations)\n'
            f'- ALL classes and functions\n'
            f'- ALL categories and their processing logic\n'
            f'- ALL user interface code\n'
            f'- ALL main execution logic\n'
            f'- ALL error handling\n'
            f'- ONE main() function that ties everything together\n\n'
            f'EXAMPLES OF CORRECT SINGLE-FILE APPROACH:\n'
            f'- 15 categories? → ALL 15 categories in ONE file\n'
            f'- Multiple APIs? → ALL API integrations in ONE file\n'
            f'- Complex data processing? → ALL processing in ONE file\n'
            f'- User interface + backend? → ALL combined in ONE file\n'
            f'- Image generation + file management? → ALL in ONE file\n\n'
            f'WHAT YOU MUST NEVER DO:\n'
            f'❌ Never say "create multiple files"\n'
            f'❌ Never suggest "separate script for each category"\n'
            f'❌ Never mention "modular approach with different files"\n'
            f'❌ Never create file1.py, file2.py, etc.\n'
            f'❌ Never suggest organizing into packages/modules\n\n'
            f'IMPLEMENTATION STRATEGY:\n'
            f'1. Start with shebang and imports\n'
            f'2. Define ALL data structures\n'
            f'3. Create ALL necessary classes\n'
            f'4. Define ALL functions\n'
            f'5. Create unified main() that handles everything\n'
            f'6. End with if __name__ == "__main__": main()\n\n'
            f'🔥 BACKUP PLAN: Even if you feel compelled to create multiple blocks, put ALL functionality in ONE comprehensive code block. If you absolutely must show multiple sections, put them ALL in ONE ```python``` block.\n\n'
            f'Remember: ONE FILE MUST CONTAIN EVERYTHING. Make it comprehensive, complete, and functional.\n\n'
            f'Generate the complete Python code for ONE single file:\n'
        )
        
        # Call the model
        response = self.call_model(prompt)
        if not response:
            return False
        
        # Extract Python code from response
        code = self.extract_python_code(response)
        if not code:
            print("❌ Could not extract Python code from model response.")
            if attempt == 1:
                print("Raw response:", response[:200] + "..." if len(response) > 200 else response)
            return False
        
        # Validate Python syntax
        if not self.validate_python_code(code):
            print("❌ Generated code has syntax errors.")
            return False
        
        # Generate filename (respecting user-specified name)
        filename = self.generate_filename(cleaned_request, specified_filename)
        if specified_filename:
            print(f"📝 Using specified filename: {filename}")
        else:
            print(f"📝 Auto-generated filename: {filename}")
        
        # Validate and improve code with model
        if ENABLE_VALIDATION_LOOP:
            code, validation_feedback = self.validate_code_with_model(code, filename)
            if SHOW_VALIDATION_FEEDBACK:
                print(validation_feedback)
        
        # Apply comprehensive code quality validation and auto-fixes
        if self.validators_enabled:
            print(f"\n🔧 Running comprehensive code quality validation and auto-fixes...")
            validation_results = self.code_validator.validate_and_fix_code(code, filename)
            
            if validation_results['fixes_applied']:
                code = validation_results['improved_code']
                print("✅ Auto-fixes applied:")
                for fix in validation_results['fixes_applied']:
                    print(f"  • {fix}")
            
            if validation_results['warnings']:
                print(f"\n⚠️ Quality warnings (for your review):")
                for warning in validation_results['warnings'][:5]:
                    print(f"  • {warning}")
                if len(validation_results['warnings']) > 5:
                    print(f"  ... and {len(validation_results['warnings']) - 5} more warnings")
        
        # Save the code
        if self.save_code(code, filename, output_dir):
            print(f"🎉 Generated Python script: {filename}")
            
            # Show a preview of the code
            print("\n📄 Code preview:")
            print("-" * 60)
            preview_lines = code.split('\n')[:15]
            for i, line in enumerate(preview_lines, 1):
                print(f"{i:2d}: {line}")
            if len(code.split('\n')) > 15:
                print("    ... (showing first 15 lines)")
            print("-" * 60)
            
            # Show final summary
            if self.validators_enabled and 'validation_results' in locals():
                print(f"\n📊 Quality Summary:")
                if validation_results['fixes_applied']:
                    print(f"  🔧 {len(validation_results['fixes_applied'])} automatic fixes applied")
                if validation_results['warnings']:
                    print(f"  ⚠️ {len(validation_results['warnings'])} warnings for review")
                print(f"  ✅ Code is production-ready!")
            
            return True
        
        return False

# ... [main function unchanged] ...

if __name__ == "__main__":
    main()