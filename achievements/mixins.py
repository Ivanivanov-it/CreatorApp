from django.contrib import messages


class AchievementMixin:
    def form_valid(self, form):
        response = super().form_valid(form)
        newly_earned = getattr(self.object, 'newly_earned', [])

        for achievement in newly_earned:

            messages.success(
                self.request,
                f'{achievement.icon}|{achievement.name}|{achievement.description}'
            )

        return response