import os
from colorama import init, Fore

init(autoreset=True)  # Initialize colorama for Windows

# Function to list all .py files in the directory
def list_py_files(directory):
    py_files = [file for file in os.listdir(directory) if file.endswith('.py')]
    return py_files

# Function to execute the selected Python file
def execute_file(file_name):
    try:
        with open(file_name, 'r') as file:
            code = file.read()
            exec(code)
    except FileNotFoundError:
        print(Fore.RED + "File not found.")
    except Exception as e:
        print(Fore.RED + "Error executing file:", e)

# Main function
def main():
    examples_dir = "examples"
    py_files = list_py_files(examples_dir)

    print("Available Python files to execute:")
    for i, file in enumerate(py_files):
        print(f"{i+1}. {file}")

    try:
        choice = int(input("\nWhich file do you want to execute? (Enter number): "))
        if 1 <= choice <= len(py_files):
            selected_file = os.path.join(examples_dir, py_files[choice - 1])
            print(Fore.GREEN + f"Executing '{selected_file}'...")
            execute_file(selected_file)
        else:
            print(Fore.RED + "Invalid choice.")
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
