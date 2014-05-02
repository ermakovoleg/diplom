# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Template'
        db.create_table('forms_custom_template', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('url', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
            ('cdt', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('group_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user.MyGroup'])),
            ('tableview', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('forms_custom', ['Template'])

        # Adding model 'TemplateField'
        db.create_table('forms_custom_templatefield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forms_custom.Template'])),
            ('tag', self.gf('django.db.models.fields.SlugField')(default='2014_04_30_19_42_58_579187', max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('tab', self.gf('django.db.models.fields.IntegerField')(default=999)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('forms_custom', ['TemplateField'])

        # Adding unique constraint on 'TemplateField', fields ['template', 'tag']
        db.create_unique('forms_custom_templatefield', ['template_id', 'tag'])

        # Adding model 'FieldParameter'
        db.create_table('forms_custom_fieldparameter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forms_custom.TemplateField'])),
            ('tag', self.gf('django.db.models.fields.SlugField')(max_length=10)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('forms_custom', ['FieldParameter'])

        # Adding unique constraint on 'FieldParameter', fields ['field', 'tag', 'value']
        db.create_unique('forms_custom_fieldparameter', ['field_id', 'tag', 'value'])

        # Adding model 'Record'
        db.create_table('forms_custom_record', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cdt', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user.MyUser'])),
            ('esign', self.gf('django.db.models.fields.CharField')(default='', max_length=2000)),
        ))
        db.send_create_signal('forms_custom', ['Record'])

        # Adding model 'RecordData'
        db.create_table('forms_custom_recorddata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forms_custom.Record'])),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forms_custom.TemplateField'])),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('forms_custom', ['RecordData'])


    def backwards(self, orm):
        # Removing unique constraint on 'FieldParameter', fields ['field', 'tag', 'value']
        db.delete_unique('forms_custom_fieldparameter', ['field_id', 'tag', 'value'])

        # Removing unique constraint on 'TemplateField', fields ['template', 'tag']
        db.delete_unique('forms_custom_templatefield', ['template_id', 'tag'])

        # Deleting model 'Template'
        db.delete_table('forms_custom_template')

        # Deleting model 'TemplateField'
        db.delete_table('forms_custom_templatefield')

        # Deleting model 'FieldParameter'
        db.delete_table('forms_custom_fieldparameter')

        # Deleting model 'Record'
        db.delete_table('forms_custom_record')

        # Deleting model 'RecordData'
        db.delete_table('forms_custom_recorddata')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'forms_custom.fieldparameter': {
            'Meta': {'unique_together': "(('field', 'tag', 'value'),)", 'object_name': 'FieldParameter'},
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forms_custom.TemplateField']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.SlugField', [], {'max_length': '10'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'forms_custom.record': {
            'Meta': {'object_name': 'Record'},
            'cdt': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'esign': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['user.MyUser']"})
        },
        'forms_custom.recorddata': {
            'Meta': {'object_name': 'RecordData'},
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forms_custom.TemplateField']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forms_custom.Record']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'forms_custom.template': {
            'Meta': {'ordering': "('-cdt',)", 'object_name': 'Template'},
            'cdt': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'group_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['user.MyGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tableview': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'forms_custom.templatefield': {
            'Meta': {'unique_together': "(('template', 'tag'),)", 'object_name': 'TemplateField'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tab': ('django.db.models.fields.IntegerField', [], {'default': '999'}),
            'tag': ('django.db.models.fields.SlugField', [], {'default': "'2014_04_30_19_42_58_596188'", 'max_length': '100'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forms_custom.Template']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'user.district': {
            'Meta': {'ordering': "('name_district',)", 'object_name': 'District'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_district': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        'user.locality': {
            'Meta': {'ordering': "('district', 'name')", 'object_name': 'Locality'},
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['user.District']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'user.mygroup': {
            'Meta': {'object_name': 'MyGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'})
        },
        'user.myuser': {
            'Meta': {'object_name': 'MyUser'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['user.Locality']", 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        }
    }

    complete_apps = ['forms_custom']