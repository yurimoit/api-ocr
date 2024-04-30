from google.cloud import documentai_v1 as documentai


def process_document(project_id: str, location: str,
                     processor_id: str, file_path: str,
                     mime_type: str) -> documentai.Document:
    """
    Processes a document using the Document AI API.
    """

    # Instantiates a client
    documentai_client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location/processor/processor-id
    # You must create new processors in the Cloud Console first
    resource_name = documentai_client.processor_path(
        project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

        # Load Binary Data into Document AI RawDocument Object
        raw_document = documentai.RawDocument(
            content=image_content, mime_type=mime_type)

        # Configure the process request
        request = documentai.ProcessRequest(
            name=resource_name, raw_document=raw_document)

        # Use the Document AI client to process the sample form
        result = documentai_client.process_document(request=request)

        return result.document


def main():
    """
    Run the codelab.
    """
    project_id = 'YOUR_PROJECT_ID'
    location = 'YOUR_PROJECT_LOCATION'  # Format is 'us' or 'eu'
    processor_id = 'YOUR_PROCESSOR_ID'  # Create processor in Cloud Console

    # The local file in your current working directory
    file_path = 'Winnie_the_Pooh_3_Pages.pdf'
    # Refer to https://cloud.google.com/document-ai/docs/processors-list for the supported file types
    mime_type = 'application/pdf'

    document = process_document(project_id=project_id, location=location,
                                processor_id=processor_id, file_path=file_path,
                                mime_type=mime_type)

    print("Document processing complete.")
    print(f"Text: {document.text}")
