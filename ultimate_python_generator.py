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
import importlib.util
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
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
# ============================================================

class CodeQualityValidator:
    """Comprehensive code quality validator with auto-fixing capabilities."""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
    
    def validate_and_fix_code(self, code: str, filename: str = "generated_code.py") -> Dict:
        """
        Run comprehensive validation and auto-fix Python code.
        
        Args:
            code: Python code to validate and fix
            filename: Name for the temporary file
            
        Returns:
            Dictionary with validation results and improved code
        """
        results = {
            'valid': True,
            'issues': [],
            'warnings': [],
            'tool_results': {},
            'improved_code': code,
            'fixes_applied': []
        }
        
        # Create temporary file for validation
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code)
            temp_path = temp_file.name
        
        try:
            # 1. Basic syntax validation
            syntax_result = self._validate_syntax(code)
            results['tool_results']['syntax'] = syntax_result
            if not syntax_result['valid']:
                results['valid'] = False
                results['issues'].extend(syntax_result['issues'])
                return results
            
            # 2. Apply BLACK formatting (auto-fix)
            black_result = self._apply_black_formatting(temp_path)
            if black_result['fixed']:
                results['fixes_applied'].append('BLACK: Code formatted')
                code = Path(temp_path).read_text()
                results['improved_code'] = code
            
            # 3. Apply autopep8 style fixes (auto-fix)
            autopep8_result = self._apply_autopep8_fixes(temp_path)
            if autopep8_result['fixed']:
                results['fixes_applied'].append('AUTOPEP8: Style issues fixed')
                code = Path(temp_path).read_text()
                results['improved_code'] = code
            
            # 4. Apply isort import sorting (auto-fix)
            isort_result = self._apply_isort_fixes(temp_path)
            if isort_result['fixed']:
                results['fixes_applied'].append('ISORT: Imports sorted')
                code = Path(temp_path).read_text()
                results['improved_code'] = code
            
            # 5. Bandit security analysis (analysis only)
            bandit_result = self._run_bandit_analysis(temp_path)
            results['tool_results']['bandit'] = bandit_result
            if bandit_result['issues']:
                results['warnings'].extend([f"Security: {issue}" for issue in bandit_result['issues']])
            
            # 6. Flake8 style checking (analysis only, fixes already applied by autopep8)
            flake8_result = self._run_flake8_analysis(temp_path)
            results['tool_results']['flake8'] = flake8_result
            if flake8_result['issues']:
                results['warnings'].extend([f"Style: {issue}" for issue in flake8_result['issues']])
            
            # 7. MyPy type checking (analysis only)
            mypy_result = self._run_mypy_analysis(temp_path)
            results['tool_results']['mypy'] = mypy_result
            if mypy_result['issues']:
                results['warnings'].extend([f"Type: {issue}" for issue in mypy_result['issues']])
            
            # 8. Pylint comprehensive analysis (analysis only)
            pylint_result = self._run_pylint_analysis(temp_path)
            results['tool_results']['pylint'] = pylint_result
            if pylint_result['issues']:
                results['warnings'].extend([f"Quality: {issue}" for issue in pylint_result['issues']])
            
            # 9. Apply additional improvements
            improved_code = self._apply_additional_improvements(results['improved_code'])
            if improved_code != results['improved_code']:
                results['fixes_applied'].append('ENHANCEMENTS: Added docstrings and improvements')
                results['improved_code'] = improved_code
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_path)
            except:
                pass
        
        return results
    
    def _validate_syntax(self, code: str) -> Dict:
        """Validate Python syntax."""
        try:
            ast.parse(code)
            return {'valid': True, 'issues': []}
        except SyntaxError as e:
            return {
                'valid': False,
                'issues': [f"Syntax error at line {e.lineno}: {e.msg}"]
            }
    
    def _apply_black_formatting(self, file_path: str) -> Dict:
        """Apply BLACK code formatting."""
        try:
            result = subprocess.run(
                ['black', '--quiet', file_path],
                capture_output=True, text=True, timeout=30
            )
            return {'fixed': result.returncode == 0, 'output': result.stdout}
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return {'fixed': False, 'output': 'BLACK not available'}
    
    def _apply_autopep8_fixes(self, file_path: str) -> Dict:
        """Apply autopep8 style fixes."""
        try:
            result = subprocess.run(
                ['autopep8', '--in-place', '--aggressive', '--aggressive', file_path],
                capture_output=True, text=True, timeout=30
            )
            return {'fixed': result.returncode == 0, 'output': result.stdout}
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return {'fixed': False, 'output': 'autopep8 not available'}
    
    def _apply_isort_fixes(self, file_path: str) -> Dict:
        """Apply isort import sorting."""
        try:
            result = subprocess.run(
                ['isort', file_path],
                capture_output=True, text=True, timeout=30
            )
            return {'fixed': result.returncode == 0, 'output': result.stdout}
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return {'fixed': False, 'output': 'isort not available'}
    
    def _run_bandit_analysis(self, file_path: str) -> Dict:
        """Run Bandit security analysis."""
        try:
            result = subprocess.run(
                ['bandit', '-f', 'txt', file_path],
                capture_output=True, text=True, timeout=30
            )
            
            issues = []
            if result.stdout and 'No issues identified' not in result.stdout:
                # Parse bandit output for issues
                lines = result.stdout.split('\n')
                for line in lines:
                    if '>> Issue:' in line:
                        issues.append(line.strip())
            
            return {'issues': issues}
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # Basic security checks as fallback
            with open(file_path, 'r') as f:
                code = f.read()
            
            security_issues = []
            if 'eval(' in code:
                security_issues.append("Use of eval() detected - potential security risk")
            if 'exec(' in code:
                security_issues.append("Use of exec() detected - potential security risk")
            if '__import__' in code:
                security_issues.append("Dynamic import detected - review for security")
                
            return {'issues': security_issues}
    
    def _run_flake8_analysis(self, file_path: str) -> Dict:
        """Run Flake8 style analysis."""
        try:
            result = subprocess.run(
                ['flake8', '--max-line-length=88', '--ignore=E501,W503', file_path],
                capture_output=True, text=True, timeout=30
            )
            
            issues = []
            if result.stdout:
                issues = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            
            return {'issues': issues}
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return {'issues': ['Flake8 not available']}
    
    def _run_mypy_analysis(self, file_path: str) -> Dict:
        """Run MyPy type analysis."""
        try:
            result = subprocess.run(
                ['mypy', '--ignore-missing-imports', file_path],
                capture_output=True, text=True, timeout=30
            )
            
            issues = []
            if result.stdout:
                for line in result.stdout.split('\n'):
                    if line and 'error:' in line:
                        issues.append(line.strip())
            
            return {'issues': issues}
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return {'issues': ['MyPy not available']}
    
    def _run_pylint_analysis(self, file_path: str) -> Dict:
        """Run Pylint comprehensive analysis."""
        try:
            result = subprocess.run(
                ['pylint', '--disable=C0114,C0115,C0116', '--score=no', file_path],
                capture_output=True, text=True, timeout=30
            )
            
            issues = []
            if result.stdout:
                lines = result.stdout.split('\n')
                for line in lines:
                    if line and any(prefix in line for prefix in ['C:', 'R:', 'W:', 'E:']):
                        issues.append(line.strip())
            
            return {'issues': issues[:10]}  # Limit to first 10 issues
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return {'issues': ['Pylint not available']}
    
    def _apply_additional_improvements(self, code: str) -> str:
        """Apply additional code improvements."""
        lines = code.split('\n')
        improved_lines = []
        
        # Add shebang if missing
        if not lines[0].startswith('#!'):
            improved_lines.append('#!/usr/bin/env python3')
        
        # Check for module docstring
        has_module_docstring = False
        code_started = False
        
        for i, line in enumerate(lines):
            if line.strip().startswith('#!/usr/bin/env python3'):
                improved_lines.append(line)
                continue
                
            if line.strip().startswith('"""') or line.strip().startswith("'''"):
                has_module_docstring = True
                improved_lines.append(line)
                continue
            
            if line.strip() and not line.strip().startswith('#') and not code_started:
                code_started = True
                if not has_module_docstring:
                    improved_lines.append('"""')
                    improved_lines.append('Generated Python script with comprehensive validation and auto-fixes applied.')
                    improved_lines.append('"""')
                    improved_lines.append('')
                improved_lines.append(line)
            else:
                improved_lines.append(line)
        
        return '\n'.join(improved_lines)
    
    def get_summary(self, results: Dict) -> str:
        """Get a human-readable summary of validation results."""
        summary_lines = []
        
        if results['valid']:
            summary_lines.append("✅ Code validation passed!")
        else:
            summary_lines.append("❌ Code validation failed!")
        
        if results['fixes_applied']:
            summary_lines.append(f"🔧 Auto-fixes applied: {len(results['fixes_applied'])}")
            for fix in results['fixes_applied']:
                summary_lines.append(f"  • {fix}")
        
        if results['warnings']:
            summary_lines.append(f"\n🟡 Warnings to review: {len(results['warnings'])}")
            for warning in results['warnings'][:5]:  # Show first 5 warnings
                summary_lines.append(f"  • {warning}")
            if len(results['warnings']) > 5:
                summary_lines.append(f"  ... and {len(results['warnings']) - 5} more")
        
        return '\n'.join(summary_lines)


class UltimatePythonCodeGenerator:
    """Ultimate Python code generator with comprehensive auto-fixing validation."""
    
    def __init__(self, model_name=OLLAMA_MODEL):
        self.model_name = model_name
        self.output_dir = Path(DEFAULT_OUTPUT_DIR)
        self.backup_dir = Path(BACKUP_DIRECTORY)
        self.context_buffer = []
        self.multi_line_mode = False
        self.current_input = ""
        self.validators_enabled = ENABLE_CODE_VALIDATORS
        self.code_validator = CodeQualityValidator()
        self.ensure_directories()
    
    def ensure_directories(self):
        """Ensure the output and backup directories exist."""
        self.output_dir.mkdir(exist_ok=True, parents=True)
        if BACKUP_BEFORE_VALIDATION:
            self.backup_dir.mkdir(exist_ok=True, parents=True)
    
    def is_complete_structure(self, text: str) -> bool:
        """Check if the input is a complete, valid structure that can be processed."""
        stripped = text.strip()
        
        if not stripped:
            return False
        
        if self._has_unclosed_strings(stripped):
            return False
        
        if self.is_valid_python_structure(stripped):
            return True
        
        # Look for common request patterns
        request_indicators = [
            'create', 'make', 'generate', 'build', 'write', 'develop',
            'implement', 'design', 'script', 'program', 'function',
            'class', 'module', 'tool', 'application', 'system'
        ]
        
        if any(word in stripped.lower() for word in request_indicators):
            return True
        
        if not any(char in stripped for char in ['{', '[', '=', ':', '"']):
            return True
            
        if (stripped.count('{') == stripped.count('}') and
            stripped.count('[') == stripped.count(']') and
            stripped.count('(') == stripped.count(')')):
            
            if (stripped.endswith('}') or stripped.endswith(']') or 
                stripped.endswith(')') or not any(char in stripped for char in ['{', '[', '('])):
                return True
        
        return False
    
    def _has_unclosed_strings(self, text: str) -> bool:
        """Check if there are unclosed string literals."""
        in_single = False
        in_double = False
        i = 0
        while i < len(text):
            char = text[i]
            if char == "'" and not in_double:
                if i > 0 and text[i-1] == '\\':
                    i += 1
                    continue
                in_single = not in_single
            elif char == '"' and not in_single:
                if i > 0 and text[i-1] == '\\':
                    i += 1
                    continue
                in_double = not in_double
            i += 1
        
        return in_single or in_double
    
    def is_incomplete_structure(self, text: str) -> bool:
        """Check if the input appears to be an incomplete data structure."""
        stripped = text.strip()
        
        if self.is_complete_structure(stripped):
            return False
        
        request_words = ['create', 'make', 'generate', 'build', 'write', 'develop', 'script', 'program', 'implement']
        if any(word in stripped.lower() for word in request_words):
            return False
        
        if len(stripped.split()) > 5:
            return False
        
        extremely_obvious_incomplete = (
            stripped.endswith('=') or
            (stripped.endswith('{') and stripped.count('}') == 0) or
            (stripped.endswith('[') and stripped.count(']') == 0) or
            (len(stripped) < 10 and stripped.isidentifier())
        )
        
        return extremely_obvious_incomplete
    
    def is_valid_python_structure(self, text: str) -> bool:
        """Check if the text is a valid Python structure."""
        try:
            ast.parse(text)
            return True
        except SyntaxError:
            return False

    def extract_filename_from_request(self, user_request: str) -> tuple[str, str]:
        """Extract filename from user request if specified."""
        import re
        
        # Pattern 1: "save as filename.py" or "name it filename.py"
        pattern1 = r'(?:save\s+as|name\s+it|call\s+it|filename\s*:?)\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.py)?)'
        match = re.search(pattern1, user_request, re.IGNORECASE)
        if match:
            filename = match.group(1)
            cleaned_request = re.sub(pattern1, '', user_request, flags=re.IGNORECASE).strip()
            return cleaned_request, filename
        
        # Pattern 2: "create filename.py that does..."
        pattern2 = r'create\s+([a-zA-Z_][a-zA-Z0-9_]*\.py)\s+(?:that|to|which)'
        match = re.search(pattern2, user_request, re.IGNORECASE)
        if match:
            filename = match.group(1)
            cleaned_request = re.sub(pattern2, 'create a script that', user_request, flags=re.IGNORECASE).strip()
            return cleaned_request, filename
        
        # Pattern 3: filename at the end
        words = user_request.split()
        if len(words) > 0 and words[-1].endswith('.py'):
            filename = words[-1]
            cleaned_request = ' '.join(words[:-1])
            return cleaned_request, filename
        
        return user_request, None

    def should_confirm_input(self, text: str) -> bool:
        """Determine if we should ask for confirmation on ambiguous input."""
        if not CONFIRM_AMBIGUOUS_INPUT:
            return False
        
        lines = text.strip().split('\n')
        if len(lines) >= CONFIRMATION_THRESHOLD * 2:
            return True
        
        return False

    def call_model(self, prompt: str, purpose: str = "generation") -> str:
        """Call the Ollama model with a prompt and return the response."""
        thinking_active = None
        progress_thread = None
        process = None
        
        try:
            if purpose == "generation":
                print("🤔 Thinking (this may take a while for complex requests)...")
            elif purpose == "validation":
                print("🔍 Validating generated code...")
            
            print("💡 Press Ctrl+C to interrupt if needed")
            
            thinking_active = threading.Event()
            thinking_active.set()
            
            def show_thinking_progress():
                dots = 0
                while thinking_active.is_set():
                    dots = (dots + 1) % 4
                    if purpose == "generation":
                        progress = "   Thinking" + "." * dots
                    else:
                        progress = "   Validating" + "." * dots
                    print(f"\r{progress}", end="", flush=True)
                    time.sleep(0.5)
                print("")
            
            progress_thread = threading.Thread(target=show_thinking_progress, daemon=True)
            progress_thread.start()
            
            process = subprocess.Popen(
                ["ollama", "run", self.model_name],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            stdout, stderr = process.communicate(input=prompt.encode())
            
            thinking_active.clear()
            if progress_thread:
                progress_thread.join(timeout=1)
            
            if process.returncode != 0:
                error_msg = stderr.decode().strip()
                print(f"Error calling model: {error_msg}")
                return None
            
            output = stdout.decode().strip()
            if purpose == "generation":
                print("✓ Model finished thinking!")
            else:
                print("✓ Validation complete!")
            return output
        
        except KeyboardInterrupt:
            print(f"\n⚠️  {purpose.capitalize()} interrupted by user.")
            return None
        except FileNotFoundError:
            print("Error: Ollama not found. Please ensure Ollama is installed and in your PATH.")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
        finally:
            if thinking_active:
                thinking_active.clear()
            if progress_thread:
                progress_thread.join(timeout=1)
            if process:
                try:
                    if process.poll() is None:
                        process.terminate()
                        process.wait(timeout=5)
                except:
                    try:
                        process.kill()
                    except:
                        pass

    def extract_python_code(self, response: str) -> str:
        """Extract Python code from the model response."""
        lines = response.split('\n')
        code_lines = []
        in_code_block = False
        
        for line in lines:
            if line.strip().startswith('```python') or line.strip().startswith('```'):
                if in_code_block:
                    break
                in_code_block = True
                continue
            
            if in_code_block:
                if line.strip() == '```':
                    break
                code_lines.append(line)
        
        if not code_lines:
            for line in lines:
                stripped = line.strip()
                if (not stripped.startswith('Here') and 
                    not stripped.startswith('This') and 
                    not stripped.startswith('The') and
                    stripped and
                    not stripped.endswith(':')):
                    code_lines.append(line)
        
        return '\n'.join(code_lines).strip()

    def validate_python_code(self, code: str) -> bool:
        """Check if the code is syntactically valid Python."""
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False

    def validate_code_with_model(self, code: str, filename: str) -> tuple[str, str]:
        """Use the model to validate and improve the generated code."""
        if not ENABLE_VALIDATION_LOOP:
            return code, "Validation disabled"
        
        validation_prompt = f"""Review and improve this Python code for:

{VALIDATION_LEVEL == 'syntax' and 'Syntax errors only' or 
 VALIDATION_LEVEL == 'logic' and 'Syntax and logic errors' or 
 'Syntax, logic, best practices, proper comments, error handling, and code quality'}

Code to review:
```python
{code}
```

If the code has issues, provide a corrected version. If it's perfect, respond with "CODE_APPROVED" followed by the original code.
Always include the complete corrected code in your response, properly formatted in a code block.

Response:"""
        
        for attempt in range(VALIDATION_PASSES + 1):
            response = self.call_model(validation_prompt, "validation")
            if not response:
                return code, f"Validation failed (attempt {attempt + 1})"
            
            if "CODE_APPROVED" in response:
                return code, "✓ Code approved without changes"
            
            improved_code = self.extract_python_code(response)
            if improved_code and self.validate_python_code(improved_code):
                issues_found = []
                if "syntax" in response.lower():
                    issues_found.append("syntax errors")
                if "logic" in response.lower():
                    issues_found.append("logic issues")
                if "error handling" in response.lower():
                    issues_found.append("error handling")
                if "comment" in response.lower():
                    issues_found.append("comments")
                
                feedback = f"⚠️ Fixed: {', '.join(issues_found) if issues_found else 'code improvements'}"
                return improved_code, feedback
            
            code = improved_code if improved_code else code
        
        return code, f"⚠️ Validation completed ({VALIDATION_PASSES} passes)"

    def create_backup(self, filepath: Path) -> bool:
        """Create a backup of the file before overwriting."""
        if not BACKUP_BEFORE_VALIDATION or not filepath.exists():
            return True
        
        try:
            backup_filename = f"{filepath.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}{filepath.suffix}"
            backup_path = self.backup_dir / backup_filename
            shutil.copy2(filepath, backup_path)
            if SHOW_VALIDATION_FEEDBACK:
                print(f"📄 Backup created: {backup_path}")
            return True
        except Exception as e:
            print(f"⚠️ Backup failed: {e}")
            return False

    def generate_filename(self, user_request: str, specified_name: str = None) -> str:
        """Generate a filename based on the user request or use specified name."""
        if specified_name:
            if not specified_name.endswith('.py'):
                specified_name += '.py'
            return specified_name
        
        words = user_request.lower().split()
        filename_words = []
        
        skip_words = {'make', 'create', 'generate', 'write', 'a', 'an', 'the', 'file', 'script', 'program'}
        
        for word in words:
            clean_word = ''.join(c for c in word if c.isalnum())
            if clean_word and clean_word not in skip_words:
                filename_words.append(clean_word)
        
        if not filename_words:
            filename_words = ['script']
        
        base_name = '_'.join(filename_words[:3])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_name}_{timestamp}.py"

    def save_code(self, code: str, filename: str, output_dir: Path = None) -> bool:
        """Save the generated code to a file."""
        if output_dir is None:
            output_dir = self.output_dir
        
        try:
            output_path = output_dir / filename
            
            if ENABLE_VALIDATION_LOOP:
                self.create_backup(output_path)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            print(f"✓ Code saved to: {output_path}")
            return True
        
        except Exception as e:
            print(f"Error saving file: {e}")
            return False

    def set_output_directory(self, directory: str):
        """Set a new output directory."""
        self.output_dir = Path(directory)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        print(f"Output directory set to: {self.output_dir.absolute()}")

    def handle_multi_line_input(self, user_input: str) -> str:
        """Handle input - process immediately unless it's EXTREMELY obviously incomplete."""
        if not self.multi_line_mode:
            if not self.is_incomplete_structure(user_input):
                return user_input
            
            self.multi_line_mode = True
            self.current_input = user_input
            print("💡 Input appears incomplete. Continue entering data, or type 'END' to process as-is.")
            return None
        else:
            if user_input.strip().upper() == 'END':
                self.multi_line_mode = False
                complete_input = self.current_input
                self.current_input = ""
                return complete_input
            elif user_input.strip().upper() == 'CANCEL':
                self.multi_line_mode = False
                self.current_input = ""
                print("❌ Input cancelled.")
                return None
            else:
                self.current_input += "\n" + user_input
                
                if not self.is_incomplete_structure(self.current_input):
                    self.multi_line_mode = False
                    complete_input = self.current_input
                    self.current_input = ""
                    return complete_input
                
                return None

    def process_request_with_retry(self, user_request: str, output_dir: Path = None):
        """Process a user request with retry logic."""
        for attempt in range(MAX_RETRIES):
            try:
                success = self.process_request(user_request, output_dir, attempt + 1)
                if success:
                    return True
                    
                if attempt < MAX_RETRIES - 1:
                    print(f"⚠️ Attempt {attempt + 1} failed, retrying...")
                    time.sleep(1)
                    
            except Exception as e:
                print(f"⚠️ Attempt {attempt + 1} error: {e}")
                if attempt < MAX_RETRIES - 1:
                    print("Retrying...")
                    time.sleep(1)
        
        print(f"❌ Failed after {MAX_RETRIES} attempts.")
        return False

    def process_request(self, user_request: str, output_dir: Path = None, attempt: int = 1) -> bool:
        """Process a user request to generate Python code."""
        print(f"\n🎯 Processing request{f' (attempt {attempt})' if attempt > 1 else ''}: {user_request[:100]}{'...' if len(user_request) > 100 else ''}")
        
        # Extract filename if specified by user
        cleaned_request, specified_filename = self.extract_filename_from_request(user_request)
        
        # Universal prompt that works for ANY complexity level
        prompt = f"""You are an expert Python developer. Generate ONE COMPLETE, COMPREHENSIVE Python script based on this request:

"{cleaned_request}"

CRITICAL REQUIREMENTS - ALWAYS FOLLOW THESE:
1. Create EXACTLY ONE Python script that handles ALL aspects of the request
2. NEVER break this into multiple separate scripts - everything must be in ONE single file
3. If the request involves multiple categories, data structures, or components - handle ALL of them in the SAME script
4. Include ALL necessary imports, functions, classes, and data structures in this ONE file
5. Make the script complete, functional, and ready to run
6. Include proper error handling and user-friendly interfaces
7. Add clear comments explaining each section
8. If there are multiple operations or categories, create a unified system that handles them all

EXAMPLES OF WHAT TO INCLUDE IN ONE SCRIPT:
- All data structures (dictionaries, lists, etc.)
- All categories and subcategories
- All functionality (file operations, API calls, image generation, etc.)
- All user interface elements (menus, options, etc.)
- All processing logic in one cohesive program

NO MATTER HOW COMPLEX THE REQUEST IS, CREATE ONE COMPREHENSIVE SCRIPT THAT DOES EVERYTHING.

Request details: {cleaned_request}

Generate the complete Python code (no explanations, just code):"""
        
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

def main():
    """Main interactive loop."""
    generator = UltimatePythonCodeGenerator()
    
    print("🚀 Ultimate Python Code Generator with Auto-Fixing Validators")
    print("=" * 80)
    print("This tool generates Python scripts and automatically fixes all code quality issues.")
    print("Give it ANY level of complex prompt - it will create ONE comprehensive script!")
    print("\n🎯 FEATURES:")
    print("  ✓ Handles ANY complexity level in ONE comprehensive script")
    print("  ✓ Intelligent multi-line input support")
    print("  ✓ Automatic code quality validation and fixes")
    print("  ✓ BLACK formatting, autopep8 style fixes, isort import sorting")
    print("  ✓ Security analysis, type checking, quality analysis")
    print("  ✓ Automatic backup system")
    print("  ✓ Retry logic with error recovery")
    print("  ✓ Smart filename detection and generation")
    
    print(f"\n⚙️ CONFIGURATION:")
    print(f"  • Model: {OLLAMA_MODEL}")
    print(f"  • Max retries: {MAX_RETRIES}")
    print(f"  • Model validation: {'Enabled' if ENABLE_VALIDATION_LOOP else 'Disabled'} ({VALIDATION_LEVEL})")
    print(f"  • Code validators: {'Enabled' if ENABLE_CODE_VALIDATORS else 'Disabled'}")
    print(f"  • Backups: {'Enabled' if BACKUP_BEFORE_VALIDATION else 'Disabled'}")
    
    print("\n🔧 AUTO-FIXING TOOLS:")
    print("  • BLACK: Code formatting")
    print("  • AUTOPEP8: Style issue fixes") 
    print("  • ISORT: Import sorting")
    print("  • BANDIT: Security analysis")
    print("  • FLAKE8: Style checking")
    print("  • MYPY: Type checking")
    print("  • PYLINT: Code quality analysis")
    
    print("\n📝 EXAMPLES:")
    print("  - 'make a hello world program'")
    print("  - 'create a file organizer script'")
    print("  - 'generate a web scraper for news articles'")
    print("  - 'create calculator.py that does basic math'  (uses specified filename)")
    print("  - 'make an image processor save as image_tools.py'")
    print("  - Complex prompts with multiple categories and data structures")
    print("  - Large dictionary-based prompts (ALL handled as ONE comprehensive script)")
    print("  - Multi-component applications (web servers, data processors, AI tools, etc.)")
    print("  📌 NO MATTER HOW COMPLEX - ALWAYS CREATES ONE PERFECT SCRIPT")
    
    print("\n💡 COMMANDS:")
    print("  'set output <directory>' - Change output directory")
    print("  'clear context' - Clear multi-line input buffer")
    print("  'toggle validators' - Enable/disable code validators")
    print("  'quit' or 'exit' - Exit the program")
    print("=" * 80)
    print(f"Current output directory: {generator.output_dir.absolute()}")
    if BACKUP_BEFORE_VALIDATION:
        print(f"Backup directory: {generator.backup_dir.absolute()}")
    print("")
    
    while True:
        try:
            prompt = "What Python script would you like me to generate? > "
            user_input = input(prompt).strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break
            
            if user_input.lower() == 'clear context':
                generator.multi_line_mode = False
                generator.current_input = ""
                generator.context_buffer = []
                print("✓ Context cleared.")
                continue
            
            if user_input.lower() == 'toggle validators':
                generator.validators_enabled = not generator.validators_enabled
                status = "enabled" if generator.validators_enabled else "disabled"
                print(f"✓ Code validators {status}.")
                continue
            
            if user_input.lower().startswith('set output '):
                new_dir = user_input[11:].strip()
                if new_dir:
                    generator.set_output_directory(new_dir)
                else:
                    print("Please specify a directory path.")
                continue
            
            # Handle multi-line input
            processed_input = generator.handle_multi_line_input(user_input)
            
            if processed_input is not None:
                # Process the code generation request with retry logic
                generator.process_request_with_retry(processed_input)
                print("")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

if __name__ == "__main__":
    main()