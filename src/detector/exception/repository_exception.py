

# base exception to group and catch all repository related exceptions
class RepositoryException(Exception):
    pass


class NotFoundException(RepositoryException):
    pass


class NotUniqueException(RepositoryException):
    pass


class RestrictionException(RepositoryException):
    pass