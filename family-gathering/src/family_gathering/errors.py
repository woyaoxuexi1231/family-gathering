"""领域错误 — API 层映射为 HTTP 状态码。"""


class DomainError(Exception):
    """业务规则失败。"""


class NotFoundError(DomainError):
    pass


class ConflictError(DomainError):
    pass


class ValidationError(DomainError):
    pass
