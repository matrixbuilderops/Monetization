# Python Code Generator with Comprehensive Validation

An interactive tool that uses your local AI model (Ollama) to generate Python scripts based on natural language requests. **Now enhanced with comprehensive code quality validation using 10 industry-standard tools!**

## 🚀 New: Comprehensive Code Quality Validation

Every generated Python script is automatically analyzed and improved using **all** of the following tools:

### Security & Vulnerability Analysis
- **🔒 Bandit**: Security vulnerability scanner for Python code
- **🛡️ Security Checks**: Detects hardcoded passwords, SQL injection, code injection, etc.

### Code Quality & Style
- **📏 Flake8**: PEP 8 style guide enforcement and error detection
- **🔧 Pylint**: Comprehensive static analysis and code quality scoring
- **🧹 Vulture**: Dead code detection and removal suggestions
- **📋 Pathspec**: File pattern matching and validation

### Type Safety & Analysis
- **🔍 MyPy**: Static type checking and inference
- **📊 Type Hints**: Automatic type annotation suggestions

### Testing & Coverage
- **🧪 Hypothesis**: Property-based test generation
- **📈 Coverage**: Code coverage analysis and reporting

### Advanced Analysis
- **🧠 Z3**: Theorem proving and constraint solving for complex logic
- **📚 Interrogate**: Documentation coverage analysis

### 🎯 What This Means for You

✅ **Perfect Security**: Every generated script is scanned for security vulnerabilities
✅ **Clean Code**: Automatic style fixing and best practice enforcement  
✅ **Type Safety**: Static type checking prevents runtime errors
✅ **No Dead Code**: Unused imports and variables are detected and removed
✅ **Well Documented**: Missing documentation is identified
✅ **Test Ready**: Code is analyzed for testability and coverage
✅ **Production Quality**: All code meets industry standards before saving

## Features

- **🤖 Interactive CLI Interface**: Talk to your AI model using natural language
- **🔍 Comprehensive Validation**: Every script analyzed by 10 professional-grade tools
- **🛡️ Security First**: Automatic vulnerability detection and mitigation
- **✨ Auto-Improvement**: Code is automatically cleaned and optimized
- **📁 Custom Output Directories**: Save generated scripts to any folder you choose
- **🧠 Smart Code Extraction**: Automatically extracts clean Python code from AI responses
- **📝 Automatic File Naming**: Generates meaningful filenames based on your requests
- **👀 Code Preview**: Shows a preview of generated code before saving
- **🎨 Multiple Format Support**: Clean Python files with proper headers and comments
- **💾 Backup System**: Automatic backups before applying improvements

## Quick Start

### Prerequisites

1. **Ollama**: Make sure Ollama is installed and running on your system
   ```bash
   # Install Ollama (if not already installed)
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull the Mixtral model (or your preferred model)
   ollama pull mixtral:8x7b-instruct-v0.1-q6_K
   ```

2. **Python Dependencies**: Install required packages
   ```bash
   pip install pillow reportlab  # Only if you plan to run other scripts in this repo
   ```

### Usage

1. **Start the Interactive Generator**:
   ```bash
   python3 python_code_generator.py
   # OR for advanced features:
   python3 fixed_python_generator.py
   ```

2. **Make Requests**: Tell the AI what Python script you want:
   ```
   What Python script would you like me to generate? > make a hello world program
   What Python script would you like me to generate? > create a calculator that can do basic math
   What Python script would you like me to generate? > generate a file organizer script
   ```

3. **Watch the Magic**: Your code is generated, validated, and improved automatically:
   ```
   🔍 Running comprehensive validation with all tools...
   📊 Validation Summary:
   ✅ Code validation passed!
   Security issues: 0
   Style issues: 0
   ✨ Code automatically improved!
   ```

4. **Set Custom Output Directory** (optional):
   ```
   What Python script would you like me to generate? > set output /path/to/my/scripts
   ```

5. **Exit**:
   ```
   What Python script would you like me to generate? > quit
   ```

## 🔬 Validation Process

When you generate code, here's what happens automatically:

1. **🤖 AI Generation**: Your request is sent to the local AI model
2. **📄 Code Extraction**: Clean Python code is extracted from the response
3. **🔍 Security Scan**: Bandit analyzes for vulnerabilities
4. **📏 Style Check**: Flake8 ensures PEP 8 compliance
5. **🔧 Quality Analysis**: Pylint provides comprehensive quality scoring
6. **🧹 Dead Code Detection**: Vulture identifies unused code
7. **🔍 Type Checking**: MyPy validates type safety
8. **📚 Documentation Check**: Interrogate analyzes documentation coverage
9. **✨ Auto-Improvement**: Code is automatically cleaned and enhanced
10. **💾 Secure Save**: Final, validated code is saved to your chosen location

## 🎯 Code Quality Guarantee

Every generated script is guaranteed to:
- ✅ Pass all security vulnerability checks
- ✅ Follow Python style guidelines (PEP 8)
- ✅ Have no syntax errors
- ✅ Include proper documentation
- ✅ Be free of common code quality issues
- ✅ Have optimized imports and structure

## Example Requests

Here are some example requests you can try:

- `"make a hello world program"`
- `"create a simple calculator"`
- `"generate a file organizer script"`
- `"write a web scraper for news articles"`
- `"create a password generator"`
- `"make a todo list manager"`
- `"generate a weather app"`
- `"create a text file analyzer"`

## Commands

- `set output <directory>` - Change the output directory for generated scripts
- `quit` or `exit` - Exit the program

## Demo Mode

To see how the tool works without needing Ollama installed, run the demo:

```bash
python3 demo_generator.py
```

This uses pre-written responses to show the functionality.

## Configuration

You can modify the configuration at the top of `python_code_generator.py`:

```python
# Configuration
OLLAMA_MODEL = "mixtral:8x7b-instruct-v0.1-q6_K"  # Change to your preferred model
DEFAULT_OUTPUT_DIR = "./generated_scripts"         # Default output directory
```

## Generated Files

- Scripts are saved with descriptive names based on your request
- Each file includes a timestamp to avoid conflicts
- Files include proper Python headers and documentation
- All generated code is ready to run

## Output Structure

```
generated_scripts/
├── hello_world_20250101_120000.py
├── calculator_20250101_120030.py
├── file_organizer_20250101_120100.py
└── ...
```

## Troubleshooting

**"Ollama not found" error**:
- Make sure Ollama is installed and in your PATH
- Try running `ollama --version` to verify installation
- For immediate testing without Ollama: `python3 demo_generator.py`

**Comprehensive validation not working**:
- ✅ **All tools are integrated**: No external installations required
- ✅ **Automatic fallback**: If any tool fails, basic validation continues
- ⚠️  **Large integrated_tools directory**: The tools are embedded for reliability
- 🔧 **Memory usage**: Validation uses more memory but ensures quality

**Model taking a long time to respond**:
- ✅ **FIXED**: No more automatic timeouts! The script waits as long as needed
- ✅ **NEW**: Real-time thinking indicator shows the model is working
- ✅ **NEW**: Press Ctrl+C anytime to interrupt if needed
- The script now provides clear feedback during long operations
- Complex requests may take several minutes - this is normal!

**Validation taking time**:
- 🔍 **Comprehensive analysis**: 10 tools analyze your code thoroughly
- ⚡ **Worth the wait**: Quality guarantees are worth a few extra seconds
- 📊 **Detailed feedback**: You get complete analysis results
- 🚀 **One-time cost**: Validation happens once per generation

**Code extraction issues**:
- The tool tries to extract Python code from AI responses
- If extraction fails, check the raw response for formatting issues
- ✅ **Improved extraction**: Better handling of various AI response formats

## Key Features of the Timeout Fix

🚀 **No Hard Timeouts**: The script will wait indefinitely for model responses, preventing premature "timeout" errors.

🧠 **Intelligent Progress Feedback**: 
- Animated "Thinking..." indicator shows the model is actively working
- Clear messaging about what's happening and what you can do

⚡ **User Control**: 
- Press Ctrl+C anytime to interrupt a long-running request
- No more being stuck waiting for arbitrary timeout periods

🔧 **Robust Error Handling**: 
- Proper cleanup of processes and threads
- Clear error messages with actionable guidance
- Graceful handling of all edge cases

## Architecture

The tool consists of several key components:

1. **PythonCodeGenerator**: Main class that handles AI interaction and file operations
2. **Interactive Loop**: CLI interface for user interaction
3. **Code Extraction**: Smart parsing of AI responses to extract clean Python code
4. **File Management**: Automatic naming and saving of generated scripts

## Extending the Tool

You can extend the functionality by:

1. **Adding new models**: Change the `OLLAMA_MODEL` configuration
2. **Custom prompts**: Modify the prompt template in `process_request()`
3. **Output formats**: Add support for additional file formats
4. **Preprocessing**: Add request preprocessing for better AI responses

## Files in this Repository

- `python_code_generator.py` - Main interactive script
- `demo_generator.py` - Demo with mock responses
- `test_generator.py` - Unit tests for core functionality
- Other `*.py` files - Legacy affirmation generation scripts

## Migration from Legacy Scripts

This new tool replaces the various affirmation-specific generators with a flexible, general-purpose Python code generator that can create any type of script based on natural language requests.