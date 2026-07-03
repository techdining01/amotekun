import json
from django import forms
from django.contrib.gis.geos import GEOSGeometry
from .models import Camera


class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = "__all__"

    def clean_location(self):
        """Validates incoming hidden map widget input text data."""
        raw_data = self.cleaned_data.get("location")

        # Allow field to be blank if your model allows null values
        if not raw_data:
            return None

        # 1. Verify text string is well-formed JSON syntax
        try:
            parsed_json = json.loads(raw_data)
        except (ValueError, TypeError):
            raise forms.ValidationError(
                "Invalid string payload format sent from map device widget."
            )

        # 2. Assert basic structural components of GeoJSON specs
        if parsed_json.get("type") != "Point" or "coordinates" not in parsed_json:
            raise forms.ValidationError(
                "Payload is missing explicit coordinate definitions."
            )

        # 3. Clean and parse directly into Spatial GEOS instances
        try:
            # GEOSGeometry natively translates GeoJSON dict configurations cleanly
            spatial_point = GEOSGeometry(json.dumps(parsed_json))
            return spatial_point
        except Exception:
            raise forms.ValidationError(
                "Coordinates provided do not map to valid geometric points."
            )
