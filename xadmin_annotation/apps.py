# coding=utf-8
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AnnotationConfig(AppConfig):
	"""Configurações do app publique"""
	name = 'xadmin_annotation'
	verbose_name = _("Annotation")

	def ready(self):
		from xadmin_annotation import settings as annotation_settings
		from xadmin_annotation.register import register_models
		register_models(*annotation_settings.ANNOTATION_FOR_MODELS)
