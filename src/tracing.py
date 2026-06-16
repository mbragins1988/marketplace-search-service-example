import contextvars
import logging
import uuid

trace_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "trace_id", default=""
)


def get_trace_id() -> str:
    return trace_id_var.get()


def set_trace_id(value: str) -> None:
    trace_id_var.set(value)


def new_trace_id() -> str:
    return str(uuid.uuid4())


class TraceIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = get_trace_id()
        return True


def setup_logging() -> None:
    handler = logging.StreamHandler()
    handler.addFilter(TraceIdFilter())
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(name)s %(levelname)s [%(trace_id)s] %(message)s"
        )
    )
    logging.root.setLevel(logging.INFO)
    logging.root.addHandler(handler)
