# PDF to JPEG Azure Function (Custom docker runtime)

This Azure function uses the [pdf2image](https://pypi.org/project/pdf2image/) library to convert PDF files to JPEG format. Each page is converted to JPEG. All the pages are then concatenated together into an .jblob file. 

The .jblob file can then be converted back into multiple JPEGs by parsing it ([example parser](https://github.com/SoTrx/jblob-decoder)).

The function is triggered each time a file is dropped in the **src** BLOB container and puts the resulting .jblob in the **out** BLOB container. Both **src** and **out** are in the same Storage Account **DataStorage** (see [Configuration](#configuration)).

## Usage

To use this function, you must [create an Azure Function App](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-azure-function) and select *Docker Container* in the "Publish" section.

Once the Function App is created, select "Container settings" is the app dashboard and enter *dockerutils/pypdftojpg:latest* under "Full Image Name and Tag" (or any custom made Docker image).

## Configuration 

This function uses a single variable called **DataStorage**. In the app dashboard, select "Configuration" and provide a value for DataStorage (The Storage Account access key).

See the [application settings documentation](https://docs.microsoft.com/en-us/azure/azure-functions/functions-how-to-use-azure-function-app-settings#settings).

```json
{
    "scriptFile": "__init__.py",
    "bindings": [
        {
            "name": "myBlob",
            "type": "blobTrigger",
            "direction": "in",
            "path": "src/{name}",
            "connection": "DataStorage"
        },
        {
            "name": "myOutputBlob",
            "type": "blob",
            "path": "out/{name}.jblob",
            "connection": "DataStorage",
            "direction": "out"
        }
    ]
}
```

## Why Docker

The pdf2image library requires the poppler tool to be installed on the host. This tool is not included in the default Microsoft Python runtime, so this runtime needs to be extended.