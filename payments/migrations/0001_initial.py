# Generated by Django 4.1.5 on 2023-01-27 10:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id_merchant', models.CharField(blank=True, default=uuid.uuid4, help_text='The Payment ID by which the Razorpay refers', max_length=250, null=True)),
                ('order_id_merchant', models.CharField(blank=True, help_text='The Order ID by which the Razorpay refers', max_length=250, null=True)),
                ('amount', models.IntegerField()),
                ('payment_status', models.CharField(choices=[('P', 'Pending'), ('F', 'Failed'), ('S', 'Success'), ('R', 'Refund Done')], default='P', help_text='The status of payment', max_length=250)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('order', models.ForeignKey(help_text='The order ID by which the system refers', on_delete=django.db.models.deletion.CASCADE, to='main.order')),
            ],
            options={
                'verbose_name_plural': 'Payments',
                'ordering': ('-created_at',),
            },
        ),
    ]