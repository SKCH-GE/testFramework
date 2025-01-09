import sys
import glob
import os

def clear_console():
    """Clear the console based on the operating system"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_latest_results_file():
    """Get the most recent results file"""
    files = glob.glob("test_results_*.txt")
    if not files:
        return None
    return max(files, key=os.path.getctime)


def print_file_contents(filename):
    """Print the contents of the file to console"""
    with open(filename, 'r', encoding='utf-8') as f:
        print(f.read())


if __name__ == "__main__":
    clear_console()
    if len(sys.argv) > 1:
        # If filename provided as argument
        filename = sys.argv[1]
    else:
        # Get latest results file
        filename = get_latest_results_file()

    if not filename:
        print("No test results file found!")
        sys.exit(1)

    print_file_contents(filename)