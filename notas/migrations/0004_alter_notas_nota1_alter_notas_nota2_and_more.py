# Generated by Django 5.2 on 2025-04-22 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notas', '0003_alter_notas_nota1_alter_notas_nota2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notas',
            name='nota1',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='notas',
            name='nota2',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='notas',
            name='nota3',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
