from abc import ABC, abstractmethod

# local imports
from ...model.dto import BlobFileContainerDto


class AbstractBlobStorageClient(ABC):

    @abstractmethod
    async def upload(self, blob: BlobFileContainerDto) -> None:
        """
        Upload blob file to storage account.

        :param blob: Blob file to be uploaded
        :type blob: BlobFileContainerDto
        :raises UploadFailed: If any issues with uploading the blob file
        """
        raise NotImplementedError()
    
    @abstractmethod
    async def download(self, path: str) -> BlobFileContainerDto:
        """
        Download blob file from storage account.

        :param path: Blob file path in storage account
        :type path: str
        :raises DownloadFailed: If any issues with downloading the blob file
        :return: Downloaded blob file
        :rtype: BlobFileContainerDto
        """
        raise NotImplementedError()
    
    @abstractmethod
    async def delete(self, path: str) -> bool:
        """
        Delete blob file in storage account.

        :param path: Path to file in storage account
        :type path: str
        :raises DeleteFailed: If any issues with deleting the blob file
        :return: 'True' if success
        :rtype: bool
        """
        raise NotImplementedError()