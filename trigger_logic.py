class TriggerLogic:
    """
    A simple pass-through node that acts as a Logic Gate.
    Useful for forcing execution order or creating 'Any' triggers.
    """
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
    CATEGORY = "automation 101"

    def process(self, completed):
        # Pass through the signal
        # Output 1: Trigger for Node 2
        # Output 2: Counter Increment (just sending 1 to indicate 'add 1')
        return (completed, 1)
