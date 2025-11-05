from uuid import UUID, uuid4
from typing import Union
from fastapi import UploadFile

from common.exception.repository_exception import NotFoundException

# local imports
from ..interface import AbstractImageProcessor, AbstractBlobStorageClient, AbstractFileStorage
from ..database.repository import FileRegisterRepository
from ..model.dto import BlobFileContainerDto, FileContainerDto
from ..exception import FileFetchingFailed, FileStoringFailed, FileNotFound, UploadFailed, DownloadFailed, DeleteFailed, FileDeletionFailed


class FileStorage(AbstractFileStorage):

    def __init__(
        self,
        image_processor: AbstractImageProcessor,
        blob_storage_client: AbstractBlobStorageClient,
        file_register_repository: FileRegisterRepository,
    ):
        self._image_processor = image_processor
        self._blob_storage_client = blob_storage_client
        self._file_register_repository = file_register_repository

    
    async def store_file(self, account_id: UUID, file: FileContainerDto) -> UUID:
        filename = f"{str(uuid4())}.{file.data_format}"
        blob_file_path = f"{account_id}/{filename}"
        try:
            file_entry = await self._file_register_repository.create(
                {"account_id": account_id, "file_name": filename, "file_path": blob_file_path, "data_format": file.data_format}
            )
        except Exception as err:
            raise FileStoringFailed("failed_to_store_file") from err

        try:
            await self._blob_storage_client.upload(
                blob=BlobFileContainerDto(
                    blob_path=blob_file_path,
                    data=file.data
                )
            )
        except UploadFailed:
            raise FileStoringFailed("failed_to_store_file")
        
        return file_entry.id


    async def fetch_file(self, account_id: UUID, file_id: UUID) -> FileContainerDto:
        try:
            file_entry = await self._file_register_repository.get_one(entity_id=file_id)
        except NotFoundException:
            raise FileNotFound("file_not_found_in_storage")

        if file_entry.account_id != account_id:
            raise FileNotFound("file_not_found_in_storage")
        
        try:
            blob_file = await self._blob_storage_client.download(path=file_entry.file_path)
        except DownloadFailed:
            raise FileFetchingFailed("failed_to_fetch_file")
        
        return FileContainerDto(
            file_id=file_id,
            data_format=file_entry.data_format,
            data=blob_file.data
        )
    
    async def fetch_files_list(self, account_id: UUID) -> list[UUID]:
        file_entries = await self._file_register_repository.get_by_account_id(account_id=account_id)

        return [file_entry.id for file_entry in file_entries]
    
    async def delete_file(self, account_id: UUID, file_id: UUID) -> bool:
        try:
            file_entry = await self._file_register_repository.get_one(entity_id=file_id)
        except NotFoundException:
            raise FileNotFound("file_not_found_in_storage")

        if file_entry.account_id != account_id:
            raise FileNotFound("file_not_found_in_storage")
        
        try:
            await self._blob_storage_client.delete(path=file_entry.file_path)
            await self._file_register_repository.delete(entity_id=file_id)
            return True
        except DeleteFailed:
            raise FileDeletionFailed("failed_to_delete_file")