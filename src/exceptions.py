class MissingEnvironmentVariableException(Exception):
    def __init__(self, missing_variable_name):
        self.message = f"Missing {missing_variable_name} environment variable. Be sure to copy a new .env file from .env.example"
        super().__init__(self.message)
