# Generated by Django 5.2.1 on 2025-06-18 10:21

import dirtyfields.dirtyfields
import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text='Unique identifier for this model instance.', unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp indicating when the instance was created.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp indicating when the instance was last updated.')),
                ('cover_letter', models.TextField()),
                ('resume', models.FileField(upload_to='resumes/')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('REVIEWED', 'Reviewed'), ('SHORTLISTED', 'Shortlisted'), ('REJECTED', 'Rejected'), ('ACCEPTED', 'Accepted')], default='PENDING', max_length=20)),
                ('expected_salary', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('candidate', models.ForeignKey(limit_choices_to={'role': 'CANDIDATE'}, on_delete=django.db.models.deletion.CASCADE, related_name='job_applications', to=settings.AUTH_USER_MODEL)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='job.job')),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('job', 'candidate')},
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
    ]
