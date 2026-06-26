"""Base tool abstractions and shared logic."""
class BaseTool:
    name: str = "base_tool"
    description: str = "Base tool"

    def run(self, *args, **kwargs):
        raise NotImplementedError