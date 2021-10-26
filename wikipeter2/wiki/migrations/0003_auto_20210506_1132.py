# Generated by Django 3.2.1 on 2021-05-06 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0002_rename_body_post_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MasterCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='short_description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.CreateModel(
            name='ClassCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('target_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wiki.class')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wiki.classcategory'),
        ),
        migrations.AddField(
            model_name='post',
            name='master_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wiki.mastercategory'),
        ),
    ]
