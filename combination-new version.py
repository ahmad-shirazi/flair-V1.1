from google.cloud import storage
import json
import re
from google.cloud import vision
from google.cloud import storage
import PyPDF2
import glob
# import OS module
import os

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    bucket_name = "ocrinpu"
    # The path to your file to upload
    source_file_name = source_filename
    # The ID of your GCS object
    destination_blob_name = destination_blob_name

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_filename)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )




# def async_detect_document(gcs_source_uri='gs://ocrinpu/00000231.PDF', gcs_destination_uri='gs://ocroutp/00000231'):

def async_detect_document(gcs_source_uri, gcs_destination_uri, h):
    """OCR with PDF/TIFF as source files on GCS"""

    # Supported mime_types are: 'application/pdf' and 'image/tiff'
    mime_type = 'application/pdf'

    # How many pages should be grouped into each json output file.
    file = open(source_filename, 'rb')
    readpdf = PyPDF2.PdfFileReader(file)
    totalpages = readpdf.numPages

    batch_size = totalpages

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
    print('Output files:')
    for blob in blob_list:
        print(blob.name)

    # Process the first output file from GCS.
    # Since we specified batch_size=2, the first response contains
    # the first two pages of the input file.
    output = blob_list[0]
    # print(output)
    json_string = output.download_as_string()
    response = json.loads(json_string)

    # The actual response for the first page of the input file.
    
    print("aminn----")
    print(totalpages)
    print(len(response['responses']))
    # print(response['responses'])

    for i in range (totalpages):
        try:
            each_page_response = response['responses'][i]
            annotation = each_page_response['fullTextAnnotation']
            text_file = open(source_folder + str(i) + "A.txt", "w")
            n = text_file.write(annotation['text'])
            text_file.close()
        except:
            print("No content in page " + str(i+1))


    # print('Full text:\n')
    # print(annotation['text'])

    
    dir_list = os.listdir(source_folder)
    filenames=[]
    for x in dir_list:
        if x.endswith("A.txt"):
            filenames.append(x)

    filenames = sorted(filenames)
    # print(filenames)

    
    with open(source_folder + str(h) + ".txt", "w") as outfile:
        for fname in filenames:
            with open(source_folder + fname) as infile:
                for line in infile:
                    outfile.write(line)


    files = glob.glob(source_folder + "*A.txt")
    for f in files:
        os.remove(f)
# file = open(source_filename, 'rb')
# readpdf = PyPDF2.PdfFileReader(file)
# totalpages = readpdf.numPages
# print(totalpages)
    # return annotation['text']

source_folder   = "/Users/ahmadmshirazi/Desktop/Test2/"



for j in range(1,2):
    source_filename = "/Users/ahmadmshirazi/Desktop/Flairsoft-projects/P4-V1/Download/Documents/" + str(j) + ".pdf"
    destination_blobname = str(j) + ".pdf"
    upload_blob("", source_filename , destination_blobname)
    async_detect_document('gs://ocrinpu/' + str(j) + ".pdf", 'gs://ocroutp/' + str(j),j)

# async_detect_document('gs://ocrinpu/00000231.PDF', 'gs://ocroutp/00000231')


