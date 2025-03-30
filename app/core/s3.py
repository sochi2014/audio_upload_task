import aioboto3
from botocore.config import Config
from botocore.exceptions import ClientError
from fastapi import UploadFile

from app.core.config import settings


class S3Client:
    def __init__(self):
        self.session = aioboto3.Session()
        self.config = Config(s3={'addressing_style': 'path'})
        self.bucket_name = settings.MINIO_BUCKET_NAME

    async def get_client(self):
        """
        Создает и возвращает асинхронный клиент S3.
        Returns:
            aioboto3.client: Асинхронный клиент S3
        """
        return self.session.client(
            's3',
            endpoint_url=settings.MINIO_HOST,
            aws_access_key_id=settings.MINIO_ROOT_USER,
            aws_secret_access_key=settings.MINIO_ROOT_PASSWORD,
            region_name='us-east-1',
            config=self.config,
            verify=False
        )

    async def ensure_bucket_exists(self) -> bool:
        """
        Проверяет существование бакета и создает его, если он не существует.
        Возвращает True, если бакет существует или был создан.
        """
        async with await self.get_client() as client:
            try:
                await client.head_bucket(Bucket=self.bucket_name)
                return True
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == '404':
                    try:
                        await client.create_bucket(Bucket=self.bucket_name)
                        return True
                    except ClientError as create_error:
                        print(f"Error creating bucket: {create_error}")
                        return False
                else:
                    print(f"Error checking bucket: {e}")
                    return False

    async def upload_file(self, file: UploadFile, object_name: str) -> bool:
        """
        Загружает файл в S3/MinIO.
        Args:
            file: FastAPI UploadFile объект
            object_name: Имя объекта в бакете
        Returns:
            bool: True если загрузка успешна, False в противном случае
        """
        async with await self.get_client() as client:
            try:
                await client.upload_fileobj(
                    file.file,
                    self.bucket_name,
                    object_name,
                    ExtraArgs={'ContentType': file.content_type}
                )
                return True
            except ClientError as e:
                print(f"Error uploading file: {e}")
                return False

    async def get_file_url(self, object_name: str) -> str:
        """
        Генерирует URL для доступа к файлу.
        Args:
            object_name: Имя объекта в бакете
        Returns:
            str: URL файла
        """
        async with await self.get_client() as client:
            try:
                url = await client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': self.bucket_name, 'Key': object_name},
                    ExpiresIn=3600
                )
                return url
            except ClientError as e:
                print(f"Error generating URL: {e}")
                return ""

    async def delete_file(self, object_name: str) -> bool:
        """
        Удаляет файл из бакета.
        Args:
            object_name: Имя объекта в бакете
        Returns:
            bool: True если удаление успешно, False в противном случае
        """
        async with await self.get_client() as client:
            try:
                await client.delete_object(
                    Bucket=self.bucket_name,
                    Key=object_name
                )
                return True
            except ClientError as e:
                print(f"Error deleting file: {e}")
                return False


s3_client = S3Client()
