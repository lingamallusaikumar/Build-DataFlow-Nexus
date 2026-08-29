import time
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

def execute_with_retry(
    func: Callable[..., Any],
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    *args,
    **kwargs
) -> Any:
    """Executes a pipeline task function with exponential backoff retry policy."""
    delay = initial_delay
    last_exception = None

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Attempt {attempt}/{max_retries} executing {func.__name__}")
            return func(*args, **kwargs)
        except Exception as exc:
            last_exception = exc
            logger.warning(f"Attempt {attempt} failed: {exc}")
            if attempt < max_retries:
                time.sleep(delay)
                delay *= backoff_factor

    logger.error(f"Execution failed after {max_retries} attempts.")
    raise last_exception
