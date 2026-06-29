"""Model fields for storing sensitive data encrypted at rest."""
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models


class EncryptedCharField(models.TextField):
    """A text field that is transparently encrypted at rest using Fernet.

    The ciphertext is stored in the database; plaintext is only ever held in
    memory. Used for sensitive values such as camera RTSP credentials. The
    symmetric key is read from ``settings.FIELD_ENCRYPTION_KEY``.

    Note: because Fernet is non-deterministic, these fields cannot be used in
    equality lookups/filters — which is the desired behaviour for secrets.
    """

    description = "Transparently encrypted text field (Fernet)."

    def _fernet(self) -> Fernet:
        key = getattr(settings, "FIELD_ENCRYPTION_KEY", "")
        if not key:
            raise ImproperlyConfigured(
                "FIELD_ENCRYPTION_KEY must be set to read/write EncryptedCharField "
                "values. Generate one with: python -c "
                '"from cryptography.fernet import Fernet; '
                'print(Fernet.generate_key().decode())"'
            )
        return Fernet(key if isinstance(key, bytes) else key.encode())

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value in (None, ""):
            return value
        return self._fernet().encrypt(str(value).encode()).decode()

    def from_db_value(self, value, expression, connection):
        if value in (None, ""):
            return value
        try:
            return self._fernet().decrypt(value.encode()).decode()
        except InvalidToken:
            # Value predates encryption (stored as plaintext) — return as-is so
            # existing rows remain readable and can be re-saved encrypted.
            return value
