import logging
from os import cpu_count
import azure.functions as func
from io import BytesIO
from pdf2image import convert_from_bytes


def main(myBlob: func.InputStream, myOutputBlob: func.Out[func.InputStream]):
    """ Convert a PDF file into JPEG images.

    Args:
        myBlob (func.InputStream): A PDF file dropped into a storage account.
        myOutputBlob (func.Out[func.InputStream]): A binary sink to write new data into a storage account
    """
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myBlob.name}\n"
                 f"Blob Size: {myBlob.length} bytes")

    if(not myBlob.name.endswith(".pdf")):
        logging.info(f"{myBlob.name} isn't a PDF file, aborting.")
        return

    # Convert the PDF BLOB bytes stream into another bytes stream of multiple readeable images
    # JPEG Headers will later serve to tell them apart
    img_list = convert_from_bytes(
        myBlob.read(), fmt="jpg", thread_count=cpu_count())
    bIO = BytesIO()
    for img in img_list:
        img.save(bIO, format="jpeg")

    # Save the binary stream to a new Blob
    myOutputBlob.set(bIO.getvalue())
    logging.info(
        f"Processing complete for file {myBlob.name} ({len(img_list)} pages)")


