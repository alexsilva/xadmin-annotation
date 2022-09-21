# coding=utf-8
import warnings
from django.apps import apps
from django.contrib.contenttypes.fields import GenericRelation
from xadmin_annotation.models import Annotation
from xadmin_annotation import settings


def register_models(*models):
	"""Registers models that receive annotation"""
	for model in models:
		try:
			app_label, model_name = model.split(".", 1)
		except ValueError as exc:
			warnings.warn(f"invalid model '{model}', expected 'app_label.model_name'",
			              RuntimeWarning)
			continue
		# with the reverse relationship it is possible to create annotations in the generic model
		model = apps.get_model(app_label, model_name)
		relation = GenericRelation(Annotation)
		relation.contribute_to_class(model, settings.ANNOTATION_RELATION_FIELD)
