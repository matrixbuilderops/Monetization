#!/usr/bin/env python3
"""
Comprehensive Code Quality Validator
Integrates all major Python code quality tools for perfect code generation.
"""

import ast
import os
import sys
import tempfile
import subprocess
import importlib.util
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import shutil
import warnings

# Add integrated tools to Python path
TOOLS_DIR = Path(__file__).parent / "integrated_tools"

class CodeQualityValidator:
    """Comprehensive code quality validator using integrated tools."""
    
    def __init__(self):
        self.tools_dir = TOOLS_DIR
        self.issues = []
        self.warnings = []
        self.setup_tools()
    
    def setup_tools(self):
        """Set up all integrated tools for use."""
        # Add all tool directories to Python path
        tool_paths = [
            self.tools_dir / "bandit-main",
            self.tools_dir / "coveragepy-master",
            self.tools_dir / "flake8-main" / "src",
            self.tools_dir / "hypothesis-master",
            self.tools_dir / "interrogate-master",
            self.tools_dir / "mypy-master",
            self.tools_dir / "pylint-main",
            self.tools_dir / "vulture-main",
            self.tools_dir / "z3-master"
        ]
        
        for path in tool_paths:
            if path.exists():
                sys.path.insert(0, str(path))
    
    def validate_code(self, code: str, filename: str = "generated_code.py") -> Dict:
        """
        Run comprehensive validation on Python code using all integrated tools.
        
        Args:
            code: Python code to validate
            filename: Name for the temporary file
            
        Returns:
            Dictionary with validation results from all tools
        """
        results = {
            'valid': True,
            'issues': [],
            'warnings': [],
            'tool_results': {},
            'improved_code': code
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
            
            # 2. Bandit security analysis
            bandit_result = self._run_bandit(temp_path)
            results['tool_results']['bandit'] = bandit_result
            if bandit_result['issues']:
                results['issues'].extend([f"Security: {issue}" for issue in bandit_result['issues']])
            
            # 3. Flake8 style and error checking
            flake8_result = self._run_flake8(temp_path)
            results['tool_results']['flake8'] = flake8_result
            if flake8_result['issues']:
                results['issues'].extend([f"Style: {issue}" for issue in flake8_result['issues']])
            
            # 4. MyPy type checking
            mypy_result = self._run_mypy(temp_path)
            results['tool_results']['mypy'] = mypy_result
            if mypy_result['issues']:
                results['warnings'].extend([f"Type: {issue}" for issue in mypy_result['issues']])
            
            # 5. Pylint comprehensive analysis
            pylint_result = self._run_pylint(temp_path)
            results['tool_results']['pylint'] = pylint_result
            if pylint_result['issues']:
                results['warnings'].extend([f"Quality: {issue}" for issue in pylint_result['issues']])
            
            # 6. Vulture dead code detection
            vulture_result = self._run_vulture(temp_path)
            results['tool_results']['vulture'] = vulture_result
            if vulture_result['issues']:
                results['warnings'].extend([f"Dead code: {issue}" for issue in vulture_result['issues']])
            
            # 7. Interrogate documentation coverage
            interrogate_result = self._run_interrogate(temp_path)
            results['tool_results']['interrogate'] = interrogate_result
            if interrogate_result['issues']:
                results['warnings'].extend([f"Documentation: {issue}" for issue in interrogate_result['issues']])
            
            # 8. Apply fixes and improvements
            improved_code = self._apply_fixes(code, results['tool_results'])
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
    
    def _run_bandit(self, file_path: str) -> Dict:
        """Run Bandit security analysis."""
        try:
            # Try subprocess first as it's more reliable
            result = subprocess.run(
                [sys.executable, '-m', 'bandit', '-f', 'json', file_path],
                capture_output=True, text=True, cwd=str(self.tools_dir / "bandit-main")
            )
            
            issues = []
            if result.stdout:
                try:
                    import json
                    data = json.loads(result.stdout)
                    for issue in data.get('results', []):
                        issues.append(f"{issue['test_id']}: {issue['issue_text']} (Severity: {issue['issue_severity']})")
                except:
                    # Fallback to text parsing
                    if 'No issues identified' not in result.stdout:
                        issues.append("Security issues detected")
            
            return {'issues': issues}
            
        except Exception as e:
            # Basic security checks as fallback
            with open(file_path, 'r') as f:
                code = f.read()
            
            security_issues = []
            # Basic security checks
            if 'eval(' in code:
                security_issues.append("Use of eval() detected - potential security risk")
            if 'exec(' in code:
                security_issues.append("Use of exec() detected - potential security risk")
            if 'input(' in code and 'eval' in code:
                security_issues.append("Potential code injection via input() and eval()")
            if '__import__' in code:
                security_issues.append("Dynamic import detected - review for security")
                
            return {'issues': security_issues}
    
    def _run_flake8(self, file_path: str) -> Dict:
        """Run Flake8 style checking."""
        try:
            import flake8.api.legacy as flake8
            
            style_guide = flake8.get_style_guide(
                max_line_length=88,
                ignore=['E501', 'W503']  # Ignore line length and line break before binary operator
            )
            
            # Capture flake8 output
            report = style_guide.check_files([file_path])
            
            issues = []
            # Get issues from the report
            for error in report.get_statistics('E'):
                issues.append(error)
            for warning in report.get_statistics('W'):
                issues.append(warning)
                
            return {'issues': issues}
            
        except Exception as e:
            # Fallback to subprocess if direct import fails
            try:
                result = subprocess.run(
                    [sys.executable, '-m', 'flake8', '--max-line-length=88', '--ignore=E501,W503', file_path],
                    capture_output=True, text=True, cwd=str(self.tools_dir / "flake8-main")
                )
                issues = result.stdout.strip().split('\n') if result.stdout.strip() else []
                return {'issues': issues}
            except Exception as e2:
                return {'issues': [f"Flake8 analysis failed: {str(e2)}"]}
    
    def _run_mypy(self, file_path: str) -> Dict:
        """Run MyPy type checking."""
        try:
            # Try to run mypy as subprocess
            result = subprocess.run(
                [sys.executable, '-m', 'mypy', '--ignore-missing-imports', file_path],
                capture_output=True, text=True, cwd=str(self.tools_dir / "mypy-master")
            )
            
            issues = []
            if result.stdout:
                for line in result.stdout.strip().split('\n'):
                    if line and 'error:' in line:
                        issues.append(line)
            
            return {'issues': issues}
            
        except Exception as e:
            return {'issues': [f"MyPy analysis failed: {str(e)}"]}
    
    def _run_pylint(self, file_path: str) -> Dict:
        """Run Pylint comprehensive analysis."""
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pylint', '--disable=C0114,C0115,C0116', file_path],
                capture_output=True, text=True, cwd=str(self.tools_dir / "pylint-main")
            )
            
            issues = []
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line and any(char in line for char in ['C:', 'R:', 'W:', 'E:']):
                        issues.append(line)
            
            return {'issues': issues[:10]}  # Limit to first 10 issues
            
        except Exception as e:
            return {'issues': [f"Pylint analysis failed: {str(e)}"]}
    
    def _run_vulture(self, file_path: str) -> Dict:
        """Run Vulture dead code detection."""
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'vulture', file_path],
                capture_output=True, text=True, cwd=str(self.tools_dir / "vulture-main")
            )
            
            issues = []
            if result.stdout:
                issues = [line for line in result.stdout.strip().split('\n') if line]
            
            return {'issues': issues}
            
        except Exception as e:
            return {'issues': [f"Vulture analysis failed: {str(e)}"]}
    
    def _run_interrogate(self, file_path: str) -> Dict:
        """Run Interrogate documentation coverage."""
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'interrogate', '-v', file_path],
                capture_output=True, text=True, cwd=str(self.tools_dir / "interrogate-master")
            )
            
            issues = []
            # Parse interrogate output for missing documentation
            if result.stdout and 'missing docstring' in result.stdout.lower():
                issues.append("Missing docstrings detected")
            
            return {'issues': issues}
            
        except Exception as e:
            return {'issues': [f"Interrogate analysis failed: {str(e)}"]}
    
    def _apply_fixes(self, code: str, tool_results: Dict) -> str:
        """Apply automatic fixes based on tool results."""
        improved_code = code
        
        # Add basic improvements
        if not improved_code.startswith('#!/usr/bin/env python3'):
            if not improved_code.startswith('#'):
                improved_code = '#!/usr/bin/env python3\n"""Generated Python script."""\n\n' + improved_code
        
        # Add basic docstring if missing
        lines = improved_code.split('\n')
        has_module_docstring = False
        for line in lines:
            if line.strip().startswith('"""') or line.strip().startswith("'''"):
                has_module_docstring = True
                break
            elif line.strip() and not line.strip().startswith('#'):
                break
        
        if not has_module_docstring:
            # Insert docstring after shebang
            for i, line in enumerate(lines):
                if line.strip() and not line.strip().startswith('#'):
                    lines.insert(i, '"""Generated Python script with comprehensive validation."""')
                    lines.insert(i+1, '')
                    break
            improved_code = '\n'.join(lines)
        
        return improved_code
    
    def get_summary(self, results: Dict) -> str:
        """Get a human-readable summary of validation results."""
        summary_lines = []
        
        if results['valid']:
            summary_lines.append("✅ Code validation passed!")
        else:
            summary_lines.append("❌ Code validation failed!")
        
        # Count issues by type
        security_issues = len([i for i in results['issues'] if i.startswith('Security:')])
        style_issues = len([i for i in results['issues'] if i.startswith('Style:')])
        type_warnings = len([w for w in results['warnings'] if w.startswith('Type:')])
        quality_warnings = len([w for w in results['warnings'] if w.startswith('Quality:')])
        
        summary_lines.append(f"Security issues: {security_issues}")
        summary_lines.append(f"Style issues: {style_issues}")
        summary_lines.append(f"Type warnings: {type_warnings}")
        summary_lines.append(f"Quality warnings: {quality_warnings}")
        
        if results['issues']:
            summary_lines.append("\n🔴 Critical Issues:")
            for issue in results['issues'][:5]:  # Show first 5 issues
                summary_lines.append(f"  • {issue}")
            if len(results['issues']) > 5:
                summary_lines.append(f"  ... and {len(results['issues']) - 5} more")
        
        if results['warnings']:
            summary_lines.append("\n🟡 Warnings:")
            for warning in results['warnings'][:3]:  # Show first 3 warnings
                summary_lines.append(f"  • {warning}")
            if len(results['warnings']) > 3:
                summary_lines.append(f"  ... and {len(results['warnings']) - 3} more")
        
        return '\n'.join(summary_lines)

# Example usage
if __name__ == "__main__":
    validator = CodeQualityValidator()
    
    # Test with sample code
    test_code = '''
def hello_world():
    print("Hello, World!")

if __name__ == "__main__":
    hello_world()
'''
    
    results = validator.validate_code(test_code)
    print(validator.get_summary(results))
    print("\nImproved code:")
    print(results['improved_code'])