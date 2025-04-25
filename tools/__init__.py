from .tool_definition import ToolDefinition
from .file_operations import read_file_from_path, list_files_from_path, edit_file

read_file_tool = ToolDefinition(
    name="read_file",
    description="Read the contents of a file",
    parameters={
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the file to read"
            }
        },
        "required": ["file_path"]
    },
    function_to_call=read_file_from_path
)

list_files_tool = ToolDefinition(
    name="list_files",
    description="List files and directories at a given path. If no path is provided, lists files in the current directory.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string", 
                "description": "Optional relative path to list files from. Defaults to current directory if not provided."
            }
        }
    },
    function_to_call=list_files_from_path
)

edit_file_tool = ToolDefinition(
    name="edit_file",
    description="Make edits to a text file. Replaces 'old_str' with 'new_str' in the given file. 'old_str' and 'new_str' MUST be different from each other. If the file specified with path doesn't exist, it will be created.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The path to the file"
            },
            "old_str": {
                "type": "string",
                "description": "Text to search for - must match exactly and must only have one match exactly"
            },
            "new_str": {
                "type": "string",
                "description": "Text to replace old_str with"
            }
        },
        "required": ["path", "old_str", "new_str"]
    },
    function_to_call=edit_file
) 