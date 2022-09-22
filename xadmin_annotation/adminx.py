# coding=utf-8
import django.forms as django_forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.formats import date_format
from xadmin.sites import register
from xadmin.sites import site
from xadmin.views.edit import ModelFormAdminView
from xadmin_annotation import settings
from xadmin_annotation.models import Annotation
from xadmin_annotation.xplugin import AnnotationPlugin
from django.contrib.auth import get_user_model
from django.apps import apps

User = get_user_model()

# create / update
site.register_plugin(AnnotationPlugin, ModelFormAdminView)


@register(Annotation)
class AnnotationAdmin:
	hidden_menu = True
	exclude = ('user',)
	list_filter = ('object_id', 'key')
	search_fields = (
		"description",
	)
	formfield_widgets = {
		'key': django_forms.HiddenInput,
		'object_id': django_forms.HiddenInput,
		'content_type': django_forms.HiddenInput
	}
	fields = (
		'key',
		'object_id',
		'content_type',
		'description',
	)

	def tb_created(self, instance):
		"""Formatted creation date"""
		return date_format(instance.created_at)
	tb_created.short_description = _("creation date")
	tb_created.admin_order_field = "created_dt"
	tb_created.is_column = True

	def _get_initial_object(self):
		initial = {}
		try:
			rel_id = self.request.GET["rel_id"]
		except KeyError:
			return initial
		field = self.opts.get_field('object_id')
		try:
			initial['object_id'] = field.to_python(rel_id)
		except ValidationError:
			return initial
		try:
			rel_model = self.request.GET["rel_model"]
		except KeyError:
			return initial
		model = apps.get_model(*rel_model.split('.', 1))
		initial['content_type'] = ContentType.objects.get_for_model(model)
		return initial

	def get_field_attrs(self, db_field, **kwargs):
		attrs = super().get_field_attrs(db_field, **kwargs)
		if db_field.name in self.formfield_widgets.keys():
			attrs['required'] = False
		return attrs

	def get_form_datas(self):
		data = super().get_form_datas()
		if self.request_method == 'get':
			key = self.request.GET['key']
			initial = data.setdefault("initial", {})
			initial[settings.ANNOTATION_RELATION_FIELD] = key
			initial.update(self._get_initial_object())
		return data

	def save_forms(self):
		res = super().save_forms()
		instance = self.new_obj
		if self.new_obj.key is None:
			self.new_obj.key = self.form_obj.cleaned_data['key']
		if instance.user is None:
			instance.user = self.request.user
		return res
