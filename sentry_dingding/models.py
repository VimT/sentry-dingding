# coding=utf-8

"""
sentry_dingding.models
~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2011 by VimT, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
import requests
from django import forms
from sentry.plugins.bases.notify import NotifyPlugin
import sentry_dingding


class DingDingOptionsForm(forms.Form):
    endpoint = forms.CharField(help_text="DingDing Endpoint", required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'dingding endpoint'}))


class DingDingMessage(NotifyPlugin):
    author = 'VimT'
    author_url = 'https://github.com/VimT/sentry-dingding'
    version = sentry_dingding.VERSION
    description = "Event notification to DingDing."
    resource_links = [
        ('Bug Tracker', 'https://github.com/VimT/sentry-dingding/issues'),
        ('Source', 'https://github.com/VimT/sentry-dingding'),
    ]
    slug = 'dingding'
    title = 'DingDing'
    conf_title = title
    conf_key = 'dingding'
    project_conf_form = DingDingOptionsForm

    def _bulid_link_message(self, project, error, level, server_name, link, msg):
        title = '[{level}]{project_name}'.format(project_name=project, level=level)

        text = '''{server_name}: {error}'''.format(error=error, server_name=server_name, link=link, )

        result = {"msgtype": "link", "link": {"title": title, "text": text, "messageUrl": link}}

        return result

    def _build_message(self, project, error, level, server_name, link, msg):
        title = '[{level}]{project_name}'.format(project_name=project, level=level)

        text = '''
## [{server_name}]{error}
{msg}
> [Click here to see details]({link})
'''.format(error=error, level=level, msg=msg, server_name=server_name, link=link, )

        result = {"msgtype": "markdown", "markdown": {"title": title, "text": text, }}

        return result

    def is_configured(self, project):
        return bool(self.get_option('endpoint', project))

    def notify_users(self, group, event, fail_silently=False):
        project = event.project
        level = group.get_level_display().upper()
        link = group.get_absolute_url()
        endpoint = self.get_option('endpoint', project)
        server_name = event.get_tag('server_name')
        title = event.title
        msg = event.message
        data = self._build_message(project, title, level, server_name, link, msg)
        self.send_payload(
            endpoint=endpoint,
            data=data
        )

    def send_payload(self, endpoint, data):
        requests.post(
            endpoint,
            json=data,
        )
