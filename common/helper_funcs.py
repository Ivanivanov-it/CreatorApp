


MAGIC_BYTES = {
    b'\xff\xd8\xff': 'image/jpeg',
    b'\x89PNG': 'image/png',
    b'RIFF': 'image/webp',
}

def validate_image_magic_bytes(file):
    file.seek(0)
    header = file.read(12)
    file.seek(0)

    for magic, mime in MAGIC_BYTES.items():
        if header.startswith(magic):
            if mime == 'image/webp' and b'WEBP' not in header:
                continue
            return mime
    return None