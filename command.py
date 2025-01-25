class Command:
    def execute(self):
        raise NotImplementedError("This method should be implemented by subclasses")

class QueryModelCommand(Command):
    def __init__(self, model, prompt):
        self.model = model
        self.prompt = prompt

    def execute(self):
        return self.model.get_response(self.prompt)
