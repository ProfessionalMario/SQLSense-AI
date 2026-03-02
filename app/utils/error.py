# utils/errors.py

class LLMError(Exception):
    """Base class for LLM related errors."""
    pass


class ModelTimeoutError(LLMError):
    """Raised when model inference exceeds allowed time."""
    pass


class InvalidSQLGenerated(LLMError):
    """Raised when generated SQL is invalid or unsafe."""
    pass


class DatabaseExecutionError(Exception):
    """Raised when database execution fails."""
    pass