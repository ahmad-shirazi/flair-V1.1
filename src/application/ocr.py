from src.util.google_cloud import get_gcs_url, get_text
from src.dataaccess import document as document_data_access, image as image_data_access
from src.config.enum import STATUS, BUCKET_NAMES
from src.util.name_setter import get_random_name


def get_ocr(file_name, bucket_name, destination_file_name, destination_bucket_name):
    source_url = get_gcs_url(bucket_name, file_name)
    destination_url = get_gcs_url(destination_bucket_name, destination_file_name)
    return get_text(source_url, destination_url)


class OCR(object):
    def __init__(self, name):
        self.name = name

    @staticmethod
    async def run():
        next_files = await document_data_access.fetch_by_status(STATUS["REMOVED_NOISE"])
        if len(next_files) <= 0:
            return
        next_file = next_files[0]
        images = await image_data_access.fetch_by_file_key(next_file.fileKey)
        for image in images:
            name = get_random_name(15) + ".json"
            bucket_name = BUCKET_NAMES["OCR"]
            image.ocrBucketName = bucket_name
            image.ocrName = name
            text = get_ocr(image.noiseRemovedName, image.noiseRemovedBucketName,
                           image.ocrName, image.ocrBucketName)
            image.result = text
            image.status = STATUS["OCR"]
            image.result = image.result.replace('\'', ' ').replace('\"', ' ')
            _ = await image_data_access.update(image)

        next_file.status = STATUS["OCR"]
        _ = await document_data_access.update(next_file)
