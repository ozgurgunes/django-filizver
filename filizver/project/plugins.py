# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from filizver.core.plugins import MenuPoint
from filizver.topic.plugins import TopicPoint
from forms import ProjectForm
from admin import ProjectInline

class ProjectTopic(TopicPoint):
    name = 'project'
    title = 'Project'
    form_class = ProjectForm
    admin_inline = ProjectInline
    #link = reverse('project:project_create')
        
    def create(self, request):
        return super(ProjectTopic, self).create(request)

class ProjectMenu(MenuPoint):
    name = 'project-menu'
    title = 'Project Menu'

    def get_link(self):
        return reverse('project:project_list')

    def get_label(self):
        return _('Projects')
