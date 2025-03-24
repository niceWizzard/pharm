# Generated by Django 5.1.7 on 2025-03-24 07:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0003_alter_inventoryitem_category_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventorytransaction',
            old_name='item',
            new_name='item_stock',
        ),
        migrations.RemoveField(
            model_name='inventoryitem',
            name='date_of_delivery',
        ),
        migrations.RemoveField(
            model_name='inventoryitem',
            name='expiration_date',
        ),
        migrations.RemoveField(
            model_name='inventoryitem',
            name='stocks',
        ),
        migrations.CreateModel(
            name='InventoryStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_delivery', models.DateField(auto_now_add=True)),
                ('expiration_date', models.DateField()),
                ('count', models.PositiveIntegerField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicines.inventoryitem')),
            ],
        ),
    ]
