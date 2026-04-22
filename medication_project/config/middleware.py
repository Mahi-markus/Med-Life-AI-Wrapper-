import time
import logging

logger = logging.getLogger("api_usage")

class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.monotonic()
        response = self.get_response(request)
        elapsed_ms = round((time.monotonic() - start) * 1000, 1)

        user = "anonymous"
        if hasattr(request, "user") and request.user.is_authenticated:
            user = request.user.username

        logger.info(
            "API usage: %s %s status=%s user=%s duration=%sms",
            request.method,
            request.get_full_path(),
            response.status_code,
            user,
            elapsed_ms,
        )

        return response