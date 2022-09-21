# coding=utf-8
import django.forms as django_forms


class AnnotationWidget(django_forms.TextInput):
	input_type = 'hidden'
	template_name = 'annotation/adminx/annotation_form_widget.html'


class AnnotationField(django_forms.Field):
	widget = AnnotationWidget
