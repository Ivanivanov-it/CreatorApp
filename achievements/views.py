

from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView

from achievements.models import UserAchievement, Achievement


# Create your views here.


class AchievementListView(LoginRequiredMixin,ListView):
    template_name = 'achievements/achievements.html'
    extra_context = {
        'page_title': 'User Achievements',
    }
    context_object_name = 'user_achievements'

    def get_queryset(self):
        return UserAchievement.objects.filter(user=self.request.user).select_related('achievement').order_by('-achieved')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        earned_ids = self.get_queryset().values_list('achievement_id', flat=True)

        context['locked_achievements'] = Achievement.objects.exclude(
            id__in=earned_ids
        )
        return context