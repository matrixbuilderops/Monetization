# Python Code Generator

An interactive tool that uses your local AI model (Ollama) to generate Python scripts based on natural language requests.

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

1. **Start the Interactive Generator**:
   ```bash
   python3 python_code_generator.py
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

**"Model call timed out"**:
- The model might be taking too long to respond
- Try a simpler request or check if Ollama is running properly

**Code extraction issues**:
- The tool tries to extract Python code from AI responses
- If extraction fails, check the raw response for formatting issues

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