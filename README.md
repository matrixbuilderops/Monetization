# Python Code Generator

An interactive tool that uses your local AI model (Ollama) to generate Python scripts based on natural language requests.

## 🆕 NEW: Seamless Generator (Recommended)

The **seamless generator** eliminates the multi-line mode prompts that were causing workflow interruptions. Now you can paste ANY content (single or multi-line) and get ONE Python script immediately!

### Quick Start with Seamless Generator

```bash
python3 python_code_generator_seamless.py
```

**Key Benefits:**
- ✅ **No multi-line mode prompts** - paste anything and go!
- ✅ **Handles any input size** - from simple commands to complex data structures
- ✅ **Always generates ONE unified script** per request
- ✅ **Command-agnostic** - no assumptions about your intent
- ✅ **Same Ollama integration** as before, but better UX

### Example Usage

**Old way (with unwanted prompts):**
```
> CATS = {
(multi-line mode) > ...
(multi-line mode) > ...
(multi-line mode) > ... 
```

**New seamless way:**
```
> [paste your entire request]
🎯 Processing request: CATS = {...
✅ Generated Python script: cats_20250803_123456.py
```

## Features

- **Interactive CLI Interface**: Talk to your AI model using natural language
- **Custom Output Directories**: Save generated scripts to any folder you choose
- **Smart Code Extraction**: Automatically extracts clean Python code from AI responses
- **Automatic File Naming**: Generates meaningful filenames based on your requests
- **Code Preview**: Shows a preview of generated code before saving
- **Multiple Format Support**: Clean Python files with proper headers and comments

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

**Seamless Generator (Recommended):**
```bash
python3 python_code_generator_seamless.py
```

**Original Generator:**
```bash
python3 python_code_generator.py
```

**Enhanced Generator:**
```bash
python3 python_code_generator_enhanced.py
```

2. **Make Requests**: Tell the AI what Python script you want:
   ```
   What Python script would you like me to generate? > make a hello world program
   What Python script would you like me to generate? > create a calculator that can do basic math
   What Python script would you like me to generate? > generate a file organizer script
   ```

3. **Set Custom Output Directory** (optional):
   ```
   What Python script would you like me to generate? > set output /path/to/my/scripts
   ```

4. **Exit**:
   ```
   What Python script would you like me to generate? > quit
   ```

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

## Testing and Demos

**Run All Tests:**
```bash
python3 test_seamless_generator.py
```

**Interactive Demo (No Ollama Required):**
```bash
python3 demo_seamless_interactive.py
```

**Comparison Demo:**
```bash
python3 demo_seamless_vs_enhanced.py
```

## Files in this Repository

- `python_code_generator_seamless.py` - **NEW: Recommended seamless generator**
- `python_code_generator.py` - Original interactive script
- `python_code_generator_enhanced.py` - Enhanced version with multi-line support
- `test_seamless_generator.py` - Unit tests for seamless generator
- `demo_seamless_interactive.py` - Interactive demo with mock responses
- `demo_seamless_vs_enhanced.py` - Comparison demo
- Other `*.py` files - Legacy affirmation generation scripts

## Migration to Seamless Generator

If you're experiencing issues with multi-line mode prompts like:
```
(multi-line mode) > ...
(multi-line mode) > ...
```

**Solution:** Use the new seamless generator:
```bash
python3 python_code_generator_seamless.py
```

The seamless generator provides the same functionality but eliminates the frustrating multi-line mode interface.

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

**Model taking a long time to respond**:
- ✅ **FIXED**: No more automatic timeouts! The script waits as long as needed
- ✅ **NEW**: Real-time thinking indicator shows the model is working
- ✅ **NEW**: Press Ctrl+C anytime to interrupt if needed
- The script now provides clear feedback during long operations
- Complex requests may take several minutes - this is normal!

**Code extraction issues**:
- The tool tries to extract Python code from AI responses
- If extraction fails, check the raw response for formatting issues

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

- `python_code_generator_seamless.py` - **NEW: Recommended seamless generator**
- `python_code_generator.py` - Original interactive script
- `python_code_generator_enhanced.py` - Enhanced version with multi-line support
- `test_seamless_generator.py` - Unit tests for seamless generator
- `demo_seamless_interactive.py` - Interactive demo with mock responses
- `demo_seamless_vs_enhanced.py` - Comparison demo
- Other `*.py` files - Legacy affirmation generation scripts

## Migration from Legacy Scripts

This new tool replaces the various affirmation-specific generators with a flexible, general-purpose Python code generator that can create any type of script based on natural language requests.