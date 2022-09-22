# coding=utf-8
import django.forms as django_forms
import urllib.parse
import uuid
from django.contrib.contenttypes.models import ContentType
from django.db.models import ManyToManyField
from xadmin.plugins.quickform import RelatedFieldWidgetWrapper
from xadmin.views.base import BaseAdminPlugin
from xadmin_annotation import settings
from xadmin_annotation.forms.fields import AnnotationField, AnnotationWidget
from xadmin_annotation.models import Annotation


class AnnotationForm(django_forms.ModelForm):
	"""dummy"""
	pass


class AnnotationPlugin(BaseAdminPlugin):
	annotation_model = Annotation

	def init_request(self, *args, **kwargs):
		self.modal_name = f"{self.opts.app_label}.{self.opts.model_name}"
		is_active = False
		for md in settings.ANNOTATION_FOR_MODELS:
			is_active = md.lower() == self.modal_name
			if is_active:
				break
		return is_active

	def setup(self, *args, **kwargs):
		self.annotation_opts = self.annotation_model._meta
		self.rel_field = settings.ANNOTATION_RELATION_FIELD
		self.content_type = ContentType.objects.get_for_model(self.model)
		self.key = str(uuid.uuid4())

	def save_models(self):
		instance = self.admin_view.new_obj
		if instance.pk is not None:
			# relates the key objects to the content being edited.
			key = self.admin_view.form_obj.cleaned_data[self.rel_field]
			queryset = self.annotation_model.objects.filter(
				key=key,
				object_id__isnull=True,
				content_type__isnull=True
			)
			queryset.update(object_id=instance.pk,
			                content_type=self.content_type)

	def get_annotation_queryset(self):
		return self.annotation_model.objects.all()

	def quick_addtn(self, widget):
		"""Create the widget with the quickform plugin button."""
		instance = self.admin_view.org_obj
		add_url = self.admin_view.get_model_url(self.annotation_model, "add")
		rel_add_url = self.admin_view.get_model_url(self.model, "add")
		add_url += "?" + urllib.parse.urlencode({
			"key": self.key,
			'rel_id': instance.pk if instance else '',
			"rel_model": self.modal_name
		})
		return RelatedFieldWidgetWrapper(
			widget,
			ManyToManyField(self.annotation_model).remote_field,
			add_url,
			rel_add_url,
			change_url=None,
			rel_change_url=None,
			request_params=self.request.GET.copy()
		)

	def get_widget_context(self):
		"""Context passed to AnnotationField."""
		context = {
			'url': self.admin_view.get_model_url(self.annotation_model, "changelist"),
			'verbose_name': (getattr(self.annotation_opts, "verbose_name", None) or
			                 self.annotation_opts.model_name.upper()),
			'count': self.get_annotation_queryset().count(),
			'value': self.key
		}
		return context

	def get_media(self, media):
		media += django_forms.Media(js=(
			"annotation/adminx/js/annotation_form_widget.js",
		))
		return media

	def get_form_class(self, form):
		if not isinstance(form, AnnotationForm):
			bases = (AnnotationForm, form)
			widget = self.quick_addtn(AnnotationWidget(attrs=self.get_widget_context()))
			form = type(''.join([f.__name__ for f in bases]), bases, {
				self.rel_field: AnnotationField(widget=widget)
			})
		return form

	def get_form_fields(self, fields):
		return fields
