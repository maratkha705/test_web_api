from amtl_api.adapters.api.config import logger


class ApiBaseException(Exception):
    base_name: str = "ApiBaseException"

    def __init__(
            self,
            message: str = "",
            status_code: int = 500,
            detail: dict | str | list | None = None,
            mime_type: str = "",
            *args,  # noqa
            **kwargs
    ):
        self.status_code = status_code
        self.message = message
        self.detail = detail
        self.mime_type = mime_type
        self.more = kwargs.get("more")
        self.pid = kwargs.get("pid")
        logger.error(f"Exc: {self.base_name} {status_code}: {message} {mime_type}")

    def __repr__(self):
        return f"Msg[{self.base_name}]: {self.message}"


class WrongUrl(ApiBaseException):
    ...
