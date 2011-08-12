# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'Talk', fields ['slug']
        db.create_unique('talks_talk', ['slug'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Talk', fields ['slug']
        db.delete_unique('talks_talk', ['slug'])


    models = {
        'talks.talk': {
            'Meta': {'object_name': 'Talk'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['talks']
