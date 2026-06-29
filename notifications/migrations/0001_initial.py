# Generated manually for notifications app

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('incident_created', 'Incident Created'), ('incident_updated', 'Incident Updated'), ('dispatch_created', 'Dispatch Created'), ('dispatch_assigned', 'Dispatch Assigned'), ('dispatch_status_changed', 'Dispatch Status Changed'), ('dispatch_cancelled', 'Dispatch Cancelled'), ('system_alert', 'System Alert')], max_length=50)),
                ('title', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('data', models.JSONField(blank=True, default=dict)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [
                    models.Index(fields=['recipient', 'is_read'], name='notifications_recipient_is_read_idx'),
                    models.Index(fields=['-created_at'], name='notifications_created_at_idx'),
                ],
            },
        ),
    ]
