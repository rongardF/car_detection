import aioboto3
from botocore.client import Config as BotoConfig

from common.config import Config

# local imports
from ..interface import AbstractBlobStorageClient
from ..model.dto import BlobFileContainerDto
from ..exception.service import UploadFailed, DownloadFailed, DeleteFailed


class BlobStorageClient(AbstractBlobStorageClient):

    def __init__(self, config: Config) -> None:
        self._config = config
        self._session = aioboto3.Session(
            aws_access_key_id=config.require_config("SCW_ACCESS_KEY"),
            aws_secret_access_key=config.require_config("SCW_SECRET_KEY"),
            region_name="pl-waw",
        )

    async def upload(self, blob: BlobFileContainerDto) -> None:
        async with self._session.client(
            "s3",
            endpoint_url=self._config.require_config("SCW_BLOB_ENDPOINT"),
            config=BotoConfig(signature_version="s3v4"),
        ) as s3:
            try:
                await s3.put_object(
                    Bucket=self._config.require_config("SCW_BUCKET"),
                    Key=blob.blob_path,
                    Body=blob.data
                )
                return True
            except Exception as e:
                raise UploadFailed("blob_upload_failed") from e
    
    async def download(self, path: str) -> BlobFileContainerDto:
        async with self._session.client(
            "s3",
            endpoint_url=self._config.require_config("SCW_BLOB_ENDPOINT"),
            config=BotoConfig(signature_version="s3v4"),
        ) as s3:
            try:
                response = await s3.get_object(
                    Bucket=self._config.require_config("SCW_BUCKET"),
                    Key=path,
                )
                file_data = await response["Body"].read()
                return BlobFileContainerDto(
                    blob_path=path,
                    data=file_data,
                )
            except Exception as e:
                raise DownloadFailed("blob_download_failed") from e
            
    async def delete(self, path: str) -> bool:
        async with self._session.client(
            "s3",
            endpoint_url=self._config.require_config("SCW_BLOB_ENDPOINT"),
            config=BotoConfig(signature_version="s3v4"),
        ) as s3:
            try:
                await s3.delete_object(
                    Bucket=self._config.require_config("SCW_BUCKET"),
                    Key=path,
                )
                return True
            except Exception as e:
                raise DeleteFailed("blob_deletion_failed") from e
        
