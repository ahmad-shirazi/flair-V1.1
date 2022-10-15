

class Document(object):
    def __init__(self, document_id, file_key, original_name, original_bucket_name, result=None,
                 status=None, created_at=None, updated_at=None):
        self.id = document_id
        self.fileKey = file_key

        self.originalName = original_name
        self.originalBucketName = original_bucket_name

        self.result = result
        self.status = status

        self.createdAt = created_at
        self.updatedAt = updated_at


class Token(object):
    def __init__(self, token_id, file_key, key, value, created_at=None, updated_at=None):
        self.id = token_id
        self.fileKey = file_key

        self.key = key
        self.value = value

        self.createdAt = created_at
        self.updatedAt = updated_at


class Image(object):
    def __init__(self, image_id, file_key, name, bucket_name, number,
                 noise_removed_name='', noise_removed_bucket_name='', ocr_name='', ocr_bucket_name='',
                 result='', status='', created_at=None, updated_at=None):
        self.id = image_id
        self.fileKey = file_key

        self.name = name
        self.bucketName = bucket_name
        self.number = number

        self.noiseRemovedName = noise_removed_name
        self.noiseRemovedBucketName = noise_removed_bucket_name

        self.ocrName = ocr_name
        self.ocrBucketName = ocr_bucket_name

        self.result = result
        self.status = status

        self.createdAt = created_at
        self.updatedAt = updated_at
