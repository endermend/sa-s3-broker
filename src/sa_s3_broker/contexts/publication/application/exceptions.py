from sa_s3_broker.shared.application.exceptions import ApplicationError


class InvalidCredentialsError(ApplicationError):
    """Неверная топик либо пароль."""


class InvalidTopicError(ApplicationError):
    """Топика не существует."""

class InvalidPublicationError(ApplicationError):
    """Публикации не существует."""