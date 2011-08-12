# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Talk.slug'
        db.alter_column('talks_talk', 'slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=100, populate_from=None, unique_with=()))


    def backwards(self, orm):
        
        # Changing field 'Talk.slug'
        db.alter_column('talks_talk', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=100, unique=True))


    models = {
        'talks.talk': {
            'Meta': {'object_name': 'Talk'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '100', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['talks']
