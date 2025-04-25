import typing

class ToolDefinition:
    def __init__(self, name: str, description: str, parameters: dict, function_to_call: typing.Callable):
        self.name = name
        self.description = description
        self.parameters = parameters 
        self.function = function_to_call

    def get_api_description(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            }
        } 