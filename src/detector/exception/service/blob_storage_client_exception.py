

class BlobStorageClientException(Exception):
    pass


class UploadFailed(BlobStorageClientException):
    pass


class DownloadFailed(BlobStorageClientException):
    pass


class DeleteFailed(BlobStorageClientException):
    pass