class GitHubCLIError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class UserNotFoundError(GitHubCLIError):
    def __init__(self, username):
        self.username = username
        super().__init__(f"User not found: {self.username}")

class RateLimitExceededError(GitHubCLIError):
    def __init__(self, reset_time=None):
        message = "Rate limit exceeded. Please try again later."
        if reset_time:
            message += f" Rate limit resets at {reset_time} (timestamp)."
        #on envoie a la classe parente le message d'erreur
        super().__init__(message)
        #on stocke pour information le temps de reset du rate limit
        self.reset_time = reset_time

class AuthenticationError(GitHubCLIError):
    def __init__(self):
        super().__init__("Authentication failed. Please check your token.")  

class APIConnectionError(GitHubCLIError):
    def __init__(self):
        super().__init__("Failed to connect to the GitHub API. Please check your internet connection.")     
         