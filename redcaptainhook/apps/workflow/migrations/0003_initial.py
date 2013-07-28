# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Trigger'
        db.create_table(u'workflow_trigger', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('form', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('event', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('dag', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflow.Project'])),
        ))
        db.send_create_signal(u'workflow', ['Trigger'])

        # Adding M2M table for field processes on 'Trigger'
        m2m_table_name = db.shorten_name(u'workflow_trigger_processes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('trigger', models.ForeignKey(orm[u'workflow.trigger'], null=False)),
            ('process', models.ForeignKey(orm[u'workflow.process'], null=False))
        ))
        db.create_unique(m2m_table_name, ['trigger_id', 'process_id'])

        # Adding model 'Project'
        db.create_table(u'workflow_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('site', self.gf('django.db.models.fields.CharField')(default='vanderbilt', max_length=40)),
            ('redcap_pid', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hash', self.gf('django.db.models.fields.CharField')(default=None, max_length=50)),
        ))
        db.send_create_signal(u'workflow', ['Project'])

        # Adding unique constraint on 'Project', fields ['site', 'redcap_pid']
        db.create_unique(u'workflow_project', ['site', 'redcap_pid'])

        # Adding model 'Process'
        db.create_table(u'workflow_process', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('qname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('fname', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'workflow', ['Process'])


    def backwards(self, orm):
        # Removing unique constraint on 'Project', fields ['site', 'redcap_pid']
        db.delete_unique(u'workflow_project', ['site', 'redcap_pid'])

        # Deleting model 'Trigger'
        db.delete_table(u'workflow_trigger')

        # Removing M2M table for field processes on 'Trigger'
        db.delete_table(db.shorten_name(u'workflow_trigger_processes'))

        # Deleting model 'Project'
        db.delete_table(u'workflow_project')

        # Deleting model 'Process'
        db.delete_table(u'workflow_process')


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
            'hash': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'redcap_pid': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'site': ('django.db.models.fields.CharField', [], {'default': "'vanderbilt'", 'max_length': '40'})
        },
        u'workflow.trigger': {
            'Meta': {'object_name': 'Trigger'},
            'dag': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'form': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'processes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['workflow.Process']", 'symmetrical': 'False'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workflow.Project']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['workflow']