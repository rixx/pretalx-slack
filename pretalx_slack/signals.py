import json

import requests
from django.conf import settings
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from pretalx.submission.signals import submission_state_change

webhook = settings.CONFIG.get('slack', 'webhook_url')


@receiver(submission_state_change, dispatch_uid='pretalx_slack')
def submission_state_change(sender, old_state, submission, user, **kwargs):
    if not webhook:
        print('no webhook url available')
        return

    try:
        text = _(
            'Submission <{url}|»{title}«> has been changed from {old_state} to {new_state} by {name}.'
        ).format(
            url=submission.orga_urls.base.full(),
            title=submission.title,
            old_state=old_state,
            new_state=submission.state,
            name=user.name,
        )
        requests.post(
            webhook,
            headers={'Content-type': 'application/json'},
            data=json.dumps({'text': text}),
        )
    except Exception as e:
        print(e)
