from django.db import migrations
from django.contrib.auth.models import UserManager

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', UserManager()),
            ],
        ),
    ]
