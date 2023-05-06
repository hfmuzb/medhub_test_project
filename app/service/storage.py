from typing import Union
import uuid
from pathlib import Path
from loguru import logger
import aioboto3

from service.parsers import parse_full_s3_path
from config import config


class AioBoto3:
    def __init__(
            self,
            storage_host=config.MINIO_HOST,
            storage_port=config.MINIO_PORT,
            access_key=config.MINIO_ACCESS_KEY,
            secret_key=config.MINIO_SECRET_KEY,
            s3_bucket=config.MINIO_BUCKET
    ):
        self.endpoint_url = f"http://{storage_host}:{storage_port}"
        self.s3_bucket = s3_bucket
        self.session = aioboto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

    async def create_bucket(self, bucket: str):
        async with self.session.client('s3', endpoint_url=self.endpoint_url) as s3_client:
            try:
                logger.info("Trying to create bucket")
                await s3_client.create_bucket(Bucket=bucket)
            except Exception as e:
                logger.info("Coulnd't create bucket")
                logger.exception(e)
                pass

    async def upload(
            self,
            input_filepath: Union[str, Path],
            filename: str,
            patient_id: uuid.UUID
    ) -> str:
        s3_path = f"{str(patient_id)}/{filename}"
        async with self.session.client('s3', endpoint_url=self.endpoint_url) as s3_client:
            await s3_client.upload_file(
                str(input_filepath),
                self.s3_bucket,
                s3_path
            )
        return f"s3://{self.s3_bucket}/{s3_path}"

    async def remove_object(
            self,
            full_s3_path: str
    ):
        bucket, s3_key = parse_full_s3_path(full_s3_path=full_s3_path)
        async with self.session.client('s3', endpoint_url=self.endpoint_url) as s3_client:
            await s3_client.delete_object(
                Bucket=bucket,
                Key=s3_key
            )

    async def object_exists(
            self,
            bucket: str,
            s3_key: str
    ) -> bool:
        async with self.session.client('s3', endpoint_url=self.endpoint_url) as s3_client:
            try:
                await s3_client.head_object(Bucket=bucket, Key=s3_key)
                return True
            except:
                # TODO dive deeper into boto3 exceptions here
                return False


s3 = AioBoto3()
