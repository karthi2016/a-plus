# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.utils import timezone


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Course'
        db.create_table('course_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
        ))
        db.send_create_signal('course', ['Course'])

        # Adding M2M table for field teachers on 'Course'
        db.create_table('course_course_teachers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm['course.course'], null=False)),
            ('userprofile', models.ForeignKey(orm['userprofile.userprofile'], null=False))
        ))
        db.create_unique('course_course_teachers', ['course_id', 'userprofile_id'])

        # Adding model 'CourseInstance'
        db.create_table('course_courseinstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instance_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=30, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('starting_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('ending_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='instances', to=orm['course.Course'])),
        ))
        db.send_create_signal('course', ['CourseInstance'])

        # Adding unique constraint on 'CourseInstance', fields ['course', 'url']
        db.create_unique('course_courseinstance', ['course_id', 'url'])

        # Adding M2M table for field assistants on 'CourseInstance'
        db.create_table('course_courseinstance_assistants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('courseinstance', models.ForeignKey(orm['course.courseinstance'], null=False)),
            ('userprofile', models.ForeignKey(orm['userprofile.userprofile'], null=False))
        ))
        db.create_unique('course_courseinstance_assistants', ['courseinstance_id', 'userprofile_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'CourseInstance', fields ['course', 'url']
        db.delete_unique('course_courseinstance', ['course_id', 'url'])

        # Deleting model 'Course'
        db.delete_table('course_course')

        # Removing M2M table for field teachers on 'Course'
        db.delete_table('course_course_teachers')

        # Deleting model 'CourseInstance'
        db.delete_table('course_courseinstance')

        # Removing M2M table for field assistants on 'CourseInstance'
        db.delete_table('course_courseinstance_assistants')


    models = {
        'apps.baseplugin': {
            'Meta': {'object_name': 'BasePlugin'},
            'container_pk': ('django.db.models.fields.TextField', [], {}),
            'container_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'modelwithinheritance_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['inheritance.ModelWithInheritance']", 'unique': 'True', 'primary_key': 'True'}),
            'oauth_consumer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oauth_provider.Consumer']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'timezone.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'timezone.now'}),
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
        'course.course': {
            'Meta': {'object_name': 'Course'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'teachers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'teaching_courses'", 'blank': 'True', 'to': "orm['userprofile.UserProfile']"}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'})
        },
        'course.courseinstance': {
            'Meta': {'unique_together': "(('course', 'url'),)", 'object_name': 'CourseInstance'},
            'assistants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'assisting_courses'", 'blank': 'True', 'to': "orm['userprofile.UserProfile']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'instances'", 'to': "orm['course.Course']"}),
            'ending_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'starting_time': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '30', 'blank': 'True'})
        },
        'inheritance.modelwithinheritance': {
            'Meta': {'object_name': 'ModelWithInheritance'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'oauth_provider.consumer': {
            'Meta': {'object_name': 'Consumer'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'userprofile.userprofile': {
            'Meta': {'ordering': "['id']", 'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'default': "'en_US'", 'max_length': '5'}),
            'student_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['course']