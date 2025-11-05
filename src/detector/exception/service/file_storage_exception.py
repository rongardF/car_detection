

class FileStorageException(Exception):
    pass


class FileNotFound(FileStorageException):
    pass


class FileStoringFailed(FileStorageException):
    pass


class FileFetchingFailed(FileStorageException):
    pass

class FileDeletionFailed(FileStorageException):
    pass