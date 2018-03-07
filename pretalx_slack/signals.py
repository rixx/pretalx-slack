from django.dispatch import receiver

from pretalx.submission.signals import submission_state_change


@receiver(submission_state_change, dispatch_uid='pretalx_slack')
def submission_state_change(sender, old_state, submission, user, **kwargs):
    print(f'I see you went from {old_state} to {submission.state}, {user.name}')
