# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Record.template'
        db.add_column('forms_custom_record', 'template',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['forms_custom.Template']),
                      keep_default=False)

        # Adding field 'Record.completed'
        db.add_column('forms_custom_record', 'completed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Record.template'
        db.delete_column('forms_custom_record', 'template_id')

        # Deleting field 'Record.completed'
        db.delete_column('forms_custom_record', 'completed')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)"},
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
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'esign': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forms_custom.Template']"}),
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
            'Meta': {'object_name': 'Template', 'ordering': "('-cdt',)"},
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
            'tag': ('django.db.models.fields.SlugField', [], {'default': "'2014_04_30_19_43_50_080171'", 'max_length': '100'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forms_custom.Template']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'user.district': {
            'Meta': {'object_name': 'District', 'ordering': "('name_district',)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_district': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        'user.locality': {
            'Meta': {'object_name': 'Locality', 'ordering': "('district', 'name')"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'", 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['user.Locality']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'", 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        }
    }

    complete_apps = ['forms_custom']