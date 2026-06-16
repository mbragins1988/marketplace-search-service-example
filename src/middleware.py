import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from src.tracing import get_trace_id, set_trace_id


class TraceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = request.headers.get("X-Trace-Id") or str(uuid.uuid4())
        set_trace_id(trace_id)
        response = await call_next(request)
        response.headers["X-Trace-Id"] = get_trace_id()
        return response
