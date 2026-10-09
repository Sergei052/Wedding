from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0003_rsvp_coming_alone_rsvp_has_companion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rsvp',
            name='coming_alone',
        ),
        migrations.AlterField(
            model_name='rsvp',
            name='has_companion',
            field=models.BooleanField(default=False, verbose_name='Будет сопровождающий'),
        ),
    ]