from django.db import migrations, models
import django.contrib.gis.db.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotspot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('hotspot_type', models.CharField(choices=[('crime', 'Crime'), ('violence', 'Violence'), ('traffic', 'Traffic')], default='crime', max_length=20)),
                ('intensity_score', models.FloatField(help_text='0-1 scale indicating hotspot intensity')),
                ('incident_count', models.IntegerField(default=0)),
                ('calculated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-intensity_score'],
            },
        ),
        migrations.CreateModel(
            name='HotspotAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('analysis_type', models.CharField(max_length=50)),
                ('parameters', models.JSONField(default=dict)),
                ('hotspot_bounds', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326)),
                ('results', models.JSONField(default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]