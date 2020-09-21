# PDF to JPEG Azure Function (Custom docker runtime)

This Azure function uses the [pdf2image](https://pypi.org/project/pdf2image/) library to convert PDF files to JPEG format. 

There are multiple ways this project can be used:
+ The **master** branch will convert every page to JPEG and concatenate them togetehr into a single .jblob file. The .jblob file can then be converted back into multiple JPEGs by parsing it ([example parser](https://github.com/SoTrx/jblob-decoder)).
+ The **first_page_only** branch will only convert the first page to JPEG and save it as a .jpg file.

The function is triggered each time a file is dropped in the **pdfs** BLOB container and puts the resulting .jblob in the **images** BLOB container. (see [Configuration](#configuration)).

## Usage

To use this function, you must [create an Azure Function App](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-azure-function) and select *Docker Container* in the "Publish" section.

Once the Function App is created, select "Container settings" is the app dashboard and enter *dockerutils/pypdftojpg:latest* under "Full Image Name and Tag" (or any custom made Docker image).

## Configuration 

This function uses two variables called **InputStorage** and **OutputStorage**. In the app dashboard, select "Configuration" and provide a value for both InputStorage and OutputStorage (The Storage Accounts access key). Both variable can designate the same Azure Data Storage

See the [application settings documentation](https://docs.microsoft.com/en-us/azure/azure-functions/functions-how-to-use-azure-function-app-settings#settings).

```json
{
    "scriptFile": "__init__.py",
    "bindings": [
        {
            "name": "myBlob",
            "type": "blobTrigger",
            "direction": "in",
            "path": "pdfs/{name}",
            "connection": "InputStorage"
        },
        {
            "name": "myOutputBlob",
            "type": "blob",
            "path": "images/{name}.jblob",
            "connection": "OutputStorage",
            "direction": "out"
        }
    ]
}
```

## Why Docker

The pdf2image library requires the poppler tool to be installed on the host. This tool is not included in the default Microsoft Python runtime, so this runtime needs to be extended.