import os
import glob
import shutil


class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_colored(message, color):
    """Print a message in specified color"""
    print(f"{color}{message}{Colors.RESET}")


def cleanup():
    """Clean up all generated files and directories while preserving core files"""
    # First, save the content of sensor_steps.py if it exists
    steps_file_path = os.path.join('features', 'steps', 'sensor_steps.py')
    steps_content = None
    if os.path.exists(steps_file_path):
        with open(steps_file_path, 'r') as f:
            steps_content = f.read()

    # List of directories to clean
    dirs_to_clean = ['features', 'tests', '__pycache__']

    # List of file patterns to remove
    file_patterns = [
        'test_results_*.txt',  # Test result files
        '*.pyc',  # Python compiled files
        '.coverage',  # Coverage files
        '*.log'  # Log files
    ]

    # List of core files to preserve
    core_files = {
        'aio_interface.py',
        'generate_tests.py',
        'run_tests.py',
        'cleanup.py',
        'view_results.py',
        'requirements.txt',
        'sensors_input.json',
        'README.md'
    }

    print_colored("\nStarting cleanup process...", Colors.BOLD)

    # Clean directories
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print_colored(f"✓ Removed directory: {dir_name}", Colors.GREEN)
            except Exception as e:
                print_colored(f"! Error removing {dir_name}: {e}", Colors.YELLOW)

    # Remove files by pattern
    for pattern in file_patterns:
        for file_path in glob.glob(pattern):
            try:
                os.remove(file_path)
                print_colored(f"✓ Removed file: {file_path}", Colors.GREEN)
            except Exception as e:
                print_colored(f"! Error removing {file_path}: {e}", Colors.YELLOW)

    # Clean up templates directory while preserving template files
    if os.path.exists('templates'):
        for file_name in os.listdir('templates'):
            if file_name.endswith(('.pyc', '.pyo')):
                file_path = os.path.join('templates', file_name)
                try:
                    os.remove(file_path)
                    print_colored(f"✓ Removed file: {file_path}", Colors.GREEN)
                except Exception as e:
                    print_colored(f"! Error removing {file_path}: {e}", Colors.YELLOW)

    # Restore sensor_steps.py if it existed
    if steps_content is not None:
        # Recreate the directory structure
        os.makedirs(os.path.join('features', 'steps'), exist_ok=True)
        # Restore the file
        with open(steps_file_path, 'w') as f:
            f.write(steps_content)
        print_colored(f"✓ Restored core file: features/steps/sensor_steps.py", Colors.GREEN)

    print_colored("\nCleanup completed!", Colors.BOLD)
    print_colored("\nPreserved core framework files:", Colors.BOLD)
    for file in sorted(core_files):
        if os.path.exists(file):
            print_colored(f"- {file}", Colors.GREEN)
    print_colored(f"- features/steps/sensor_steps.py", Colors.GREEN)


if __name__ == "__main__":
    try:
        user_input = input("This will remove all generated test files and directories. Continue? (y/n): ")
        if user_input.lower() == 'y':
            cleanup()
        else:
            print_colored("Cleanup cancelled.", Colors.YELLOW)
    except KeyboardInterrupt:
        print_colored("\nCleanup cancelled.", Colors.YELLOW)