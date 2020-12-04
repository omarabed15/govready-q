import filetype
import mimetypes, magic
from django.http import JsonResponse

# Dictionary of valid extensions and content types
VALID_EXTS = {
    ".zip"  : ("application/zip",),
    ".pdf"  : ("application/pdf",),
    ".png"  : ("image/png",),
    ".jpg"  : ("image/jpeg",),
    ".doc"  : ("application/msword",),
    ".docx" : ("application/vnd.openxmlformats-officedocument.wordprocessingml.document",),
    ".vsd"  : ("application/vnd.visio",),
    ".xls"  : ("application/vnd.ms-excel",),
    ".xlsx" : ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",),
    ".csv"  : ("application/csv", "text/csv",),
    ".ppt"  : ("application/vnd.ms-powerpoint",),
    ".pptx" : ("application/vnd.openxmlformats-officedocument.presentationml.presentation",),
    ".txt"  : ("text/plain",),
    ".md"   : ("text/markdown",),
    ".yaml" : ("text/plain",),
    ".yml"  : ("text/plain",),
}

def validate_file_extension(file):
    """
    Validates the file extension and type
    """

    for chunk in file.chunks():
        # Archive and image filetypes will display chunks since it only looks at the first 261 bytes
        filechunk = filetype.guess(chunk)
        print(file.content_type)

        # mime and extension
        filechunk_content_type = filechunk.mime if filechunk is not None else None
        filechunk_extension = f".{filechunk.extension}" if filechunk is not None else None

        if filechunk_content_type == None or filechunk_extension == None:

            # Get mimetype with id_buffer
            with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
                filechunk_content_type = m.id_buffer(chunk)
                filechunk_extension = mimetypes.guess_extension(filechunk_content_type) if filechunk_content_type not in ('application/csv', 'text/csv') else '.csv'

        # If it is not a valid mime or extension that return http response with error message.
        if filechunk_content_type not in VALID_EXTS.values() or filechunk_extension not in VALID_EXTS:
            return JsonResponse(status=400, data={'status': 'error',
                                                  'message': f"The file {file.name} does not have a supported file type"})
