import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setting_key', models.CharField(max_length=100, verbose_name='Կարգավորման բանալի')),
                ('setting_value', models.CharField(max_length=200, verbose_name='Արժեք')),
                ('value_type', models.CharField(choices=[('int', 'Ամբողջ թիվ'), ('float', 'Տասնորդական'), ('string', 'Տեքստ'), ('boolean', 'Այո/Ոչ')], default='string', max_length=20, verbose_name='Տիպ')),
                ('description', models.TextField(blank=True, verbose_name='Նկարագրություն')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ակտիվ է')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discounts.tenant', verbose_name='Համալսարան')),
            ],
            options={
                'verbose_name': 'Համակարգային կարգավորում',
                'verbose_name_plural': 'Համակարգային կարգավորումներ',
                'ordering': ['setting_key'],
                'unique_together': {('tenant', 'setting_key')},
            },
        ),
    ]
