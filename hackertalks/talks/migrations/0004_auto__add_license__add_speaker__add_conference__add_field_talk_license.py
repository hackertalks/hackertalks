# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'License'
        db.create_table('talks_license', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('url', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('talks', ['License'])

        # Adding model 'Speaker'
        db.create_table('talks_speaker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=100, populate_from=None, unique_with=(), db_index=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('talks', ['Speaker'])

        # Adding model 'Conference'
        db.create_table('talks_conference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=100, populate_from=None, unique_with=(), db_index=True)),
            ('admin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('talks', ['Conference'])

        # Adding field 'Talk.license'
        db.add_column('talks_talk', 'license', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['talks.License'], to_field='abbreviation', null=True), keep_default=False)

        # Adding field 'Talk.description'
        db.add_column('talks_talk', 'description', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Adding field 'Talk.conference'
        db.add_column('talks_talk', 'conference', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['talks.Conference'], null=True), keep_default=False)

        # Adding field 'Talk.duration'
        db.add_column('talks_talk', 'duration', self.gf('django.db.models.fields.TimeField')(default='asdf'), keep_default=False)

        # Adding field 'Talk.video_embedcode'
        db.add_column('talks_talk', 'video_embedcode', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Adding field 'Talk.video_bliptv_id'
        db.add_column('talks_talk', 'video_bliptv_id', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'License'
        db.delete_table('talks_license')

        # Deleting model 'Speaker'
        db.delete_table('talks_speaker')

        # Deleting model 'Conference'
        db.delete_table('talks_conference')

        # Deleting field 'Talk.license'
        db.delete_column('talks_talk', 'license_id')

        # Deleting field 'Talk.description'
        db.delete_column('talks_talk', 'description')

        # Deleting field 'Talk.conference'
        db.delete_column('talks_talk', 'conference_id')

        # Deleting field 'Talk.duration'
        db.delete_column('talks_talk', 'duration')

        # Deleting field 'Talk.video_embedcode'
        db.delete_column('talks_talk', 'video_embedcode')

        # Deleting field 'Talk.video_bliptv_id'
        db.delete_column('talks_talk', 'video_bliptv_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'talks.conference': {
            'Meta': {'object_name': 'Conference'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '100', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'})
        },
        'talks.license': {
            'Meta': {'object_name': 'License'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        'talks.speaker': {
            'Meta': {'object_name': 'Speaker'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '100', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        'talks.talk': {
            'Meta': {'object_name': 'Talk'},
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['talks.Conference']", 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'duration': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['talks.License']", 'to_field': "'abbreviation'", 'null': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '100', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'video_bliptv_id': ('django.db.models.fields.TextField', [], {}),
            'video_embedcode': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['talks']
