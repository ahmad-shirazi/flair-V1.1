from src.config import minio as config
from minio import Minio
# from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
#                          BucketAlreadyExists)

minioClient = Minio(config.HOST,
                    access_key=config.ACCESS_KEY,
                    secret_key=config.SECRET_KEY,
                    secure=True)

for key in config.BUCKET_NAMES:
    bucket = minioClient.bucket_exists(config.BUCKET_NAMES[key])
    if not bucket:
        minioClient.make_bucket(config.BUCKET_NAMES[key])


# try:
#     minioClient.make_bucket("maylogs", location="us-east-1")
# except BucketAlreadyOwnedByYou as err:
#     pass
# except BucketAlreadyExists as err:
#     pass
# except ResponseError as err:
#     raise
# else:
#     try:
#         minioClient.fput_object('maylogs', 'pumaserver_debug.log', '/tmp/pumaserver_debug.log')
#     except ResponseError as err:
#         print(err)


class MinioUtil(object):
    def __init__(self):
        self.client = minioClient

    def get_object(self, bucket_name, object_name):
        pass

    def delete_object(self, bucket_name, object_name):
        pass
