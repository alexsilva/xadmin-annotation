# coding=utf-8
import django.forms as django_forms
from xadmin.sites import register
from xadmin.sites import site
from xadmin.views.edit import ModelFormAdminView
from xadmin_annotation import settings
from xadmin_annotation.models import Annotation
from xadmin_annotation.xplugin import AnnotationPlugin
from django.contrib.auth import get_user_model

User = get_user_model()

# create / update
site.register_plugin(AnnotationPlugin, ModelFormAdminView)


@register(Annotation)
class AnnotationAdmin:
	hidden_menu = True
	exclude = ('user',)
	formfield_widgets = {
		'key': django_forms.HiddenInput
	}
	fields = (
		'key',
		'description',
	)

	def get_form_datas(self):
		data = super().get_form_datas()
		if self.request_method == 'get':
			key = self.request.GET['key']
			initial = data.setdefault("initial", {})
			initial[settings.ANNOTATION_RELATION_FIELD] = key
		return data

	def save_forms(self):
		res = super().save_forms()
		instance = self.new_obj
		self.new_obj.key = self.form_obj.cleaned_data['key']
		if instance.user is None:
			instance.user = self.request.user
		return res
