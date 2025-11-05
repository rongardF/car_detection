from uuid import UUID
from abc import ABC, abstractmethod

from common.exception.repository_exception import NotFoundException

# local imports

from ...model.dto import FileContainerDto
from ...exception import FileFetchingFailed, FileStoringFailed, FileNotFound, UploadFailed, DownloadFailed


class AbstractFileStorage():
    
    @abstractmethod
    async def store_file(self, account_id: UUID, file: FileContainerDto) -> UUID:
        """
        Persistent storage of a file

        :param account_id: Account ID, each file must be related to account
        :type account_id: UUID
        :param file: File to be stored
        :type file: FileContainerDto
        :raises FileStoringFailed: If any issues with storing the file
        :return: File ID in storage, can be used to fetch it later
        :rtype: UUID
        """
        raise NotImplementedError()

    @abstractmethod
    async def fetch_file(self, account_id: UUID, file_id: UUID) -> FileContainerDto:
        """
        Fetch a file from persistent storage

        :param account_id: Account ID, each file is related to an account
        :type account_id: UUID
        :param file_id: File storage ID
        :type file_id: UUID
        :raises FileNotFound: If no file with such ID exists in storage
        :raises FileFetchingFailed: If any general issues with fetching the file
        :return: File that was fetched
        :rtype: FileContainerDto
        """
        raise NotImplementedError()
    
    @abstractmethod
    async def fetch_files_list(self, account_id: UUID) -> list[UUID]:
        """
        Get a list of files in storage for the specified account ID. The list of
        of storage IDs will be returned.

        :param account_id: Account ID to fetch the list of files for
        :type account_id: UUID
        :return: List of storage IDs
        :rtype: list[UUID]
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete_file(self, account_id: UUID, file_id: UUID) -> bool:
        """
        Delete a file in storage

        :param account_id: Account ID the file must be related to
        :type account_id: UUID
        :param file_id: Storage ID for the file
        :type file_id: UUID
        :raises FileNotFound: If file with such storage ID was not found
        :raises FileDeletionFailed: If any issues with deleting the file
        :return: 'True' if deletion was success
        :rtype: bool
        """
        raise NotImplementedError()