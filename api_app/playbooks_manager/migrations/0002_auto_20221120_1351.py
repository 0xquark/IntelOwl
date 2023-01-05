# Generated by Django 3.2.15 on 2022-11-20 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('certego_saas_organization', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('playbooks_manager', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cachedplaybook',
            name='job',
        ),
        migrations.AddField(
            model_name='cachedplaybook',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='certego_saas_organization.organization'),
        ),
        migrations.AddField(
            model_name='cachedplaybook',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]