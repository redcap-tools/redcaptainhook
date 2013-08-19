# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'History.name'
        db.delete_column(u'workflow_history', 'name')

        # Deleting field 'History.entity'
        db.delete_column(u'workflow_history', 'entity')

        # Adding field 'History.entity_type'
        db.add_column(u'workflow_history', 'entity_type',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'History.entity_pk'
        db.add_column(u'workflow_history', 'entity_pk',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'History.name'
        db.add_column(u'workflow_history', 'name',
                      self.gf('django.db.models.fields.CharField')(default='name', max_length=50),
                      keep_default=False)

        # Adding field 'History.entity'
        db.add_column(u'workflow_history', 'entity',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Deleting field 'History.entity_type'
        db.delete_column(u'workflow_history', 'entity_type')

        # Deleting field 'History.entity_pk'
        db.delete_column(u'workflow_history', 'entity_pk')


    models = {
        u'workflow.history': {
            'Meta': {'object_name': 'History'},
            'entity_pk': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'entity_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'processes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['workflow.Process']", 'symmetrical': 'False'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workflow.Project']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['workflow']