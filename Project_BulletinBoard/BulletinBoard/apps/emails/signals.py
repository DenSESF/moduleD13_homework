from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import render_to_string

from BulletinBoard.settings import DEFAULT_FROM_EMAIL

from posts.models import Reply


def send_notify(obj, action):
        template_subject = f'emails/email/{action}_subject.txt'
        template_message = f'emails/email/{action}_message.txt'
        author_dict = {
            'created': obj.advert.author,
            'accept': obj.author,
        }
        context = {
            'reply': obj,
        }
        subject = render_to_string(template_subject, context=None)
        message = render_to_string(template_message, context)

        author_dict.get(action).email_user(
            subject=subject,
            message=message,
            from_email=DEFAULT_FROM_EMAIL,             
        )


@receiver(post_save, sender=Reply)
def notify_new_reply(sender, instance, created, *args, **kwargs):
    if created:
        send_notify(instance, 'created')
    else:
        send_notify(instance, 'accept')
