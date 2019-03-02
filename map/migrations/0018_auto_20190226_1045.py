# Generated by Django 2.1.5 on 2019-02-26 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0017_auto_20190224_1824'),
    ]

    operations = [
        migrations.CreateModel(
            name='partyboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('val', models.IntegerField(blank=True, null=True)),
                ('mys', models.IntegerField(blank=True, null=True)),
                ('ins', models.IntegerField(blank=True, null=True)),
                ('tag', models.TextField(blank=True, null=True)),
                ('arrived', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kid', models.CharField(max_length=30)),
                ('nick', models.CharField(max_length=15)),
                ('val', models.IntegerField(blank=True, null=True)),
                ('mys', models.IntegerField(blank=True, null=True)),
                ('ins', models.IntegerField(blank=True, null=True)),
                ('group', models.IntegerField(default=1)),
            ],
        ),
        migrations.RenameField(
            model_name='party',
            old_name='p_time',
            new_name='time',
        ),
        migrations.AddField(
            model_name='gym',
            name='nick',
            field=models.CharField(default='미정', max_length=10),
        ),
        migrations.AddField(
            model_name='party',
            name='description',
            field=models.TextField(blank=True, default='화력 미달시 펑', null=True),
        ),
        migrations.AddField(
            model_name='partyboard',
            name='party',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map.party'),
        ),
        migrations.AddField(
            model_name='partyboard',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map.user'),
        ),
    ]