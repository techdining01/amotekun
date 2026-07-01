from django.db import migrations, models
import django.contrib.gis.db.models.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_fix_road_geometry'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncidentMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_type', models.CharField(choices=[('image', 'Image'), ('video', 'Video')], max_length=10)),
                ('file', models.FileField(upload_to='incidents/%Y/%m/%d/')),
                ('caption', models.CharField(blank=True, max_length=500)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('incident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media', to='reports.incident')),
            ],
            options={
                'ordering': ['-uploaded_at'],
            },
        ),
    ]