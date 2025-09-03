from fastapi import UploadFile


class ArquivoWrapper:
    def __init__(self, filename: str, content: bytes):
        self.filename = filename
        self.content = content

    @classmethod
    async def from_upload_file(cls, file: UploadFile):
        content = await file.read()  # Assíncrono!
        return cls(filename=file.filename, content=content)
