# Generated by Django 3.2.10 on 2022-02-04 18:22

import akun.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AkunGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Member', max_length=25, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=75, null=True)),
                ('email', models.EmailField(help_text='Email tidak akan ditampilkan', max_length=254, null=True)),
                ('teks', models.TextField()),
                ('cmdate', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-cmdate'],
            },
        ),
        migrations.CreateModel(
            name='MyAkun',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('profile', models.ImageField(blank=True, null=True, upload_to=akun.models.upload_to_path)),
                ('nomor_hape', models.CharField(blank=True, max_length=17, null=True)),
                ('alamat', models.CharField(blank=True, max_length=255, null=True)),
                ('jenis_kelamin', models.CharField(choices=[('P', 'Male'), ('W', 'Female')], default='P', max_length=10)),
                ('akun_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='akun.akungroup')),
            ],
        ),
    ]