"""Darkest Fantasy data assets."""

HOME_IMAGES = {
    'arthur': (
        './img/Chars/Arthur/arthur_fb.png',
        './img/Chars/Arthur/arthur_fb_s.png',
    ),
    'merlin': (
        './img/Chars/Merlin/merlin_fb.png',
        './img/Chars/Merlin/merlin_fb_s.png',
    ),
}
ABILITIES = {
    'arthur': (
        (
            './img/Chars/Arthur/arthur_a_1.png',
            './img/Chars/Arthur/arthur_a_1d.png',
        ),
        (
            './img/Chars/Arthur/arthur_a_2.png',
            './img/Chars/Arthur/arthur_a_2d.png',
        ),
    ),
    'merlin': (
        (
            './img/Chars/Merlin/merlin_a_1.png',
            './img/Chars/Merlin/merlin_a_1d.png',
        ),
        (
            './img/Chars/Merlin/merlin_a_2.png',
            './img/Chars/Merlin/merlin_a_2d.png',
        ),
    ),
}

WEAPONS = {
    'basic': (
        {
            'arthur': './img/Chars/Arthur/arthur_w_1.png',
            'merlin': './img/Chars/Merlin/merlin_w_1.png',
        },
        0,
        100,
    ),
    'common': (
        {
            'arthur': './img/Chars/Arthur/arthur_w_2.png',
            'merlin': './img/Chars/Merlin/merlin_w_2.png',
        },
        1,
        20,
    ),
}
CHARACTERS = {
    'arthur': {
        'avatar': './img/Chars/Arthur/arthur_ava.png',
        'codename': 'arthur',
        'name': 'Артур',
        'hero_stage': 0,
        'xp': 0,
        'skill_points': 0,
        'lvl': 5,
        'base_hp': 150,
        'base_dmg': 12,
        'base_special_dmg': 1,
        'crit_chance': 5,
        'stamina': 0,
        'strength': 0,
        'agility': 0,
        'ability_power': 0,
        'weapon_name': 'basic',
    },
    'merlin': {
        'avatar': './img/Chars/Merlin/merlin_ava.png',
        'codename': 'merlin',
        'name': 'Мерлин',
        'hero_stage': 0,
        'xp': 0,
        'skill_points': 0,
        'lvl': 5,
        'base_hp': 120,
        'base_dmg': 15,
        'base_special_dmg': 2,
        'crit_chance': 5,
        'stamina': 0,
        'strength': 0,
        'agility': 0,
        'ability_power': 0,
        'weapon_name': 'basic',
    },
    'demon_soldier': {
        'name': 'Демон солдат',
        'lvl': 1,
        'codename': 'demon_soldier',
        'avatar': './img/Chars/Enemy/demon_1.png',
        'base_hp': 100,
        'base_dmg': 12,
        'base_special_dmg': 1,
        'crit_chance': 5,
        'ultimate': None,
        'ultimate_cd': 0,
    },
    'demon_officer': {
        'name': 'Демон офицер',
        'lvl': 5,
        'codename': 'demon_soldier',
        'avatar': './img/Chars/Enemy/demon_2.png',
        'base_hp': 105,
        'base_dmg': 13,
        'base_special_dmg': 2,
        'crit_chance': 6,
        'ultimate': 'arrow_of_darkness',
        'ultimate_cd': 0,
    },
}
GAME_STAGES = (
    {
        'stage_title': '1. "Скалистое ущелье"',
        'enemy_codename': 'demon_soldier',
        'story': (
            '^Проходя через скалистое ущелье на вас нападает Демон.'
            '\n#"И-хи-хи-хи-хи, заблудшая душа!"'
        ),
        'stage_weapon': 'basic',
    },
    {
        'stage_title': '2. "Скалистое ущелье"',
        'enemy_codename': 'demon_soldier',
        'story': (
            '^Прибыло подкрепление.'
            '\n#"Жалкий смертный, тебе нас всех не одолеть!"'
        ),
        'stage_weapon': 'basic',
    },
    {
        'stage_title': '3. "Скалистое ущелье"',
        'enemy_codename': 'demon_soldier',
        'story': (
            '^Ещё один Демон на вашем пути.'
            '\n#"Как далеко ты суммешь зайти?"'
        ),
        'stage_weapon': 'basic',
    },
    {
        'stage_title': '4. "Скалистое ущелье"',
        'enemy_codename': 'demon_soldier',
        'story': (
            '^Кажется остался последний патрульный.'
            '\n#"Нееет! Я позову на помощь!"'
        ),
        'stage_weapon': 'basic',
    },
    {
        'stage_title': '5. "Скалистое ущелье"',
        'enemy_codename': 'demon_officer',
        'story': (
            '^Из-за скалы появляется силуэт.'
            '\n#"Слабаки! Смотрите как сражаются офицеры!"'
        ),
        'stage_weapon': 'common',
    },
)
