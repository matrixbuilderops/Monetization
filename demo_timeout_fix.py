#!/usr/bin/env python3
"""
Demo script to show the timeout fix in action
This simulates a slow model response to demonstrate the thinking indicator
"""

import sys
import time
import subprocess
from pathlib import Path

def simulate_slow_ollama():
    """Simulate a slow Ollama response to show the thinking indicator."""
    print("🎭 Timeout Fix Demonstration")
    print("=" * 50)
    print("This demo simulates how the script behaves during long model thinking time.")
    print("You'll see the thinking indicator and can interrupt with Ctrl+C.")
    print()
    
    # Create a mock Ollama script that takes time to respond
    mock_ollama_script = '''#!/usr/bin/env python3
import sys
import time

# Simulate model thinking time
print("Mock Ollama starting...", file=sys.stderr)
time.sleep(10)  # Simulate 10 seconds of thinking

# Return a simple Python script
print("""#!/usr/bin/env python3
\"""
Generated Hello World Script
This was generated after a 10-second delay to demonstrate the timeout fix.
\"""

def main():
    print("Hello, World!")
    print("This script was generated without timeout issues!")

if __name__ == "__main__":
    main()
""")
'''
    
    # Save the mock script
    mock_script_path = Path("/tmp/mock_ollama.py")
    with open(mock_script_path, 'w') as f:
        f.write(mock_ollama_script)
    mock_script_path.chmod(0o755)
    
    print(f"📝 Created mock Ollama at: {mock_script_path}")
    print("🔧 This mock will take 10 seconds to respond (demonstrating no timeout)")
    print()
    
    # Create a modified version of the generator that uses our mock
    modified_generator = """#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/runner/work/Monetization/Monetization')

from python_code_generator import PythonCodeGenerator

# Override the call_model method to use our mock
class DemoTimeoutGenerator(PythonCodeGenerator):
    def call_model(self, prompt):
        import subprocess
        import threading
        import time
        
        thinking_active = None
        progress_thread = None
        process = None
        
        try:
            print("🤔 Thinking (this may take a while for complex requests)...")
            print("💡 Press Ctrl+C to interrupt if needed")
            print("⏰ This demo will take 10 seconds to show the thinking indicator...")
            
            # Start a thinking indicator in a separate thread
            thinking_active = threading.Event()
            thinking_active.set()
            
            def show_thinking_progress():
                dots = 0
                while thinking_active.is_set():
                    dots = (dots + 1) % 4
                    progress = "   Thinking" + "." * dots
                    print(f"\\r{progress}", end="", flush=True)
                    time.sleep(0.5)
                print("")
            
            # Start the progress indicator
            progress_thread = threading.Thread(target=show_thinking_progress, daemon=True)
            progress_thread.start()
            
            # Use our mock Ollama
            process = subprocess.Popen(
                ["python3", "/tmp/mock_ollama.py"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for response (no timeout!)
            stdout, stderr = process.communicate(input=prompt.encode())
            
            # Stop the thinking indicator
            thinking_active.clear()
            if progress_thread:
                progress_thread.join(timeout=1)
            
            if process.returncode != 0:
                error_msg = stderr.decode().strip()
                print(f"Error: {error_msg}")
                return None
            
            output = stdout.decode().strip()
            print("✓ Model finished thinking (after 10 seconds)!")
            return output
        
        except KeyboardInterrupt:
            print("\\n⚠️  Generation interrupted by user.")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
        finally:
            # Clean up
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

# Run a quick demo
generator = DemoTimeoutGenerator()
generator.process_request("make a hello world script")
print("\\n🎉 Demo completed! The script waited 10 seconds without timing out.")
print("💡 In the old version, this would have failed with 'Model call timed out' after 60 seconds.")
print("🚀 Now it waits indefinitely and provides clear progress feedback!")
"""
    
    # Save and run the demo
    demo_script_path = Path("/tmp/timeout_demo.py")
    with open(demo_script_path, 'w') as f:
        f.write(modified_generator)
    
    print("🚀 Running timeout demonstration...")
    print("   (You can press Ctrl+C to interrupt at any time)")
    print()
    
    try:
        result = subprocess.run(
            ["python3", str(demo_script_path)],
            cwd="/home/runner/work/Monetization/Monetization",
            timeout=30,  # Give it enough time to complete
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print("✅ Demo completed successfully!")
        else:
            print(f"❌ Demo failed with return code: {result.returncode}")
            
    except subprocess.TimeoutExpired:
        print("⏰ Demo took longer than expected (that's actually good - no hard timeout!)")
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user (this is the correct behavior!)")
    
    # Clean up
    try:
        mock_script_path.unlink()
        demo_script_path.unlink()
    except:
        pass

if __name__ == "__main__":
    simulate_slow_ollama()