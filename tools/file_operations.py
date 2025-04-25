import os
import json


def read_file_from_path(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File not found at path: {file_path}")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file '{file_path}': {e}")


def list_files_from_path(path: str = ".") -> str:
    try:
        file_list = []
        for root, dirs, files in os.walk(path):
            if root == path:
                for d in dirs:
                    file_list.append(f"{d}/")
                for f in files:
                    file_list.append(f)
            else:
                rel_path = os.path.relpath(root, path)
                for d in dirs:
                    file_list.append(f"{rel_path}/{d}/")
                for f in files:
                    file_list.append(f"{rel_path}/{f}")
        return json.dumps(file_list)
    except Exception as e:
        raise Exception(f"An error occurred while listing files at path '{path}': {e}")

def create_new_file(file_path: str, content: str) -> str:
    dir_path = os.path.dirname(file_path)
    if dir_path and dir_path != ".":
        os.makedirs(dir_path, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    return f"Successfully created file {file_path}"


def edit_file(path: str, old_str: str, new_str: str) -> str:
    if path == "" or old_str == new_str:
        raise ValueError("Invalid input parameters")
    
    try:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                old_content = f.read()
            
            if old_str == "":
                raise FileNotFoundError() # Treat empty old_str as file not found for creation logic
                
            new_content = old_content.replace(old_str, new_str)
            
            if old_content == new_content and old_str != "": 
                raise ValueError("old_str not found in file")
                
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            return f"Successfully edited file {path}"
            
        except FileNotFoundError:
            if old_str == "": # If old_str is empty and file not found, create new file
                return create_new_file(path, new_str)
            raise
    except Exception as e:
        raise Exception(f"An error occurred while editing the file '{path}': {e}") 