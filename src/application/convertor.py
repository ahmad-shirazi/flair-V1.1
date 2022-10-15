
from src.util.google_cloud import upload_file, get_file
from src.dataaccess import document as document_data_access, image as image_data_access
from src.config.enum import STATUS, BUCKET_NAMES
from src.config.file import TEMP_FOLDER
from src.util.misc import Image
from src.util.name_setter import get_random_name
from pdf2image import convert_from_path


# todo ahmad
#  https://pypi.org/project/pdf2image/
def convert_pdf_to_images(url, local_bucket_name):
    print(url)
    pages = convert_from_path(url)
    for page in pages:
        page.save("%spage_%d.tiff" % (local_bucket_name, pages.index(page)), "TIFF")
    return pages


def create_image_model(file_key, name, bucket_name, number, status):
    image = Image(image_id=None, file_key=file_key, name=name, bucket_name=bucket_name, number=number, status=status)
    return image


class Convertor(object):
    def __init__(self, name):
        self.name = name

    @staticmethod
    async def run():
        next_files = await document_data_access.fetch_by_status(STATUS["UNPROCESSED"])
        if len(next_files) <= 0:
            return
        next_file = next_files[0]
        base_url = TEMP_FOLDER + BUCKET_NAMES["CONVERTED"] + "/"
        destination_url = base_url + next_file.originalName
        _ = get_file(name=next_file.originalName,
                     bucket_name=next_file.originalBucketName,
                     destination_url=destination_url)
        images = convert_pdf_to_images(url=destination_url, local_bucket_name=base_url)
        for i in range(len(images)):
            name = get_random_name(15) + ".tiff"
            bucket_name = BUCKET_NAMES["CONVERTED"]
            image = create_image_model(file_key=next_file.fileKey, name=name, bucket_name=bucket_name,
                                       number=i, status=STATUS["CONVERTED"])

            file_url = base_url + "page_{}.tiff".format(i)
            upload_file(name, bucket_name, file_url)
            _ = await image_data_access.insert(image)

        next_file.status = "CONVERTED"
        _ = await document_data_access.update(next_file)
