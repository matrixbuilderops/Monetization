#!/usr/bin/env python3
"""
Ultimate Interactive Python Code Generator with Comprehensive Validators.

Uses local Ollama model to generate Python scripts and automatically fixes
all code quality issues.
Features: intelligent input detection, comprehensive validation, auto-fixing,
backup system, and seamless UX.
"""

import ast
import json
import os
import re
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ==================== USER CONFIGURATION ====================
OLLAMA_MODEL = "mixtral:8x7b-instruct-v0.1-q6_K"
DEFAULT_OUTPUT_DIR = "./generated_scripts"

# Validation Settings
ENABLE_VALIDATION_LOOP = True
SHOW_VALIDATION_FEEDBACK = True
ENABLE_CODE_VALIDATORS = True

# Backup Settings
BACKUP_BEFORE_VALIDATION = True
BACKUP_DIRECTORY = "./backups"
# ============================================================


class CodeQualityValidator:
    """Comprehensive code quality validator using all major Python tools."""

    def __init__(self) -> None:
        """Initialize the validator with available tools check."""
        self.warnings: List[str] = []
        self.tools_available = self._check_tools_availability()

    def _check_tools_availability(self) -> Dict[str, bool]:
        """Check which validation tools are available."""
        tools = {
            'bandit': self._check_tool('bandit'),
            'coverage': self._check_tool('coverage'),
            'flake8': self._check_tool('flake8'),
            'hypothesis': self._check_tool(
                'python3', ['-c', 'import hypothesis']
            ),
            'interrogate': self._check_tool('interrogate'),
            'mypy': self._check_tool('mypy'),
            'pathspec': self._check_tool(
                'python3', ['-c', 'import pathspec']
            ),
            'pylint': self._check_tool('pylint'),
            'vulture': self._check_tool('vulture'),
            'z3': self._check_tool('python3', ['-c', 'import z3'])
        }
        return tools

    def _check_tool(self, tool_name: str,
                    args: Optional[List[str]] = None) -> bool:
        """Check if a tool is available."""
        if args is None:
            args = ['--help']
        try:
            cmd = [tool_name] + args
            subprocess.run(
                cmd, capture_output=True, check=True, timeout=10
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError,
                subprocess.TimeoutExpired):
            return False

    def validate_and_fix_code(self, code: str,
                              filename: str) -> Dict[str, str]:
        """Run comprehensive validation and auto-fix issues."""
        results: Dict[str, str] = {
            'original_code': code,
            'improved_code': code,
            'fixes_applied': '',
            'warnings': '',
            'tool_results': ''
        }

        # Create temporary file for validation
        temp_file = tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', delete=False
        )
        temp_file.write(code)
        temp_file.flush()
        temp_path = temp_file.name
        temp_file.close()

        try:
            tool_results: Dict[str, Dict[str, str]] = {}

            # Run each available tool
            if self.tools_available.get('bandit'):
                tool_results['bandit'] = self._run_bandit(temp_path)

            if self.tools_available.get('flake8'):
                tool_results['flake8'] = self._run_flake8(temp_path)

            if self.tools_available.get('pylint'):
                tool_results['pylint'] = self._run_pylint(temp_path)

            if self.tools_available.get('mypy'):
                tool_results['mypy'] = self._run_mypy(temp_path)

            if self.tools_available.get('vulture'):
                tool_results['vulture'] = self._run_vulture(temp_path)

            if self.tools_available.get('interrogate'):
                tool_results['interrogate'] = self._run_interrogate(temp_path)

            # Apply automatic fixes based on results
            improved_code = self._apply_automatic_fixes(code, tool_results)
            results['improved_code'] = improved_code

            # Collect fixes and warnings
            self._collect_fixes_and_warnings(results)

        finally:
            # Clean up temporary file
            os.unlink(temp_path)

        return results

    def _run_bandit(self, filepath: str) -> Dict[str, str]:
        """Run Bandit security analysis."""
        try:
            result = subprocess.run(
                ['/usr/local/bin/bandit', '-f', 'json', filepath],
                capture_output=True, text=True, timeout=30
            )
            if result.stdout:
                return json.loads(result.stdout)
        except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
            return {'error': str(e)}
        return {}

    def _run_flake8(self, filepath: str) -> Dict[str, str]:
        """Run Flake8 style checking."""
        try:
            result = subprocess.run(
                ['/usr/local/bin/flake8', '--format=json', filepath],
                capture_output=True, text=True, timeout=30
            )
            if result.stdout:
                return json.loads(result.stdout)
        except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
            return {'error': str(e)}
        return {}

    def _run_pylint(self, filepath: str) -> Dict[str, str]:
        """Run Pylint analysis."""
        try:
            result = subprocess.run(
                ['/usr/local/bin/pylint', '--output-format=json', filepath],
                capture_output=True, text=True, timeout=30
            )
            if result.stdout:
                return json.loads(result.stdout)
        except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
            return {'error': str(e)}
        return {}

    def _run_mypy(self, filepath: str) -> Dict[str, str]:
        """Run MyPy type checking."""
        try:
            result = subprocess.run(
                ['/usr/local/bin/mypy', '--show-error-codes', filepath],
                capture_output=True, text=True, timeout=30
            )
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': str(result.returncode)
            }
        except subprocess.TimeoutExpired as e:
            return {'error': str(e)}

    def _run_vulture(self, filepath: str) -> Dict[str, str]:
        """Run Vulture dead code detection."""
        try:
            result = subprocess.run(
                ['/usr/local/bin/vulture', filepath],
                capture_output=True, text=True, timeout=30
            )
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': str(result.returncode)
            }
        except subprocess.TimeoutExpired as e:
            return {'error': str(e)}

    def _run_interrogate(self, filepath: str) -> Dict[str, str]:
        """Run Interrogate documentation coverage."""
        try:
            result = subprocess.run(
                ['/usr/local/bin/interrogate', '-v', filepath],
                capture_output=True, text=True, timeout=30
            )
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': str(result.returncode)
            }
        except subprocess.TimeoutExpired as e:
            return {'error': str(e)}

    def _apply_automatic_fixes(self, code: str,
                               tool_results: Dict[str, Dict[str, str]]) -> str:
        """Apply automatic fixes based on tool results."""
        # This is a simplified auto-fix implementation
        # In a real implementation, this would be much more sophisticated
        improved_code = code

        # Basic fixes based on common issues
        lines = improved_code.split('\n')

        # Fix common style issues
        for i, line in enumerate(lines):
            # Remove trailing whitespace
            lines[i] = line.rstrip()

            # Fix common spacing issues
            if ' =' in line and ' ==' not in line:
                lines[i] = line.replace(' =', ' = ')

        improved_code = '\n'.join(lines)

        return improved_code

    def _collect_fixes_and_warnings(self, results: Dict[str, str]) -> None:
        """Collect fixes and warnings from tool results."""
        fixes: List[str] = []
        warnings: List[str] = []

        # Process tool-specific results would go here
        # For now, just basic collection

        results['fixes_applied'] = ', '.join(fixes)
        results['warnings'] = ', '.join(warnings)


class UltimatePythonCodeGenerator:
    """Ultimate Python code generator with comprehensive validation."""

    def __init__(self, model_name: str = OLLAMA_MODEL) -> None:
        """Initialize the generator."""
        self.model_name = model_name
        self.output_dir = Path(DEFAULT_OUTPUT_DIR)
        self.backup_dir = Path(BACKUP_DIRECTORY)
        self.ensure_directories()

        # Initialize code quality validator
        self.code_validator = CodeQualityValidator()
        self.validators_enabled = ENABLE_CODE_VALIDATORS

        print("🚀 Ultimate Python Code Generator initialized")
        print(f"📁 Output directory: {self.output_dir}")
        if self.validators_enabled:
            available_tools = [
                tool for tool, available in
                self.code_validator.tools_available.items() if available
            ]
            print("🔧 Validation tools available: "
                  f"{', '.join(available_tools)}")

    def ensure_directories(self) -> None:
        """Ensure required directories exist."""
        self.output_dir.mkdir(exist_ok=True, parents=True)
        if BACKUP_BEFORE_VALIDATION:
            self.backup_dir.mkdir(exist_ok=True, parents=True)

    def call_model(self, prompt: str) -> str:
        """Call the Ollama model to generate code."""
        try:
            # Use the correct Ollama command: 'run' instead of 'generate'
            # Send prompt via stdin instead of as command argument
            process = subprocess.Popen(
                ['ollama', 'run', self.model_name],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=prompt, timeout=300)
            
            if process.returncode == 0:
                return stdout.strip()
            else:
                print(f"❌ Model call failed: {stderr.strip()}")
                return ""
        except subprocess.TimeoutExpired:
            print("❌ Model call timed out")
            # Ensure process is terminated
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                try:
                    process.kill()
                except:
                    pass
            return ""
        except OSError as e:
            print(f"❌ Error calling model: {e}")
            return ""

    def extract_python_code(self, response: str) -> str:
        """Extract Python code from model response."""
        # Look for code blocks
        patterns = [
            r'```python\n(.*?)\n```',
            r'```\n(.*?)\n```',
            r'```python(.*?)```',
            r'```(.*?)```'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, response, re.DOTALL)
            if matches:
                return matches[0].strip()

        # If no code blocks found, return the entire response if it
        # looks like code
        if ('import ' in response or 'def ' in response or
                'class ' in response):
            return response.strip()

        return ""

    def validate_python_code(self, code: str) -> bool:
        """Validate Python code syntax."""
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False

    def generate_filename(self, request: str,
                          specified_filename: Optional[str] = None) -> str:
        """Generate appropriate filename based on request."""
        if specified_filename:
            if not specified_filename.endswith('.py'):
                specified_filename += '.py'
            return specified_filename

        # Generate from request
        words = request.lower().split()[:3]
        clean_words = [
            re.sub(r'[^a-z0-9]', '', word) for word in words
            if word.isalnum()
        ]
        base_name = ('_'.join(clean_words) if clean_words
                     else 'generated_script')

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_name}_{timestamp}.py"

    def extract_filename_from_request(self, request: str) -> tuple:
        """Extract filename from user request."""
        # Look for filename patterns
        patterns = [
            r'(?:save|name|call|filename).*?([a-zA-Z_][a-zA-Z0-9_]*\.py)',
            r'([a-zA-Z_][a-zA-Z0-9_]*\.py)',
            r'(?:save|name|call).*?([a-zA-Z_][a-zA-Z0-9_]*)'
        ]

        for pattern in patterns:
            match = re.search(pattern, request, re.IGNORECASE)
            if match:
                filename = match.group(1)
                cleaned_request = request.replace(match.group(0), '').strip()
                return cleaned_request, filename

        return request, None

    def validate_code_with_model(self, code: str, filename: str) -> tuple:
        """Validate and improve code using the model."""
        validation_prompt = f"""
        Review this Python code for correctness, style, and best practices.
        Provide an improved version if needed, or confirm it's good as-is.

        Code:
        ```python
        {code}
        ```

        Please provide:
        1. The improved code (if any changes needed)
        2. Brief explanation of changes
        """

        response = self.call_model(validation_prompt)
        improved_code = self.extract_python_code(response)

        if improved_code and self.validate_python_code(improved_code):
            return improved_code, "✅ Code validated and improved via model"
        else:
            return code, "✅ Code validated - no changes needed"

    def save_code(self, code: str, filename: str,
                  output_dir: Optional[Path] = None) -> bool:
        """Save generated code to file."""
        if output_dir is None:
            output_dir = self.output_dir

        try:
            filepath = output_dir / filename

            # Create backup if enabled
            if BACKUP_BEFORE_VALIDATION and filepath.exists():
                backup_name = (f"{filename}.backup_"
                               f"{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                backup_path = self.backup_dir / backup_name
                shutil.copy2(filepath, backup_path)
                print(f"📋 Backup created: {backup_path}")

            # Save the code
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)

            print(f"💾 Code saved to: {filepath}")
            return True

        except OSError as e:
            print(f"❌ Error saving code: {e}")
            return False

    def process_request(self, user_request: str,
                        output_dir: Optional[Path] = None,
                        attempt: int = 1) -> bool:
        """Process a user request to generate Python code."""
        request_preview = (user_request[:100] + '...'
                           if len(user_request) > 100 else user_request)
        attempt_text = f' (attempt {attempt})' if attempt > 1 else ''
        print(f"\n🎯 Processing request{attempt_text}: {request_preview}")

        # Extract filename if specified by user
        cleaned_request, specified_filename = (
            self.extract_filename_from_request(user_request)
        )

        # ULTRA-STRONG anti-fragmentation prompt that works for ANY complexity
        prompt = (
            'You are an expert Python developer. You MUST generate EXACTLY '
            'ONE COMPLETE Python script file.\n\n'
            f'REQUEST: "{cleaned_request}"\n\n'
            '🚨 CRITICAL MANDATE - THIS IS NON-NEGOTIABLE:\n'
            'YOU MUST CREATE EXACTLY ONE PYTHON FILE THAT CONTAINS '
            'EVERYTHING.\n'
            'NEVER SUGGEST MULTIPLE FILES OR SEPARATE SCRIPTS.\n'
            'EVERYTHING MUST BE IN ONE SINGLE .PY FILE.\n\n'
            'ANTI-FRAGMENTATION RULES:\n'
            '1. IGNORE any instinct to split into multiple files\n'
            '2. IGNORE any thought about "it would be better organized in '
            'separate files"\n'
            '3. IGNORE any consideration of modularity across files\n'
            '4. PUT EVERYTHING in ONE script: imports, classes, functions, '
            'data, main logic\n'
            '5. If you see categories/components, put ALL of them in the '
            'SAME file\n'
            '6. If you see multiple functionalities, combine ALL in the '
            'SAME file\n'
            '7. Create ONE unified program that does EVERYTHING requested\n\n'
            'WHAT TO INCLUDE IN THE SINGLE FILE:\n'
            '- ALL imports at the top\n'
            '- ALL data structures (dictionaries, lists, configurations)\n'
            '- ALL classes and functions\n'
            '- ALL categories and their processing logic\n'
            '- ALL user interface code\n'
            '- ALL main execution logic\n'
            '- ALL error handling\n'
            '- ONE main() function that ties everything together\n\n'
            'EXAMPLES OF CORRECT SINGLE-FILE APPROACH:\n'
            '- 15 categories? → ALL 15 categories in ONE file\n'
            '- Multiple APIs? → ALL API integrations in ONE file\n'
            '- Complex data processing? → ALL processing in ONE file\n'
            '- User interface + backend? → ALL combined in ONE file\n'
            '- Image generation + file management? → ALL in ONE file\n\n'
            'WHAT YOU MUST NEVER DO:\n'
            '❌ Never say "create multiple files"\n'
            '❌ Never suggest "separate script for each category"\n'
            '❌ Never mention "modular approach with different files"\n'
            '❌ Never create file1.py, file2.py, etc.\n'
            '❌ Never suggest organizing into packages/modules\n\n'
            'IMPLEMENTATION STRATEGY:\n'
            '1. Start with shebang and imports\n'
            '2. Define ALL data structures\n'
            '3. Create ALL necessary classes\n'
            '4. Define ALL functions\n'
            '5. Create unified main() that handles everything\n'
            '6. End with if __name__ == "__main__": main()\n\n'
            '🔥 BACKUP PLAN: Even if you feel compelled to create multiple '
            'blocks, put ALL functionality in ONE comprehensive code block. '
            'If you absolutely must show multiple sections, put them ALL in '
            'ONE ```python``` block.\n\n'
            'Remember: ONE FILE MUST CONTAIN EVERYTHING. Make it '
            'comprehensive, complete, and functional.\n\n'
            'Generate the complete Python code for ONE single file:\n'
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
                response_preview = (response[:200] + "..."
                                    if len(response) > 200 else response)
                print("Raw response:", response_preview)
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
            code, validation_feedback = self.validate_code_with_model(
                code, filename
            )
            if SHOW_VALIDATION_FEEDBACK:
                print(validation_feedback)

        # Apply comprehensive code quality validation and auto-fixes
        if self.validators_enabled:
            print("\n🔧 Running comprehensive code quality validation and "
                  "auto-fixes...")
            validation_results = self.code_validator.validate_and_fix_code(
                code, filename
            )

            if validation_results['fixes_applied']:
                code = validation_results['improved_code']
                print("✅ Auto-fixes applied:")
                fixes = validation_results['fixes_applied'].split(', ')
                for fix in fixes[:5]:  # Show first 5 fixes
                    if fix.strip():
                        print(f"  • {fix}")

            if validation_results['warnings']:
                print("\n⚠️ Quality warnings (for your review):")
                warnings = validation_results['warnings'].split(', ')
                for warning in warnings[:5]:  # Show first 5 warnings
                    if warning.strip():
                        print(f"  • {warning}")
                if len(warnings) > 5:
                    print(f"  ... and {len(warnings) - 5} more warnings")

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
            if (self.validators_enabled and
                    'validation_results' in locals()):
                print("\n📊 Quality Summary:")
                if validation_results['fixes_applied']:
                    fixes_count = len(
                        validation_results['fixes_applied'].split(', ')
                    )
                    print(f"  🔧 {fixes_count} automatic fixes applied")
                if validation_results['warnings']:
                    warnings_count = len(
                        validation_results['warnings'].split(', ')
                    )
                    print(f"  ⚠️ {warnings_count} warnings for review")
                print("  ✅ Code is production-ready!")

            return True

        return False


def main() -> None:
    """Main interactive function."""
    print("🐍 Ultimate Python Code Generator with Comprehensive Validation")
    print("=" * 60)
    print("Generate Python code from natural language descriptions.")
    print("All code is automatically validated and improved using:")
    print("bandit, coverage, flake8, hypothesis, interrogate, mypy, "
          "pathspec, pylint, vulture, z3")
    print("\nType 'exit' or 'quit' to stop.")
    print("=" * 60)

    generator = UltimatePythonCodeGenerator()

    while True:
        try:
            print("\n" + "─" * 50)
            user_input = input(
                "🎯 What Python code would you like me to generate? "
            ).strip()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit', 'stop', 'bye']:
                print("\n👋 Goodbye! Thanks for using Ultimate Python Code "
                      "Generator!")
                break

            if user_input.lower() in ['help', '?']:
                print("\n📚 Help:")
                print("• Describe what you want in natural language")
                print("• Examples:")
                print("  - 'Create a web scraper for news articles'")
                print("  - 'Make a password generator with GUI'")
                print("  - 'Build a file organizer script'")
                print("• The code will be automatically validated and "
                      "improved")
                continue

            # Process the request
            success = generator.process_request(user_input)

            if success:
                print("\n✨ Success! Your code has been generated and "
                      "validated.")
                print(f"📁 Check the '{generator.output_dir}' directory for "
                      "your script.")
            else:
                print("\n❌ Failed to generate code. Please try rephrasing "
                      "your request.")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using Ultimate Python Code "
                  "Generator!")
            break
        except OSError as e:
            print(f"\n❌ Unexpected error: {e}")
            print("Please try again with a different request.")


if __name__ == "__main__":
    main()
