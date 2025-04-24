from contextvars import ContextVar
from uuid import uuid4

TX_ID = ContextVar("TX_ID")  # type: ignore


def make_tx_id():
    """Generate and set a new transaction ID in the context variable."""
    TX_ID.set(uuid4().hex)


def get_tx_id():
    """Retrieve the current transaction ID from the context variable."""
    return TX_ID.get()
