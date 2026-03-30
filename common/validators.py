import os
from cloudinary.forms import CloudinaryFileField
from django import forms
from common.helper_funcs import validate_image_magic_bytes


class ValidatedCloudinaryFileField(CloudinaryFileField):
    ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp']
    VALID_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']
    MAX_SIZE_MB = 2

    def to_python(self, data):

        if not data or isinstance(data, str):
            return super().to_python(data)

        ext = os.path.splitext(data.name)[-1].lower()
        if ext not in self.VALID_EXTENSIONS:
            raise forms.ValidationError("Only JPEG, PNG, and WebP images are allowed.")

        if hasattr(data, 'content_type') and data.content_type not in self.ALLOWED_TYPES:
            raise forms.ValidationError("Only JPEG, PNG, and WebP images are allowed.")


        detected_type = validate_image_magic_bytes(data)
        if detected_type is None:
            raise forms.ValidationError("File does not appear to be a valid image.")
        if detected_type not in self.ALLOWED_TYPES:
            raise forms.ValidationError("Only JPEG, PNG, and WebP images are allowed.")


        if data.size > self.MAX_SIZE_MB * 1024 * 1024:
            raise forms.ValidationError(f"Image must not exceed {self.MAX_SIZE_MB}MB.")

        return super().to_python(data)