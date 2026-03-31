from asgiref.sync import sync_to_async

from achievements.models import Achievement, UserAchievement
from common.choices import AchievementType


async def check_condition(achievement,user,stats=None,battle=None,**kwargs):
    checkers = {
        AchievementType.FIRST_WIN: check_first_win,
        AchievementType.WIN_STREAK: check_win_streak,
        AchievementType.FIRST_LOSE: check_first_lose,
        AchievementType.TOTAL_WINS: check_total_wins,
        AchievementType.TOTAL_LOSES: check_total_loses,
        AchievementType.TOTAL_BATTLES: check_total_battles,
        AchievementType.PERFECT_VICTORY: check_perfect_victory,
        AchievementType.FIRST_CHARACTER_CREATION: check_first_character,
        AchievementType.FIRST_PARTNER_CREATION: check_first_partner,
        AchievementType.FIRST_ENEMY_CREATION: check_first_enemy,
        AchievementType.FIRST_CARD_CREATION: check_first_card,
    }
    checker = checkers.get(achievement.type)
    if checker:
        return await checker(achievement,user,stats=stats,battle=battle,**kwargs)
    return False

async def check_first_win(achievement, user, stats=None, **kwargs):
    return stats and stats.wins >= achievement.threshold

async def check_first_lose(achievement, user, stats=None, **kwargs):
    return stats and stats.losses >= achievement.threshold

async def check_win_streak(achievement, user, stats=None, **kwargs):
    return stats and stats.win_streak >= achievement.threshold

async def check_total_wins(achievement, user, stats=None, **kwargs):
    return stats and stats.wins >= achievement.threshold

async def check_total_loses(achievement, user, stats=None, **kwargs):
    return stats and stats.losses >= achievement.threshold

async def check_total_battles(achievement, user, stats=None, **kwargs):
    return stats and (stats.wins + stats.losses) >= achievement.threshold

async def check_perfect_victory(achievement, user, battle=None, **kwargs):
    if not battle:
        return False
    from battle.models import BattleLog
    get_logs = sync_to_async(
        lambda: BattleLog.objects.filter(
            battle=battle,
            content__icontains='Turn 2'
        ).exists()
    )
    took_damage = await get_logs()
    return not took_damage

async def check_first_character(achievement, user, **kwargs):
    from characters.models import Character
    get_count = sync_to_async(
        lambda: Character.objects.filter(creator=user).count()
    )
    return await get_count() >= achievement.threshold

async def check_first_enemy(achievement, user, **kwargs):
    from enemies.models import Enemy
    get_count = sync_to_async(
        lambda: Enemy.objects.filter(creator=user).count()
    )
    return await get_count() >= achievement.threshold

async def check_first_card(achievement, user, **kwargs):
    from cards.models import Card
    get_count = sync_to_async(
        lambda: Card.objects.filter(creator=user).count()
    )
    return await get_count() >= achievement.threshold

async def check_first_partner(achievement, user, **kwargs):
    from partners.models import Partner
    get_count = sync_to_async(
        lambda: Partner.objects.filter(creator=user).count()
    )
    return await get_count() >= achievement.threshold


async def check_and_award_battle_achievements(user,**kwargs):
    get_achievements = sync_to_async(lambda: list(Achievement.objects.all()))
    get_existing = sync_to_async(
        lambda: set(
            UserAchievement.objects.filter(user=user)
            .values_list('achievement_id', flat=True)
        )
    )

    all_achievements, already_earned = await get_achievements(), await get_existing()
    newly_earned = []

    for achievement in all_achievements:
        if achievement.id in already_earned:
            continue

        earned = await check_condition(achievement, user, **kwargs)

        if earned:
            create = sync_to_async(UserAchievement.objects.create)
            await create(user=user, achievement=achievement)
            newly_earned.append(achievement)

    return newly_earned




