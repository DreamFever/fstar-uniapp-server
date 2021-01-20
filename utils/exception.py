class AccountError(Exception):
    def __init__(self, reason) -> None:
        self.reason = reason

    def __str__(self) -> str:
        return self.reason
