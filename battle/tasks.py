
from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task(bind=True, max_retries=3)
def send_battle_report(self, battle_id, user_id):
    try:
        from .models import Battle, BattleLog
        from django.contrib.auth import get_user_model

        User = get_user_model()
        battle = Battle.objects.get(pk=battle_id)
        user = User.objects.get(pk=user_id)

        if not user.email:
            return

        logs = list(BattleLog.objects.filter(battle=battle).order_by('id'))
        character = battle.battlecharacter_set.select_related('character').first()
        enemy = battle.battleenemy_set.select_related('enemy').first()
        result = 'Victory' if character.is_alive else 'Defeat'

        context = {
            'user': user,
            'battle': battle,
            'character': character,
            'enemy': enemy,
            'logs': logs,
            'result': result,
        }

        html_message  = render_to_string('battle/email/battle_report.html', context)
        plain_message = render_to_string('battle/email/battle_report.txt',  context)



        email = EmailMultiAlternatives(
            subject=f'Battle #{battle.id} Report — {result}!',
            body=plain_message,
            from_email=None,
            to=[user.email],
        )
        email.attach_alternative(html_message, 'text/html')
        email.send()


    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)