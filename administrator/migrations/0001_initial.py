# Generated by Django 2.1.5 on 2019-03-01 08:34

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
            name='UserExtension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telephone', models.CharField(blank=True, max_length=50, verbose_name='Telephone')),
                ('sex', models.IntegerField(blank=True, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user_extension',
            },
        ),
        migrations.CreateModel(
            name='UserStudy',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('study_time', models.DateTimeField(blank=True, null=True)),
                ('study_id', models.IntegerField()),
            ],
            options={
                'db_table': 'study_mid',
            },
        ),
        migrations.AddField(
            model_name='userextension',
            name='studies',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.UserStudy'),
        ),
        migrations.AddField(
            model_name='userextension',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='extension', to=settings.AUTH_USER_MODEL),
        ),
    ]
