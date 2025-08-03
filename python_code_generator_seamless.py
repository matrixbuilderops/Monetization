#!/usr/bin/env python3
"""
Seamless Python Code Generator
Uses local Ollama model to generate Python scripts based on natural language requests.
Designed to handle ANY pasted input (single or multi-line) without multi-line mode prompts.
"""

import os
import subprocess
import sys
import threading
import time
from pathlib import Path
from datetime import datetime

# Configuration
OLLAMA_MODEL = "mixtral:8x7b-instruct-v0.1-q6_K"
DEFAULT_OUTPUT_DIR = "./generated_scripts"

class SeamlessPythonCodeGenerator:
    def __init__(self, model_name=OLLAMA_MODEL):
        self.model_name = model_name
        self.output_dir = Path(DEFAULT_OUTPUT_DIR)
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """Ensure the output directory exists."""
        self.output_dir.mkdir(exist_ok=True, parents=True)
    
    def call_model(self, prompt: str) -> str:
        """Call the Ollama model with a prompt and return the response."""
        thinking_active = None
        progress_thread = None
        process = None
        
        try:
            print("🤔 Thinking (this may take a while for complex requests)...")
            print("💡 Press Ctrl+C to interrupt if needed")
            
            # Start a thinking indicator in a separate thread
            thinking_active = threading.Event()
            thinking_active.set()
            
            def show_thinking_progress():
                """Show progress dots while the model is thinking."""
                dots = 0
                while thinking_active.is_set():
                    dots = (dots + 1) % 4
                    progress = "   Thinking" + "." * dots
                    print(f"\r{progress}", end="", flush=True)
                    time.sleep(0.5)
                print("")  # New line when done
            
            # Start the progress indicator
            progress_thread = threading.Thread(target=show_thinking_progress, daemon=True)
            progress_thread.start()
            
            # Start the subprocess without timeout
            process = subprocess.Popen(
                ["ollama", "run", self.model_name],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Send the prompt and wait for response
            stdout, stderr = process.communicate(input=prompt.encode())
            
            # Stop the thinking indicator
            thinking_active.clear()
            if progress_thread:
                progress_thread.join(timeout=1)
            
            if process.returncode != 0:
                error_msg = stderr.decode().strip()
                print(f"Error calling model: {error_msg}")
                return None
            
            output = stdout.decode().strip()
            print("✓ Model finished thinking!")
            return output
        
        except KeyboardInterrupt:
            print("\n⚠️  Generation interrupted by user.")
            return None
        except FileNotFoundError:
            print("Error: Ollama not found. Please ensure Ollama is installed and in your PATH.")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
        finally:
            # Always clean up the thinking indicator and process
            if thinking_active:
                thinking_active.clear()
            if progress_thread:
                progress_thread.join(timeout=1)
            if process:
                try:
                    if process.poll() is None:  # Process is still running
                        process.terminate()
                        process.wait(timeout=5)
                except:
                    try:
                        process.kill()
                    except:
                        pass
    
    def extract_python_code(self, response: str) -> str:
        """Extract Python code from the model response."""
        # Look for code blocks marked with ```python or ```
        lines = response.split('\n')
        code_lines = []
        in_code_block = False
        
        for line in lines:
            if line.strip().startswith('```python') or line.strip().startswith('```'):
                if in_code_block:
                    break  # End of code block
                in_code_block = True
                continue
            
            if in_code_block:
                if line.strip() == '```':
                    break
                code_lines.append(line)
        
        # If no code blocks found, treat the entire response as code
        if not code_lines:
            return response.strip()
        
        return '\n'.join(code_lines).strip()
    
    def generate_filename(self, user_request: str) -> str:
        """Generate a filename based on the user request."""
        # Extract key words from the request - handle both single line and multi-line
        first_line = user_request.split('\n')[0]  # Use first line for filename
        words = first_line.lower().split()
        filename_words = []
        
        # Skip common words and focus on meaningful terms
        skip_words = {'make', 'create', 'generate', 'write', 'a', 'an', 'the', 'file', 'script', 'program', 'build'}
        
        for word in words:
            clean_word = ''.join(c for c in word if c.isalnum())
            if clean_word and clean_word not in skip_words:
                filename_words.append(clean_word)
        
        if not filename_words:
            filename_words = ['script']
        
        # Use first few words and add timestamp
        base_name = '_'.join(filename_words[:3])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_name}_{timestamp}.py"
    
    def save_code(self, code: str, filename: str, output_dir: Path = None) -> bool:
        """Save the generated code to a file."""
        if output_dir is None:
            output_dir = self.output_dir
        
        try:
            output_path = output_dir / filename
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
        self.ensure_output_dir()
        print(f"Output directory set to: {self.output_dir.absolute()}")
    
    def process_request(self, user_request: str, output_dir: Path = None):
        """Process a user request to generate Python code."""
        # Clean up the request - remove empty lines at start/end
        user_request = user_request.strip()
        
        print(f"\n🎯 Processing request: {user_request[:100]}{'...' if len(user_request) > 100 else ''}")
        
        # Create a generic prompt that works for any command or code block
        # Emphasize ONE unified script regardless of input complexity
        prompt = f"""Generate ONE complete Python script based on this request: "{user_request}"

IMPORTANT: Create exactly ONE unified script that handles the entire request, regardless of how complex or multi-part the input may be. Do not split into multiple scripts, files, or separate components.

Please provide only the Python code without any explanations or markdown formatting.
Make sure the code is complete, well-commented, and ready to run as a single script.
Include necessary imports and proper error handling where appropriate.

Request: {user_request}

Python code:"""
        
        # Call the model (this now provides its own progress feedback)
        response = self.call_model(prompt)
        if not response:
            print("❌ Failed to generate code.")
            return
        
        # Extract Python code from response
        code = self.extract_python_code(response)
        if not code:
            print("❌ Could not extract Python code from model response.")
            print("Raw response:", response[:200] + "..." if len(response) > 200 else response)
            return
        
        # Generate filename
        filename = self.generate_filename(user_request)
        
        # Save the code
        if self.save_code(code, filename, output_dir):
            print(f"🎉 Generated Python script: {filename}")
            
            # Show a preview of the code
            print("\n📄 Code preview:")
            print("-" * 50)
            preview_lines = code.split('\n')[:15]
            for i, line in enumerate(preview_lines, 1):
                print(f"{i:2d}: {line}")
            if len(code.split('\n')) > 15:
                print("    ... (showing first 15 lines)")
            print("-" * 50)

def get_multiline_input(prompt_text="Enter your request (paste anything, press Ctrl+D or type 'END' when done):\n"):
    """
    Get multi-line input from user. Handles pasted content seamlessly.
    Users can paste any content and it will be processed as one request.
    """
    print(prompt_text)
    lines = []
    
    try:
        while True:
            try:
                line = input()
                # Check if user typed 'END' on its own line to finish
                if line.strip().upper() == 'END':
                    break
                lines.append(line)
            except EOFError:
                # Ctrl+D pressed or end of pasted content
                break
    except KeyboardInterrupt:
        print("\n❌ Input cancelled.")
        return None
    
    result = '\n'.join(lines).strip()
    if not result:
        return None
    
    return result

def main():
    """Main interactive loop."""
    generator = SeamlessPythonCodeGenerator()
    
    print("🐍 Seamless Python Code Generator")
    print("=" * 60)
    print("This tool uses your local AI model to generate Python scripts based on your requests.")
    print("\n🎯 KEY FEATURES:")
    print("  ✓ Paste ANY command or code block - single or multi-line")  
    print("  ✓ Always generates ONE unified script per request")
    print("  ✓ No multi-line mode prompts - just paste and go!")
    print("  ✓ Handles simple commands and complex data structures equally")
    print("  ✓ Command-agnostic - no assumptions about your intent")
    print("\nExamples:")
    print("  - 'make a hello world program'")
    print("  - Paste large data structures or complex multi-line commands")
    print("  - 'create a file organizer script'")
    print("  - Any command/code block → ONE complete Python script")
    print("")
    print("Commands:")
    print("  'set output <directory>' - Change output directory")
    print("  'quit' or 'exit' - Exit the program")
    print("=" * 60)
    print(f"Current output directory: {generator.output_dir.absolute()}")
    print("")
    
    while True:
        try:
            print("🔥 What would you like me to create? (Type your request or paste multi-line content)")
            print("   💡 For multi-line: just paste your content and press Ctrl+D or type 'END' on a new line")
            
            # First, try to get a single line input
            try:
                user_input = input("> ").strip()
            except EOFError:
                print("\nGoodbye! 👋")
                break
            
            if not user_input:
                continue
                
            # Handle special commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break
            
            if user_input.lower().startswith('set output '):
                new_dir = user_input[11:].strip()
                if new_dir:
                    generator.set_output_directory(new_dir)
                else:
                    print("Please specify a directory path.")
                continue
            
            # Check if user wants to enter multi-line mode explicitly
            if user_input.lower() in ['multi', 'multiline', 'paste']:
                user_input = get_multiline_input()
                if user_input is None:
                    continue
            
            # Process the request
            generator.process_request(user_input)
            print("")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

if __name__ == "__main__":
    main()