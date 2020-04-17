# Generated by Django 2.2.10 on 2020-04-17 23:02

from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Insta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostTwo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, null=True)),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='static/image/posts')),
            ],
        ),
    ]
