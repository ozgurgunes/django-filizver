# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (View, ListView, DetailView, FormView, CreateView,
                                    UpdateView, DeleteView)
from django.shortcuts import redirect
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, resolve, reverse_lazy
from django.db.models import Count

from manifest.accounts.views import LoginRequiredMixin
from filizver.core.views import ExtraContextMixin, JSONResponseMixin

from filizver.topic import views
from models import Board
from forms import BoardForm
from plugins import BoardTopic


class BoardList(views.TopicList):

    queryset = Board.objects.select_related(
                    'topic__user__profile'
                ).all()
    template_name = "board/board_list.html"
    

class BoardDetail(views.TopicDetail):

    queryset = Board.objects.select_related('topic__user__profile').all()
    template_name = "board/board_detail.html"
    

class BoardCreate(views.TopicCreate):

    form_class = BoardForm
    template_name = "board/board_form.html"
    plugin = BoardTopic
    

class BoardUpdate(views.TopicUpdate):

    model = Board
    form_class = BoardForm
    template_name = "board/board_form.html"
    plugin = BoardTopic


class BoardDelete(views.TopicDelete):

    model = Board

    def get_success_url(self):
        return reverse('board:board_list')
