class TriggerLogic:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "completed": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("BOOLEAN", "INT")
    RETURN_NAMES = ("trigger", "count_input")
    FUNCTION = "process"
    CATEGORY = "utils"

    def process(self, completed):
        # Pass through the signal
        # Output 1: Trigger for Node 2
        # Output 2: Counter Increment (just sending 1 to indicate 'add 1')
        return (completed, 1)
