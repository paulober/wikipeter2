# Generated by Django 3.2.2 on 2021-05-15 13:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0009_class_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='mastercategory',
            name='date_created',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='classcategory',
            name='title',
            field=models.CharField(max_length=155),
        ),
        migrations.AlterField(
            model_name='wikifile',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Name'),
        ),
        migrations.AddConstraint(
            model_name='classcategory',
            constraint=models.UniqueConstraint(fields=('title', 'target_class'), name='unique_category_in_class'),
        ),
        migrations.AddConstraint(
            model_name='post',
            constraint=models.UniqueConstraint(fields=('title', 'category'), name='unique_post_in_category'),
        ),
        migrations.AddConstraint(
            model_name='post',
            constraint=models.UniqueConstraint(fields=('title', 'master_category'), name='unique_post_in_master_category'),
        ),
    ]