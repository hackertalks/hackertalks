# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UserProfile'
        db.create_table('backend_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('api_key', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('backend', ['UserProfile'])


    def backwards(self, orm):
        
        # Deleting model 'UserProfile'
        db.delete_table('backend_userprofile')


    models = {
        'backend.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'api_key': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['backend']
