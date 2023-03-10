# Generated by Django 4.1.1 on 2022-10-11 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='sondage',
        ),
        migrations.RemoveField(
            model_name='questionresponse',
            name='question',
        ),
        migrations.RemoveField(
            model_name='questionresponse',
            name='response',
        ),
        migrations.RemoveField(
            model_name='response',
            name='person',
        ),
        migrations.RemoveField(
            model_name='response',
            name='sondage',
        ),
        migrations.RemoveField(
            model_name='responseproposal',
            name='question',
        ),
        migrations.RemoveField(
            model_name='sondage',
            name='author',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='QuestionResponse',
        ),
        migrations.DeleteModel(
            name='Response',
        ),
        migrations.DeleteModel(
            name='ResponseProposal',
        ),
        migrations.DeleteModel(
            name='Sondage',
        ),
    ]
