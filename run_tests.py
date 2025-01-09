import subprocess
import sys
import os
from datetime import datetime
import re


# ANSI Color codes
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def create_section_header(title, width=80):
    """Create a formatted section header"""
    return f"\n{Colors.BOLD}{'=' * width}\n{title}\n{'=' * width}{Colors.RESET}\n"


def run_command(command, description):
    """Run a command and return its output with colors preserved"""
    print(f"Running {description}...")
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    env["FORCE_COLOR"] = "1"  # Force color output for pytest

    # Run command and capture output
    process = subprocess.run(
        command,
        shell=True,
        text=True,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    output = process.stdout + process.stderr
    return output, process.returncode


def format_timestamp():
    """Create a formatted timestamp"""
    return datetime.now().strftime("%Y-%m-%d_%H-%M")


def write_results_file(results, filename):
    """Write test results to file"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(results)


def colorize_test_status(output):
    """Add colors to test status words if not already colored"""
    patterns = [
        (r'\bPASSED\b(?!\[)', f"{Colors.GREEN}PASSED{Colors.RESET}"),
        (r'\bFAILED\b(?!\[)', f"{Colors.RED}FAILED{Colors.RESET}"),
        (r'\bSKIPPED\b(?!\[)', f"{Colors.YELLOW}SKIPPED{Colors.RESET}"),
        (r'\bERROR\b(?!\[)', f"{Colors.RED}ERROR{Colors.RESET}")
    ]

    for pattern, replacement in patterns:
        output = re.sub(pattern, replacement, output)
    return output


def main():
    timestamp = format_timestamp()
    results_file = f"test_results_{timestamp}.txt"
    all_results = []

    # Add test run header with timestamp
    all_results.append(f"{Colors.BOLD}Test Run: {timestamp}{Colors.RESET}\n")

    # Generate test files
    all_results.append(create_section_header("Test Generation"))
    gen_output, gen_code = run_command("python generate_tests.py", "test generation")
    all_results.append(gen_output)

    # Run pytest
    all_results.append(create_section_header("PyTest Results"))
    pytest_output, pytest_code = run_command("pytest tests/ -v --color=yes", "pytest tests")
    all_results.append(colorize_test_status(pytest_output))

    # Run behave
    all_results.append(create_section_header("Behave Results"))
    behave_output, behave_code = run_command("behave features/ -f pretty --color", "behave tests")
    all_results.append(colorize_test_status(behave_output))

    # Combine all results
    final_results = "\n".join(all_results)

    # Write to file
    write_results_file(final_results, results_file)

    # Print summary to console
    print(f"\nTest execution completed!")
    print(f"Results have been saved to: {results_file}")

    # Return appropriate exit code
    if any([gen_code, pytest_code, behave_code]):
        sys.exit(1)


if __name__ == "__main__":
    main()