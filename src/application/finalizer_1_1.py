from src.dataaccess import document as document_data_access,\
    image as image_data_access, \
    token as token_data_access
from src.config.enum import STATUS
from src.util.misc import Token
from src.ai.tokenized import run as run_tokenized


class Finalizer(object):
    def __init__(self, name):
        self.name = name

    @staticmethod
    async def run():
        next_files = await document_data_access.fetch_by_status(STATUS["OCR"])
        if len(next_files) <= 0:
            return
        next_file = next_files[0]
        next_file.status = STATUS["FINISHED"]
        key_value_list = run_tokenized(next_file.result)
        for key, value in key_value_list.items():
            token = Token(token_id=0, file_key=next_file.fileKey, key=key, value=value)
            _ = await token_data_access.insert(token)
        _ = await document_data_access.update(next_file)
