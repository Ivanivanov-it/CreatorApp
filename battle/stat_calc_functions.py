

ATK_ROLES = ["ATTACK","BUFF"]
ATK_TYPES = ["HERO","DEMON","GOD","VILLAIN"]
DEFENSE_ROLES = ["DEFEND","SUPPORT"]
DEFENSE_TYPES = ["ALIEN","ANGEL"]
HP_ROLES = ["HEAL","SEARCH"]
HP_TYPES = ["TIME TRAVELER"]

def calc_buff_atk(obj) -> int:
    result = 0

    for role in obj.roles.all():
        print(role.role)
        if role.role in ATK_ROLES:
            result += 5

    if obj.type in ATK_TYPES:
        result += 5

    return result


def calc_buff_def(obj) -> int:
    result = 0

    for role in obj.roles.all():
        if role.role in DEFENSE_ROLES:
            result += 3

    if obj.type in DEFENSE_TYPES:
        result += 5

    return result


def calc_buff_hp(obj) -> int:
    result = 0
    for role in obj.roles.all():
        if role.role in HP_ROLES:
            result += 50

    if obj.type in HP_TYPES:
        result += 50

    return result