from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeographyBoundary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boundary_type', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('state_name', models.CharField(blank=True, max_length=50, null=True)),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(srid=4326)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddIndex(
            model_name='geographyboundary',
            index=models.Index(fields=['boundary_type'], name='geography_boundary_type_idx'),
        ),
    ]