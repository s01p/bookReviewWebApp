# Generated by Django 2.0.13 on 2019-06-15 23:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_auto_20190615_1647'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commented', models.BooleanField(default=False)),
                ('book_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='record', to='book.Book')),
            ],
        ),
    ]
