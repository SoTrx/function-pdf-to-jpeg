import logging
from os import cpu_count, environ
import azure.functions as func
from io import BytesIO
from pdf2image import convert_from_bytes
from azure.storage.blob import ContainerClient

DEST_CONTAINER_NAME="images"

def main(myBlob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myBlob.name}\n"
                 f"Blob Size: {myBlob.length} bytes")
    
    if(not myBlob.name.endswith(".pdf")):
        logging.info(f"{myBlob.name} isn't a PDF file, aborting.")
        return
    
    # Retrieving the BLOB container
    connection_string = environ['CUSTOMCONNSTR_OutputStorage']
    logging.debug(f"Connection string is : {connection_string}")
    blob_container = ContainerClient.from_connection_string(conn_str=connection_string, container_name=DEST_CONTAINER_NAME)
    try:
        blob_container.create_container()
        logging.info(f"Container {DEST_CONTAINER_NAME} created.")
    except:
        logging.info(f"Container {DEST_CONTAINER_NAME} already exists. Proceeding with it.")

    # Actauly convert the pdf
    img_list = convert_from_bytes(myBlob.read(), fmt="jpg", thread_count=cpu_count())
    
    # Upload each image
    for index, img in enumerate(img_list, start=1):
        bIO = BytesIO()
        img.save(bIO, format="jpeg")  
        blob_container.upload_blob(f"{myBlob.name}-{index}.jpg", bIO)
    
    logging.info(f"Processing complete for file {myBlob.name} ({len(img_list)} pages)" )