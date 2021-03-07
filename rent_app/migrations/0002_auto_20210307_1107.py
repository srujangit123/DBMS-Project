# Generated by Django 3.1.4 on 2021-03-07 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rent_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='vacant',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='House_Management',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('house_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rent_app.house')),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rent_app.owner')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rent_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('rating', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8')], max_length=20)),
                ('house_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rent_app.house')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rent_app.user')),
            ],
            options={
                'unique_together': {('user_id', 'house_id')},
            },
        ),
    ]
