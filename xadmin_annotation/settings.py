# coding=utf-8
from django.conf import settings

# Models with reverse relationship registration
ANNOTATION_RELATION_FIELD = getattr(settings, "ANNOTATION_RELATION_FIELD", 'annotations')
ANNOTATION_FOR_MODELS = getattr(settings, "ANNOTATION_FOR_MODELS", [])
ANNOTATION_ADMINX_BASE = getattr(settings, "ANNOTATION_ADMINX_BASE", object)

