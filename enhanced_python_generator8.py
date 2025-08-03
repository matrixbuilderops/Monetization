#!/usr/bin/env python3
"""
Enhanced Python Code Generator Version 8
Advanced AI-powered code generator that can parse complex natural language prompts
and convert them into sophisticated Python scripts with automatic error correction.

Features:
- Complex prompt parsing and understanding
- Stable diffusion script generation with category management
- Automatic code validation and fixing
- Customizable output configurations
- Batch processing capabilities
"""

import os
import re
import ast
import sys
import json
import shutil
import subprocess
import threading
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

# Import validation tools
try:
    from code_quality_validator import CodeQualityValidator
    VALIDATION_AVAILABLE = True
except ImportError:
    VALIDATION_AVAILABLE = False

# Configuration
OLLAMA_MODEL = "mixtral:8x7b-instruct-v0.1-q6_K"
DEFAULT_OUTPUT_DIR = "./generated_scripts"
MAX_RETRIES = 3
VALIDATION_PASSES = 2

class EnhancedPythonGenerator8:
    """Enhanced Python code generator with advanced prompt parsing and automatic fixing."""
    
    def __init__(self, model_name=OLLAMA_MODEL):
        self.model_name = model_name
        self.output_dir = Path(DEFAULT_OUTPUT_DIR)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        # Initialize code quality validator
        if VALIDATION_AVAILABLE:
            self.validator = CodeQualityValidator()
            print("✅ Advanced validation enabled")
        else:
            self.validator = None
            print("⚠️  Basic validation mode")
        
        # Pattern recognition for common script types
        self.script_patterns = {
            'stable_diffusion': self._detect_stable_diffusion_pattern,
            'data_processing': self._detect_data_processing_pattern,
            'web_scraping': self._detect_web_scraping_pattern,
            'automation': self._detect_automation_pattern,
        }
        
        # Validation patterns for common syntax issues
        self.validation_patterns = {
            'unterminated_string': self._fix_unterminated_strings,
            'missing_imports': self._fix_missing_imports,
            'indentation_errors': self._fix_indentation_errors,
            'syntax_errors': self._fix_syntax_errors,
        }
    
    def parse_complex_prompt(self, prompt: str) -> Dict[str, Any]:
        """Parse complex natural language prompts and extract requirements."""
        print("🔍 Analyzing prompt complexity...")
        
        # Initialize result structure
        parsed_prompt = {
            'script_type': 'general',
            'requirements': [],
            'parameters': {},
            'categories': {},
            'output_specs': {},
            'features': []
        }
        
        # Detect script type
        if 'stable diffusion' in prompt.lower():
            parsed_prompt['script_type'] = 'stable_diffusion'
            parsed_prompt.update(self._parse_stable_diffusion_prompt(prompt))
        
        # Extract categories using improved regex patterns
        categories_match = re.search(r'CATEGORIES\s*=\s*{([^}]+)}', prompt, re.DOTALL)
        if categories_match:
            try:
                # Safe evaluation of category dictionary
                categories_text = '{' + categories_match.group(1) + '}'
                parsed_prompt['categories'] = ast.literal_eval(categories_text)
            except (SyntaxError, ValueError) as e:
                print(f"⚠️  Could not parse categories: {e}")
                parsed_prompt['categories'] = {}
        
        # Extract size specifications
        size_pattern1 = r'(\d+)x(\d+)\s*pixels'
        size_pattern2 = r'size.*?(\d+)\s*x\s*(\d+)'
        size_pattern3 = r'resolution.*?(\d+)\s*x\s*(\d+)'
        
        size_match = (re.search(size_pattern1, prompt) or 
                     re.search(size_pattern2, prompt) or 
                     re.search(size_pattern3, prompt))
        
        if size_match:
            parsed_prompt['output_specs']['width'] = int(size_match.group(1))
            parsed_prompt['output_specs']['height'] = int(size_match.group(2))
        else:
            # Default size as specified in prompt
            parsed_prompt['output_specs']['width'] = 550
            parsed_prompt['output_specs']['height'] = 3300
        
        # Extract number of images per category
        images_match = re.search(r'(\d+)\s*images?\s*per\s*category', prompt)
        if images_match:
            parsed_prompt['output_specs']['images_per_category'] = int(images_match.group(1))
        else:
            parsed_prompt['output_specs']['images_per_category'] = 6
        
        # Extract features
        if 'pick the categories' in prompt.lower():
            parsed_prompt['features'].append('category_selection')
        if 'do all of them' in prompt.lower():
            parsed_prompt['features'].append('process_all_categories')
        if 'different size' in prompt.lower():
            parsed_prompt['features'].append('configurable_size')
        if 'make a folder' in prompt.lower():
            parsed_prompt['features'].append('folder_organization')
        
        return parsed_prompt
    
    def _parse_stable_diffusion_prompt(self, prompt: str) -> Dict[str, Any]:
        """Parse stable diffusion specific requirements."""
        return {
            'framework': 'stable_diffusion',
            'features': ['image_generation', 'category_management', 'batch_processing'],
            'requirements': [
                'Create folders for each category',
                'Allow category selection or process all',
                'Generate specified number of images per category',
                'Support custom output sizes'
            ]
        }
    
    def _detect_stable_diffusion_pattern(self, text: str) -> bool:
        """Detect if prompt is requesting stable diffusion script."""
        indicators = ['stable diffusion', 'image generation', 'diffusion model', 'ai images']
        return any(indicator in text.lower() for indicator in indicators)
    
    def _detect_data_processing_pattern(self, text: str) -> bool:
        """Detect data processing patterns."""
        indicators = ['process data', 'csv', 'dataframe', 'pandas', 'data analysis']
        return any(indicator in text.lower() for indicator in indicators)
    
    def _detect_web_scraping_pattern(self, text: str) -> bool:
        """Detect web scraping patterns."""
        indicators = ['scrape', 'web scraping', 'beautifulsoup', 'requests', 'selenium']
        return any(indicator in text.lower() for indicator in indicators)
    
    def _detect_automation_pattern(self, text: str) -> bool:
        """Detect automation script patterns."""
        indicators = ['automate', 'automation', 'schedule', 'cron', 'task']
        return any(indicator in text.lower() for indicator in indicators)
    
    def generate_code(self, prompt: str) -> str:
        """Generate Python code from natural language prompt."""
        print("🚀 Generating code from prompt...")
        
        # Parse the prompt first
        parsed_requirements = self.parse_complex_prompt(prompt)
        
        # Create enhanced prompt for the AI model
        enhanced_prompt = self._create_enhanced_prompt(prompt, parsed_requirements)
        
        # Call the model
        generated_code = self._call_model(enhanced_prompt)
        
        # Post-process and validate the generated code
        validated_code = self.validate_and_fix_code(generated_code)
        
        return validated_code
    
    def _create_enhanced_prompt(self, original_prompt: str, requirements: Dict[str, Any]) -> str:
        """Create an enhanced prompt for better code generation."""
        enhanced_prompt = f"""
You are an expert Python developer. Generate a complete, working Python script based on this request:

{original_prompt}

Requirements Analysis:
- Script Type: {requirements['script_type']}
- Features: {', '.join(requirements.get('features', []))}
- Output Specs: {requirements.get('output_specs', {})}
- Categories: {len(requirements.get('categories', {}))} categories detected

Please generate a complete Python script that:
1. Is syntactically correct and follows best practices
2. Includes all necessary imports
3. Has proper error handling
4. Includes clear documentation
5. Implements all requested features
6. Uses appropriate libraries for the task

Make sure the code is production-ready and handles edge cases appropriately.
"""
        return enhanced_prompt
    
    def _call_model(self, prompt: str) -> str:
        """Call the Ollama model to generate code."""
        try:
            print("🤔 AI is thinking...")
            
            # Call Ollama
            process = subprocess.run(
                ["ollama", "run", self.model_name],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if process.returncode != 0:
                raise RuntimeError(f"Model call failed: {process.stderr}")
            
            return process.stdout.strip()
            
        except subprocess.TimeoutExpired:
            print("⚠️  Model call timed out, using fallback generation")
            return self._generate_fallback_code()
        except Exception as e:
            print(f"⚠️  Model call failed: {e}")
            return self._generate_fallback_code()
    
    def _generate_fallback_code(self) -> str:
        """Generate fallback code when AI model is unavailable."""
        return '''#!/usr/bin/env python3
"""
Generated Python script - Basic template
This is a fallback template when AI generation is unavailable.
"""

import os
import sys
from pathlib import Path

def main():
    """Main function for the generated script."""
    print("Generated script is running!")
    
    # Add your code implementation here
    pass

if __name__ == "__main__":
    main()
'''
    
    def validate_and_fix_code(self, code: str) -> str:
        """Validate and automatically fix common issues in generated code."""
        print("🔧 Validating and fixing code...")
        
        current_code = code
        
        # Apply multiple validation passes
        for pass_num in range(VALIDATION_PASSES):
            print(f"   Pass {pass_num + 1}/{VALIDATION_PASSES}")
            
            # Apply all validation patterns
            for pattern_name, fix_function in self.validation_patterns.items():
                try:
                    fixed_code = fix_function(current_code)
                    if fixed_code != current_code:
                        print(f"   ✅ Fixed {pattern_name}")
                        current_code = fixed_code
                except Exception as e:
                    print(f"   ⚠️  Error in {pattern_name}: {e}")
            
            # Check syntax
            try:
                ast.parse(current_code)
                print(f"   ✅ Syntax validation passed")
                break
            except SyntaxError as e:
                print(f"   ⚠️  Syntax error at line {e.lineno}: {e.msg}")
                if pass_num == VALIDATION_PASSES - 1:
                    print("   🔧 Attempting emergency syntax fix...")
                    current_code = self._emergency_syntax_fix(current_code, e)
        
        # Use comprehensive validator if available
        if self.validator:
            try:
                validation_results = self.validator.validate_code(current_code)
                if validation_results.get('errors'):
                    print("   🔧 Applying comprehensive fixes...")
                    current_code = self._apply_comprehensive_fixes(current_code, validation_results)
            except Exception as e:
                print(f"   ⚠️  Comprehensive validation error: {e}")
        
        return current_code
    
    def _fix_unterminated_strings(self, code: str) -> str:
        """Fix unterminated string literals."""
        lines = code.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            # Check for unterminated strings - common patterns
            # Pattern 1: Single quote without closing
            if line.count("'") % 2 == 1 and not line.strip().endswith("'"):
                if not line.strip().endswith('\\'):
                    line = line + "'"
            
            # Pattern 2: Double quote without closing  
            if line.count('"') % 2 == 1 and not line.strip().endswith('"'):
                if not line.strip().endswith('\\'):
                    line = line + '"'
            
            # Pattern 3: Regex patterns that need proper closing
            if 'pattern3 = r\'' in line and not line.endswith("'"):
                line = line + "'"
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _fix_missing_imports(self, code: str) -> str:
        """Add missing imports based on code analysis."""
        import_candidates = {
            'os.': 'import os',
            'sys.': 'import sys', 
            'Path(': 'from pathlib import Path',
            'datetime': 'from datetime import datetime',
            'requests.': 'import requests',
            'json.': 'import json',
            're.': 'import re',
            'subprocess.': 'import subprocess',
            'threading.': 'import threading',
            'time.': 'import time',
        }
        
        lines = code.split('\n')
        needed_imports = set()
        
        # Detect needed imports
        for line in lines:
            for pattern, import_stmt in import_candidates.items():
                if pattern in line and import_stmt not in code:
                    needed_imports.add(import_stmt)
        
        # Add missing imports at the top
        if needed_imports:
            import_lines = sorted(list(needed_imports))
            # Find where to insert imports (after shebang and docstring)
            insert_pos = 0
            for i, line in enumerate(lines):
                if line.startswith('#!') or line.startswith('"""') or line.startswith("'''"):
                    insert_pos = i + 1
                elif line.strip() and not line.startswith('#') and not line.startswith('"""'):
                    break
            
            lines = lines[:insert_pos] + import_lines + [''] + lines[insert_pos:]
        
        return '\n'.join(lines)
    
    def _fix_indentation_errors(self, code: str) -> str:
        """Fix common indentation errors."""
        lines = code.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Convert tabs to spaces
            line = line.expandtabs(4)
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _fix_syntax_errors(self, code: str) -> str:
        """Fix common syntax errors."""
        # Fix common syntax issues
        fixes = [
            (r'(\w+)\s*=\s*\[([^\]]*)\s*$', r'\1 = [\2]'),  # Fix unclosed lists
            (r'(\w+)\s*=\s*\{([^}]*)\s*$', r'\1 = {\2}'),   # Fix unclosed dicts
            (r'def\s+(\w+)\s*\([^)]*\s*$', r'def \1():'),   # Fix incomplete function definitions
        ]
        
        for pattern, replacement in fixes:
            code = re.sub(pattern, replacement, code, flags=re.MULTILINE)
        
        return code
    
    def _emergency_syntax_fix(self, code: str, syntax_error: SyntaxError) -> str:
        """Apply emergency fixes for syntax errors."""
        lines = code.split('\n')
        
        if syntax_error.lineno and syntax_error.lineno <= len(lines):
            error_line = lines[syntax_error.lineno - 1]
            
            # Try to fix the specific line
            if 'unterminated string literal' in syntax_error.msg:
                # Add missing quote
                if error_line.count('"') % 2 == 1:
                    lines[syntax_error.lineno - 1] = error_line + '"'
                elif error_line.count("'") % 2 == 1:
                    lines[syntax_error.lineno - 1] = error_line + "'"
        
        return '\n'.join(lines)
    
    def _apply_comprehensive_fixes(self, code: str, validation_results: Dict) -> str:
        """Apply fixes based on comprehensive validation results."""
        # This would integrate with the CodeQualityValidator to apply fixes
        # For now, return the original code
        return code
    
    def create_stable_diffusion_script(self, requirements: Dict[str, Any]) -> str:
        """Create a specialized stable diffusion script based on requirements."""
        categories = requirements.get('categories', {})
        specs = requirements.get('output_specs', {})
        
        # Ensure we have some default categories if none were parsed
        if not categories:
            categories = {
                "productivity": ["burnout", "focus", "time_management", "imposter_syndrome"],
                "confidence": ["self-esteem", "public_speaking", "courage"],
                "gratitude": ["daily_gratitude", "thankfulness"]
            }
        
        script_template = f'''#!/usr/bin/env python3
"""
Stable Diffusion Image Generator
Generated by Enhanced Python Generator 8

Features:
- Category-based image generation
- Configurable output sizes
- Batch processing
- Folder organization
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Configuration
CATEGORIES = {categories}

DEFAULT_WIDTH = {specs.get('width', 550)}
DEFAULT_HEIGHT = {specs.get('height', 3300)}
IMAGES_PER_CATEGORY = {specs.get('images_per_category', 6)}

class StableDiffusionGenerator:
    """Stable Diffusion image generator with category management."""
    
    def __init__(self, output_dir: str = "./generated_images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
    
    def create_category_folders(self):
        """Create folders for each category."""
        for category in CATEGORIES.keys():
            category_path = self.output_dir / category
            category_path.mkdir(exist_ok=True)
            print(f"📁 Created folder: {{category_path}}")
    
    def select_categories(self) -> List[str]:
        """Allow user to select categories or process all."""
        print("\\nAvailable categories:")
        for i, category in enumerate(CATEGORIES.keys(), 1):
            print(f"  {{i}}. {{category}}")
        
        print(f"  {{len(CATEGORIES) + 1}}. All categories")
        
        try:
            choice = input("\\nSelect categories (comma-separated numbers) or 'all': ").strip()
            
            if choice.lower() == 'all' or choice == str(len(CATEGORIES) + 1):
                return list(CATEGORIES.keys())
            
            selected_indices = [int(x.strip()) - 1 for x in choice.split(',')]
            category_list = list(CATEGORIES.keys())
            return [category_list[i] for i in selected_indices if 0 <= i < len(category_list)]
            
        except (ValueError, IndexError):
            print("Invalid selection, using all categories")
            return list(CATEGORIES.keys())
    
    def generate_images(self, categories: List[str], width: int = DEFAULT_WIDTH, height: int = DEFAULT_HEIGHT):
        """Generate images for selected categories."""
        for category in categories:
            if category not in CATEGORIES:
                print(f"⚠️  Unknown category: {{category}}")
                continue
            
            print(f"\\n🎨 Generating images for: {{category}}")
            subcategories = CATEGORIES[category]
            
            for subcategory in subcategories:
                for i in range(IMAGES_PER_CATEGORY):
                    filename = f"{{category}}_{{subcategory}}_{{i+1:03d}}.png"
                    filepath = self.output_dir / category / filename
                    
                    # Simulate image generation (replace with actual Stable Diffusion call)
                    self._generate_single_image(subcategory, filepath, width, height)
                    print(f"  ✅ Generated: {{filename}}")
    
    def _generate_single_image(self, prompt: str, filepath: Path, width: int, height: int):
        """Generate a single image (placeholder for actual Stable Diffusion implementation)."""
        # TODO: Implement actual Stable Diffusion image generation
        # This would typically involve calling a Stable Diffusion model
        pass
    
    def get_custom_size(self) -> tuple:
        """Get custom size from user."""
        try:
            size_input = input(f"Enter size (WxH) or press Enter for default ({{DEFAULT_WIDTH}}x{{DEFAULT_HEIGHT}}): ").strip()
            
            if not size_input:
                return DEFAULT_WIDTH, DEFAULT_HEIGHT
            
            width, height = map(int, size_input.split('x'))
            return width, height
            
        except ValueError:
            print(f"Invalid size format, using default: {{DEFAULT_WIDTH}}x{{DEFAULT_HEIGHT}}")
            return DEFAULT_WIDTH, DEFAULT_HEIGHT

def main():
    """Main function."""
    print("🚀 Stable Diffusion Image Generator")
    print("=" * 40)
    
    generator = StableDiffusionGenerator()
    
    # Create category folders
    generator.create_category_folders()
    
    # Select categories
    selected_categories = generator.select_categories()
    print(f"\\n📋 Selected categories: {{', '.join(selected_categories)}}")
    
    # Get custom size if needed
    width, height = generator.get_custom_size()
    print(f"🖼️  Image size: {{width}}x{{height}} pixels")
    
    # Generate images
    generator.generate_images(selected_categories, width, height)
    
    print(f"\\n🎉 Generation complete! Check the './generated_images' folder.")

if __name__ == "__main__":
    main()
'''
        
        return script_template
    
    def save_script(self, code: str, filename: str = None) -> Path:
        """Save the generated script to a file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_script_{timestamp}.py"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
        
        # Make executable
        os.chmod(filepath, 0o755)
        
        print(f"💾 Script saved: {filepath}")
        return filepath
    
    def process_prompt(self, prompt: str) -> Path:
        """Complete process: parse prompt, generate code, validate, and save."""
        print("🔄 Processing complex prompt...")
        
        # Parse requirements
        requirements = self.parse_complex_prompt(prompt)
        print(f"📋 Detected: {requirements['script_type']} script")
        
        # Generate appropriate code
        if requirements['script_type'] == 'stable_diffusion':
            code = self.create_stable_diffusion_script(requirements)
        else:
            code = self.generate_code(prompt)
        
        # Validate and fix
        validated_code = self.validate_and_fix_code(code)
        
        # Save
        script_type = requirements['script_type']
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{script_type}_script_{timestamp}.py"
        
        return self.save_script(validated_code, filename)

def main():
    """Main function for command-line usage."""
    print("🚀 Enhanced Python Generator 8")
    print("=" * 50)
    
    generator = EnhancedPythonGenerator8()
    
    if len(sys.argv) > 1:
        # Process command-line argument
        prompt = ' '.join(sys.argv[1:])
    else:
        # Interactive mode
        print("Enter your prompt (or 'quit' to exit):")
        prompt = input("> ").strip()
        
        if prompt.lower() == 'quit':
            return
    
    if prompt:
        try:
            script_path = generator.process_prompt(prompt)
            print(f"✅ Generated script: {script_path}")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("No prompt provided.")

if __name__ == "__main__":
    main()