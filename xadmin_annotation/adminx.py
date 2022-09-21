# coding=utf-8
from xadmin.sites import register
from xadmin.sites import site
from xadmin.views.edit import ModelFormAdminView
from xadmin_annotation.models import Annotation
from xadmin_annotation.xplugin import AnnotationPlugin

# create / update
site.register_plugin(AnnotationPlugin, ModelFormAdminView)


@register(Annotation)
class AnnotationAdmin:
	hidden_menu = True
