# 自定义异常信息


class DomainError(Exception):
    """业务规则失败。"""


class NotFoundError(DomainError):
    pass


class ConflictError(DomainError):
    pass


class ValidationError(DomainError):
    pass
