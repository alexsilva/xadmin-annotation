# coding=utf-8
from django.conf import settings
from django.utils.module_loading import import_string

# Models with reverse relationship registration
ANNOTATION_RELATION_FIELD = getattr(settings, "ANNOTATION_RELATION_FIELD", 'annotations')
ANNOTATION_FOR_MODELS = getattr(settings, "ANNOTATION_FOR_MODELS", [])
ANNOTATION_ADMINX_BASE = getattr(settings, "ANNOTATION_ADMINX_BASE", object)

if isinstance(ANNOTATION_ADMINX_BASE, str):
	ANNOTATION_ADMINX_BASE = import_string(ANNOTATION_ADMINX_BASE)
