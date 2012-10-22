# -*- coding: utf-8 -*-
from djangoplugins.point import PluginPoint


class TopicInline(PluginPoint):

    def admin(self):
        return self.inline
