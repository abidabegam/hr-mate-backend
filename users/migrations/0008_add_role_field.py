from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_add_username_field'),  # Adjust this if your last migration is named differently.
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(
                max_length=20,
                choices=[('ADMIN', 'Administrator'), ('HR', 'Human Resources'), ('EMPLOYEE', 'Employee')],
                default='EMPLOYEE',
            ),
        ),
    ]
