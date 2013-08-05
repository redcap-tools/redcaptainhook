# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'History'
        db.create_table(u'workflow_history', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('entity', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'workflow', ['History'])

        # Adding field 'Trigger.name'
        db.add_column(u'workflow_trigger', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
                      keep_default=False)


        # Changing field 'Project.name'
        db.alter_column(u'workflow_project', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))

    def backwards(self, orm):
        # Deleting model 'History'
        db.delete_table(u'workflow_history')

        # Deleting field 'Trigger.name'
        db.delete_column(u'workflow_trigger', 'name')


        # Changing field 'Project.name'
        db.alter_column(u'workflow_project', 'name', self.gf('django.db.models.fields.CharField')(max_length=20))

    models = {
        u'workflow.history': {
            'Meta': {'object_name': 'History'},
            'entity': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'workflow.process': {
            'Meta': {'object_name': 'Process'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'fname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'qname': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'workflow.project': {
            'Meta': {'ordering': "['redcap_pid']", 'unique_together': "(('site', 'redcap_pid'),)", 'object_name': 'Project'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'redcap_pid': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'site': ('django.db.models.fields.CharField', [], {'default': "'vanderbilt'", 'max_length': '40'})
        },
        u'workflow.trigger': {
            'Meta': {'object_name': 'Trigger'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dag': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'form': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'processes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['workflow.Process']", 'symmetrical': 'False'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workflow.Project']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['workflow']