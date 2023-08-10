import os
import stat

class SimpleFileSystem:
    def __init__(self):
        self.root = {}  # Dictionary to store the root directory
        self.current_directory = self.root  # Pointer to the current directory

    def create_file(self, filename, content=""):
        if filename not in self.current_directory:
            self.current_directory[filename] = content
            print(f"File '{filename}' created successfully.")
        else:
            print(f"File '{filename}' already exists.")

    def read_file(self, filename):
        if filename in self.current_directory:
            return self.current_directory[filename]
        else:
            print(f"File '{filename}' does not exist.")
            return None

    def create_directory(self, dirname):
        if dirname not in self.current_directory:
            self.current_directory[dirname] = {}
            print(f"Directory '{dirname}' created successfully.")
        else:
            print(f"Directory '{dirname}' already exists.")

    def list_directory(self):
        contents = list(self.current_directory.keys())
        print(f"Contents of '{self.get_current_path()}': {contents}")

    def change_directory(self, dirname):
        if dirname in self.current_directory and isinstance(self.current_directory[dirname], dict):
            self.current_directory = self.current_directory[dirname]
            print(f"Changed directory to '{self.get_current_path()}'.")
        else:
            print(f"Directory '{dirname}' does not exist.")

    def delete_file(self, filename):
        if filename in self.current_directory:
            del self.current_directory[filename]
            print(f"File '{filename}' deleted successfully.")
        else:
            print(f"File '{filename}' does not exist.")

    def write_to_file(self, filename, content):
        if filename in self.current_directory:
            self.current_directory[filename] = content
            print(f"Content written to file '{filename}' successfully.")
        else:
            print(f"File '{filename}' does not exist.")

    def set_file_permissions(self, filename, mode):
        if filename in self.current_directory:
            os.chmod(filename, mode)
            print(f"File permissions of '{filename}' set to {oct(stat.S_IMODE(os.stat(filename).st_mode))}.")
        else:
            print(f"File '{filename}' does not exist.")

    def get_current_path(self):
        path = []
        current = self.current_directory
        while current != self.root:
            parent_dir = [key for key, value in self.root.items() if value == current][0]
            path.append(parent_dir)
            current = self.root
        return '/' + '/'.join(reversed(path))

import unittest

class TestSimpleFileSystem(unittest.TestCase):
    def setUp(self):
        self.file_system = SimpleFileSystem()

    def test_create_file(self):
        filename = "test_file.txt"
        content = "This is a test file."
        self.file_system.create_file(filename, content)
        self.assertIn(filename, self.file_system.current_directory)
        self.assertEqual(self.file_system.current_directory[filename], content)

        # Test file deletion
        self.file_system.delete_file(filename)
        self.assertNotIn(filename, self.file_system.current_directory)

        # Test writing to file
        content2 = "New content."
        self.file_system.create_file(filename, content)
        self.file_system.write_to_file(filename, content2)
        self.assertEqual(self.file_system.current_directory[filename], content2)

if __name__ == "__main__":
    file_system = SimpleFileSystem()

    while True:
        print("Options:")
        print("1. Create File")
        print("2. Read File")
        print("3. Create Directory")
        print("4. List Directory")
        print("5. Change Directory")
        print("6. Delete File")
        print("7. Write to File")
        print("8. Set File Permissions")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            filename = input("Enter the file name to create: ")
            content = input("Enter the content (optional): ")
            file_system.create_file(filename, content)
        elif choice == "2":
            filename = input("Enter the file name to read: ")
            content = file_system.read_file(filename)
            if content:
                print(f"Content of '{filename}': {content}")
        elif choice == "3":
            dirname = input("Enter the directory name to create: ")
            file_system.create_directory(dirname)
        elif choice == "4":
            file_system.list_directory()
        elif choice == "5":
            dirname = input("Enter the directory name to change: ")
            file_system.change_directory(dirname)
        elif choice == "6":
            filename = input("Enter the file name to delete: ")
            file_system.delete_file(filename)
        elif choice == "7":
            filename = input("Enter the file name to write to: ")
            content = input("Enter the content: ")
            file_system.write_to_file(filename, content)
        elif choice == "8":
            filename = input("Enter the file name to set permissions: ")
            mode = int(input("Enter the permissions in octal (e.g., 644): "), 8)
            file_system.set_file_permissions(filename, mode)
        elif choice == "9":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
