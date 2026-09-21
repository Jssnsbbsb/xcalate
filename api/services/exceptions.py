class SarvamError(Exception):
    """Base exception for Sarvam API failures."""
    def __init__(self, message, code="SARVAM_ERROR", status=500):
        self.message = message
        self.code = code
        self.status = status
        super().__init__(message)


class SarvamAuthError(SarvamError):
    def __init__(self, message="Invalid Sarvam API key"):
        super().__init__(message, code="UNAUTHORIZED", status=401)


class SarvamRateLimitError(SarvamError):
    def __init__(self, message="Sarvam rate limit exceeded"):
        super().__init__(message, code="RATE_LIMITED", status=429)


class SarvamTimeoutError(SarvamError):
    def __init__(self, message="Sarvam request timed out"):
        super().__init__(message, code="SARVAM_TIMEOUT", status=504)


class UnsupportedLanguageError(SarvamError):
    def __init__(self, lang):
        super().__init__(
            f"Language '{lang}' is not supported",
            code="UNSUPPORTED_LANGUAGE",
            status=422,
        )