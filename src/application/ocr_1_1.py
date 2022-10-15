from src.util.google_cloud import get_gcs_url, get_text, get_text_from_pdf
from src.dataaccess import document as document_data_access, image as image_data_access
from src.config.enum import STATUS, BUCKET_NAMES
from src.util.name_setter import get_random_name


def get_ocr(file_name, bucket_name, destination_file_name, destination_bucket_name):
    source_url = get_gcs_url(bucket_name, file_name)
    destination_url = get_gcs_url(destination_bucket_name, destination_file_name)
    return get_text_from_pdf(source_url, destination_url)


class OCR(object):
    def __init__(self, name):
        self.name = name

    @staticmethod
    async def run():
        next_files = await document_data_access.fetch_by_status(STATUS["UNPROCESSED"])
        if len(next_files) <= 0:
            return
        next_file = next_files[0]
        bucket_name = BUCKET_NAMES["FINISHED"]
        name = get_random_name(15) + ".json"
        next_file.result = get_ocr(next_file.originalName, next_file.originalBucketName, name, bucket_name)
        next_file.result = next_file.result.replace('\'', ' ').replace('\"', ' ')
        next_file.status = STATUS["OCR"]
        _ = await document_data_access.update(next_file)
