from django import forms
from .models import Incident, State, LGA, Ward


class IncidentForm(forms.ModelForm):
    latitude = forms.FloatField(label="Latitude", required=False)
    longitude = forms.FloatField(label="Longitude", required=False)
    state = forms.ModelChoiceField(
        queryset=State.objects.all().order_by('name'),
        label="State",
        required=False,
        empty_label="Select a State"
    )
    lga = forms.ModelChoiceField(
        queryset=LGA.objects.none(),
        label="LGA",
        required=False,
        empty_label="Select an LGA"
    )
    ward = forms.ModelChoiceField(
        queryset=Ward.objects.none(),
        label="Ward",
        required=False,
        empty_label="Select a Ward"
    )

    media_type = forms.ChoiceField(
        choices=Incident.MEDIA_TYPES,
        label="Media Type",
        required=False,
    )
    file = forms.FileField(
        label="Media File",
        required=False,
    )

    class Meta:
        model = Incident
        fields = ["title", "description", "report_type", "media_type", "file", "latitude", "longitude", "state", "lga", "ward"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        css = "w-full px-4 py-2 border border-slate-200 rounded-lg"
        self.fields["title"].widget.attrs.update({"placeholder": "Enter incident title...", "class": css})
        self.fields["description"].widget.attrs.update({"placeholder": "Describe what happened...", "class": css})
        self.fields["report_type"].widget.attrs.update({"class": css})
        self.fields["media_type"].widget.attrs.update({"class": css})
        self.fields["file"].widget.attrs.update({"class": css})
        self.fields["latitude"].widget.attrs.update({"placeholder": "Latitude", "class": css})
        self.fields["longitude"].widget.attrs.update({"placeholder": "Longitude", "class": css})
        self.fields["state"].widget.attrs.update({
            "class": css,
            "hx-get": "/api/get-lgas/",
            "hx-target": "#lga-select-wrapper",
            "hx-swap": "innerHTML",
            "hx-trigger": "change",
            "onchange": "onStateChange(this)",
        })
        self.fields["lga"].widget.attrs.update({
            "class": css,
            "id": "id_lga",
            "hx-get": "/api/get-wards/",
            "hx-target": "#ward-select-wrapper",
            "hx-swap": "innerHTML",
            "hx-trigger": "change",
            "onchange": "onLgaChange(this)",
        })
        self.fields["ward"].widget.attrs.update({"class": css, "id": "id_ward"})

        if "state" in self.data:
            try:
                state_id = int(self.data.get("state"))
                self.fields["lga"].queryset = LGA.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass

        if "lga" in self.data:
            try:
                lga_id = int(self.data.get("lga"))
                self.fields["ward"].queryset = Ward.objects.filter(lga_id=lga_id).order_by('name')
            except (ValueError, TypeError):
                pass
        self.fields["file"].widget.attrs.update({"accept": "*.mp4,*.jpg,*.png, *.webp,*.mp3,*.avi"})
        
