# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Project.site'
        db.add_column(u'workflow_project', 'site',
                      self.gf('django.db.models.fields.CharField')(default='vanderbilt', max_length=40),
                      keep_default=False)

        # Adding unique constraint on 'Project', fields ['site', 'redcap_pid']
        db.create_unique(u'workflow_project', ['site', 'redcap_pid'])


    def backwards(self, orm):
        # Removing unique constraint on 'Project', fields ['site', 'redcap_pid']
        db.delete_unique(u'workflow_project', ['site', 'redcap_pid'])

        # Deleting field 'Project.site'
        db.delete_column(u'workflow_project', 'site')


    models = {
        u'workflow.process': {
            'Meta': {'object_name': 'Process'},
            'fname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'qname': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'workflow.project': {
            'Meta': {'ordering': "['redcap_pid']", 'unique_together': "(('site', 'redcap_pid'),)", 'object_name': 'Project'},
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'redcap_pid': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'site': ('django.db.models.fields.CharField', [], {'default': "'vanderbilt'", 'max_length': '40'})
        },
        u'workflow.trigger': {
            'Meta': {'object_name': 'Trigger'},
            'dag': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'form': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'processes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['workflow.Process']", 'symmetrical': 'False'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workflow.Project']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['workflow']