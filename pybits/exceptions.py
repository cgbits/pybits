class ComparisonBaseError(Exception):
    def __init__(self, message: str, depth: int = 0) -> None:
        self.depth: int = depth

        super().__init__(message)


class ComparisonError(ComparisonBaseError):
    pass


class ComparisonErrorInfo(ComparisonBaseError):
    pass
