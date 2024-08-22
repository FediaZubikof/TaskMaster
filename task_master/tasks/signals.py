from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse
from .models import Task


# @receiver(post_save, sender=Task)
def send_task_notification(sender, instance, created, **kwargs):
    if created:
        subject = f"Новая задача: {instance.title}"
        message = f"Была создана новая задача в проекте {instance.project.name}.\n" \
                  f"Описание: {instance.description}\n" \
                  f"Срок выполнения: {instance.d_time}\n" \
                  f"Ссылка на задачу: {reverse('more_details', args=[instance.pk])}"
    else:
        subject = f"Обновление задачи: {instance.title}"
        message = f"Задача {instance.title} была обновлена.\n" \
                  f"Новое описание: {instance.description}\n" \
                  f"Новый срок выполнения: {instance.d_time}\n" \
                  f"Ссылка на задачу: {reverse('more_details', args=[instance.pk])}"

    # Отправка уведомлений всем членам команды
    team_members = instance.project.team.members.all()
    recipient_list = [member.email for member in team_members if member.email]

    send_mail(subject, message, 'fediazubikof@gmail.com', recipient_list)
