import os


class Config:
    DB_STRING = 'postgresql+asyncpg://{username}:{password}@{container}:{port}/{db_name}'
    USERNAME = os.getenv('POSTGRES_USER', 'postgres')
    PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
    CONTAINER = os.getenv('POSTGRES_CONTAINER_NAME', 'pg_container')
    PORT = os.getenv('POSTGRES_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'postgres')

    DB_STRING = DB_STRING.format(username=USERNAME,
                                 password=PASSWORD,
                                 container=CONTAINER,
                                 port=PORT,
                                 db_name=DB_NAME)

    # Storage configuration
    MINIO_HOST = os.getenv('MINIO_HOST', 'localhost')
    MINIO_PORT = os.getenv('MINIO_PORT', '9000')

    MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minioUser')
    MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', '72sjjhfmmmkasdkjdwidjsafkjfh39938fhasdfSSS@#')

    MINIO_BUCKET = os.getenv('MINIO_BUCKET', 'patients-data')

    # introduce dummy doctor login and password
    DOCTOR_LOGIN = 'DOCTOR_LOGIN'
    DOCTOR_PASSWORD = 'DOCTOR_PASSWRD'


config = Config()
