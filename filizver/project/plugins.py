# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
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
