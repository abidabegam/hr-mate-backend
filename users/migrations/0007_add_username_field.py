from django.db import migrations, models
import django.contrib.auth.validators

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20250415_1707'),  # Ensure this matches your latest migration
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(
                max_length=150,
                unique=True,
                help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                verbose_name='username',
                default='temp_username'  # Temporary default; update this later if needed.
            ),
            preserve_default=False,
        ),
    ]
