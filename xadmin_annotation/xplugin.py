# coding=utf-8
import django.forms as django_forms
import urllib.parse
import uuid
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.db.models import ManyToManyField
from django.template.loader import render_to_string
from xadmin.filters import FILTER_PREFIX
from xadmin.plugins.quickform import RelatedFieldWidgetWrapper
from xadmin.views import DetailAdminView
from xadmin.views.base import BaseAdminPlugin
from xadmin.views.list import PAGE_VAR
from xadmin_annotation import settings
from xadmin_annotation.forms.fields import AnnotationField, AnnotationWidget
from xadmin_annotation.models import Annotation


class AnnotationForm(django_forms.ModelForm):
	"""dummy"""
	pass


class AnnotationPlugin(BaseAdminPlugin):
	annotation_model = Annotation
	annotation_editable = False

	def init_request(self, *args, **kwargs):
		# Need can see to at least load the list.
		if not self.has_model_perm(self.annotation_model, "view"):
			return False
		self.modal_name = f"{self.opts.app_label}.{self.opts.model_name}"
		is_active = False
		for md in settings.ANNOTATION_FOR_MODELS:
			is_active = md.lower() == self.modal_name
			if is_active:
				break
		return is_active

	def setup(self, *args, **kwargs):
		self.is_detail = isinstance(self.admin_view, DetailAdminView)
		self.is_editable = (self.has_model_perm(self.annotation_model, "add") and not self.is_detail)
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
		rel_add_url = self.admin_view.get_model_url(self.model, "add") if self.annotation_editable else None
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
			request_params=self.request.GET.copy(),
			title_i18n_add=_('Create %s')
		)

	def get_widget_context(self):
		"""Context passed to AnnotationField."""
		instance = self.admin_view.org_obj
		qs = self.get_annotation_queryset()
		if instance:
			# It only counts objects from that instance.
			qs = qs.filter(object_id=instance.pk)
		else:
			qs = qs.filter(key=self.key)
		count = qs.count()
		verbose_name = (getattr(self.annotation_opts, "verbose_name", None) or
		                self.annotation_opts.model_name.upper())
		context = {
			'url': self.admin_view.get_model_url(self.annotation_model, "changelist"),
			'verbose_name': verbose_name,
			'verbose_name_plural': (getattr(self.annotation_opts, "verbose_name_plural", None) or
			                        verbose_name),
			'object_id': instance.pk if instance else '',
			'is_editable': self.is_editable,
			'object_key': self.key,
			'filter_prefix': FILTER_PREFIX,
			'page_param': PAGE_VAR,
			'count': count,
			'value': self.key
		}
		return context

	def get_media(self, media):
		media += django_forms.Media(js=(
			"annotation/adminx/js/annotation_form_widget.js",
		))
		return media

	def get_form_class(self, form):
		if not issubclass(form, AnnotationForm):
			bases = (AnnotationForm, form)
			context = self.get_widget_context()
			widget = AnnotationWidget(attrs=context)
			if self.is_editable:
				widget = self.quick_addtn(widget)
			form = type(''.join([f.__name__ for f in bases]), bases, {
				self.rel_field: AnnotationField(label=context['verbose_name'], widget=widget)
			})
		return form

	def get_field_result(self, result_field, field_name):
		"""Preview of annotations in the details screen"""
		if field_name == self.rel_field and self.is_detail:
			result_field.label = ""
			result_field.allow_tags = True
			result_field.text = render_to_string(
				"annotation/adminx/annotation_form_field.html",
				context={
					'annotation_field': self.admin_view.form_obj[field_name]
				}
			)
		return result_field
