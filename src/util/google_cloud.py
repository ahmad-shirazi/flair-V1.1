from google.cloud import storage
from google.cloud import vision
import json
import time
import os
import re

from src.config import google_cloud as google_config

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_config.GOOGLE_APPLICATION_CREDENTIALS


def upload_file(name, bucket_name, filename):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(name)

    blob.upload_from_filename(filename)

    print(f"File uploaded to {name}.")


def get_file(name, bucket_name, destination_url):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(name)

    blob.download_to_filename(destination_url)
    time.sleep(10)
    file_obj = open(destination_url, "rb")
    return file_obj


def get_gcs_url(bucket_name, file_name):
    return google_config.GOOGLE_CLOUD_URL.format(bucket_name, file_name)


def get_text(gcs_source_uri, gcs_destination_uri, mime_type=google_config.MIME_TYPES["image"], batch_size=10):
    client = vision.ImageAnnotatorClient()

    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    gcs_source = vision.GcsSource(uri=gcs_source_uri)
    input_config = vision.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size)

    async_request = vision.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config,
        output_config=output_config)

    operation = client.async_batch_annotate_files(
        requests=[async_request])

    # print('Waiting for the operation to finish.')
    operation.result(timeout=420)

    # Once the request has completed and the output has been
    # written to GCS, we can list all the output files.
    storage_client = storage.Client()

    match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)

    # List objects with the given prefix, filtering out folders.
    blob_list = [blob for blob in list(bucket.list_blobs(
        prefix=prefix)) if not blob.name.endswith('/')]
    # print('Output files:')
    # for blob in blob_list:
    #     print(blob.name)

    # Process the first output file.py from GCS.
    # Since we specified batch_size=2, the first response contains
    # the first two pages of the input file.py.
    output = blob_list[0]
    # print(output)
    json_string = output.download_as_string()
    response = json.loads(json_string)

    # The actual response for the first page of the input file.py.
    first_page_response = response['responses'][0]
    annotation = first_page_response['fullTextAnnotation']

    # Here we print the full text from the first page.
    # The response contains more information:
    # annotation/pages/blocks/paragraphs/words/symbols
    # including confidence scores and bounding boxes
    # print('Full text:\n')
    # print(annotation['text'])
    return annotation['text']


def get_text_from_pdf(gcs_source_uri, gcs_destination_uri):
    mime_type=google_config.MIME_TYPES["pdf"]

    client = vision.ImageAnnotatorClient()

    feature = vision.Feature(
        type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    gcs_source = vision.GcsSource(uri=gcs_source_uri)
    input_config = vision.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.OutputConfig(
        gcs_destination=gcs_destination, batch_size=100)

    async_request = vision.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config,
        output_config=output_config)

    operation = client.async_batch_annotate_files(
        requests=[async_request])

    print('Waiting for the operation to finish.')
    operation.result(timeout=420)

    storage_client = storage.Client()

    match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)

    blob_list = [blob for blob in list(bucket.list_blobs(
        prefix=prefix)) if not blob.name.endswith('/')]
    print('Output files:')
    for blob in blob_list:
        print(blob.name)

    output = blob_list[0]

    json_string = output.download_as_string()
    response = json.loads(json_string)    
    result = ""
    for i in range(len(response['responses'])):
        try:
            each_page_response = response['responses'][i]
            annotation = each_page_response['fullTextAnnotation']
            result = result + "\n" + annotation['text']
        except:
            print("No content in page " + str(i+1))

    return result
