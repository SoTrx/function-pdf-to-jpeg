import logging
from os import cpu_count
import azure.functions as func
from io import BytesIO
from pdf2image import convert_from_bytes

def main(myBlob: func.InputStream, myOutputBlob: func.Out[func.InputStream]):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myBlob.name}\n"
                 f"Blob Size: {myBlob.length} bytes")
    
    if(not myBlob.name.endswith(".pdf")):
        logging.info(f"{myBlob.name} isn't a PDF file, aborting.")
        return
    
    img_list = convert_from_bytes(myBlob.read(), fmt="jpg", thread_count=cpu_count(), single_file=True)
    bIO = BytesIO()
    for img in img_list:
        img.save(bIO, format="jpeg")  
    myOutputBlob.set(bIO.getvalue())
    logging.info(f"Processing complete for file")