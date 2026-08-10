class DuplicateEmailError(Exception):
    pass


class DuplicatePhoneError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class UpdateFailedError(Exception):
    pass


class DeletionFailedError(Exception):
    pass
