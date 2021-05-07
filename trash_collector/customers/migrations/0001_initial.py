
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('pickup_day', models.CharField(blank=True, max_length=10, null=True)),
                ('one_time_pickup', models.DateField(blank=True, null=True)),
                ('account_balance', models.FloatField(default=0.0)),
                ('suspension', models.BooleanField(default=False)),
                ('suspension_end', models.DateField(blank=True, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
