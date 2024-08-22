from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.urls import reverse
from .models import Task


@shared_task
def send_deadline_reminders():
    now = timezone.now()
    upcoming_tasks = Task.objects.filter(d_time__gt=now, d_time__lt=now + timezone.timedelta(days=1))
    for task in upcoming_tasks:
        subject = f"Напоминание: приближается срок выполнения задачи {task.title}"
        message = f"Задача {task.title} должна быть выполнена к {task.d_time}.\n" \
                  f"Ссылка на задачу: {reverse('more_details', args=[task.pk])}"

        # Отправка уведомлений всем членам команды
        team_members = task.project.team.members.all()
        recipient_list = [member.email for member in team_members if member.email]

        send_mail(subject, message, 'fediazubikof@gmail.com', recipient_list)
