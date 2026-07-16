from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0002_add_hospital_ward_ambulance'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='has_mortuary',
            field=models.BooleanField(default=False),
        ),
    ]
