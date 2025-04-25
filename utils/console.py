import sys

class Console:
    RED = '[91m'
    BLUE = '[94m'
    YELLOW = '[93m'
    MAGENTA = '[95m'
    ENDC = '[0m'

    @staticmethod
    def error(message: str):
        print(f"{Console.RED}Error: {message}{Console.ENDC}", file=sys.stderr)

    @staticmethod
    def user(message: str):
        return input(f"{Console.BLUE}You{Console.ENDC}: {message}")

    @staticmethod
    def assistant(model_name: str, message: str):
        print(f"{Console.YELLOW}{model_name}{Console.ENDC}: {message}")
        
    @staticmethod
    def tool_call(tool_name: str, arguments: str):
        print(f"{Console.MAGENTA}Tool: {tool_name}({arguments}){Console.ENDC}")

    @staticmethod
    def info(message: str):
        print(message) # Simple print for general info for now 