from asgiref.sync import sync_to_async

from achievements.models import Achievement, UserAchievement
from common.choices import AchievementType


async def check_and_award_battle_achievements(user,stats,battle=None):
    newly_earned = []

    get_achievements = sync_to_async(
        lambda: list(Achievement.objects.all())
    )

    get_existing = sync_to_async(
        lambda: set(
            UserAchievement.objects.filter(user=user)
            .values_list('achievement_id', flat=True)
        )
    )

    all_achievements = await get_achievements()
    already_earned = await get_existing()
    total_battles = stats.wins + stats.losses

    for achievement in all_achievements:
        if achievement.id in already_earned:
            continue

        earned = False

        if achievement.type == AchievementType.FIRST_WIN:
            earned = stats.wins >= achievement.threshold
        elif achievement.type == AchievementType.FIRST_LOSE:
            earned = stats.losses >= achievement.threshold
        elif achievement.type == AchievementType.TOTAL_WINS:
            earned = stats.wins >= achievement.threshold
        elif achievement.type == AchievementType.TOTAL_LOSES:
            earned = stats.losses >= achievement.threshold
        elif achievement.type == AchievementType.TOTAL_BATTLES:
            earned = total_battles >= achievement.threshold
        elif achievement.type == AchievementType.WIN_STREAK:
            earned = stats.win_streak >= achievement.threshold
        elif achievement.type == AchievementType.PERFECT_VICTORY and battle:
            earned = await check_perfect_victory(battle)

        if earned:
            award = sync_to_async(UserAchievement.objects.create)
            await award(user=user,achievement=achievement)
            newly_earned.append(achievement)
    return newly_earned

#This is cooked I need to think of a better logic for this later.

async def check_perfect_victory(battle):
    from battle.models import BattleLog

    get_damage_logs = sync_to_async(
        lambda: BattleLog.objects.filter(battle=battle,
                                         content__icontains="Turn 2").exists()
    )
    took_damage = await get_damage_logs()
    return not took_damage

# async def check_perfect_lose(battle):
#     from battle.models import BattleLog
#
#     get_damage_logs = sync_to_async(
#         lambda: BattleLog.objects.filter(battle=battle,
#                                          content__icontains="Turn 2").exists()
#     )
#     took_damage = await get_damage_logs()
#     return not took_damage


