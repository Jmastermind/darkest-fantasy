"""
Darkest fantasy.

Simple turn-based dark fantasy RPG game.
"""

from ast import literal_eval
from pathlib import Path
from random import choices, randint
from time import sleep

import kivy
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.screenmanager import Screen, ScreenManager

import assets

Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', '0')

__version__ = '0.1'

kivy.require('2.1.0')


class Manager(ScreenManager):
    """Screen Manager."""

    def __init__(self, **kwargs) -> None:
        """Import Window module on initialization."""
        super().__init__(**kwargs)
        from kivy.core.window import Window

        self._keyboard = Window.request_keyboard(
            self._keyboard_closed,
            self,
            'text',
        )
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        Window.bind(mouse_pos=self.on_mouseover)

    def on_mouseover(self, window, pos) -> None:
        """Mouse-over event handler."""
        if self.ids.start_btn.collide_point(*pos):
            self.ids.start_btn.background_normal = './img/UI/btn_start_mo.png'
        else:
            self.ids.start_btn.background_normal = './img/UI/btn_start_n.png'

        if self.ids.resume_btn.collide_point(*pos):
            self.ids.resume_btn.background_normal = (
                './img/UI/btn_resume_mo.png'
            )
        else:
            self.ids.resume_btn.background_normal = './img/UI/btn_resume_n.png'

        if self.ids.restart_btn.collide_point(*pos):
            self.ids.restart_btn.background_normal = (
                './img/UI/btn_restart_mo.png'
            )
        else:
            self.ids.restart_btn.background_normal = (
                './img/UI/btn_restart_n.png'
            )
        if self.ids.reset_btn.collide_point(*pos):
            self.ids.reset_btn.background_normal = './img/UI/btn_reset_mo.png'
        else:
            self.ids.reset_btn.background_normal = './img/UI/btn_reset_n.png'
        if self.ids.checkout_btn.collide_point(*pos):
            self.ids.checkout_btn.background_normal = (
                './img/UI/btn_continue_mo.png'
            )
        else:
            self.ids.checkout_btn.background_normal = (
                './img/UI/btn_continue_n.png'
            )
        if self.ids.again_btn.collide_point(*pos):
            self.ids.again_btn.background_normal = './img/UI/btn_again_mo.png'
        else:
            self.ids.again_btn.background_normal = './img/UI/btn_restart_n.png'
        if self.ids.exit_btn.collide_point(*pos):
            self.ids.exit_btn.background_normal = './img/UI/btn_restart_mo.png'
        else:
            self.ids.exit_btn.background_normal = './img/UI/btn_restart_n.png'

    def _keyboard_closed(self) -> None:
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers) -> None:
        # Keycode is composed of an integer + a string
        if keycode[1] == 'escape' and self.current == 'battle':
            self.current = 'menu'
        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True


class Home(Screen):
    """Home screen."""


class Battle(Screen):
    """Battle screen."""


class Menu(Screen):
    """Game menu screen."""


class Checkpoint(Screen):
    """End of game round screen."""


class Stages(Screen):
    """Game stage selection screen."""


class MainApp(App):
    """Main app."""

    def build(self) -> Manager:
        """App startup."""
        # The main window title.
        self.title = 'Darkest Fantasy'
        self.ui = Manager()
        self.game = Game(self, self.ui)
        return self.ui


class Game:
    """Main class of the game."""

    def __init__(self, app, ui) -> None:
        """Initializate basic game variables."""
        # Creating main app and UI objects.
        self.app = app
        self.ui = ui
        # Game variables.
        self.loaded = False
        self.first_start = True
        self.hero_pick = 'arthur'
        self.hero_attributes = None
        self.your_turn = True
        # Save files.
        self.save_file = './saves/main.save'
        self.save_file_backup = './saves/backup.save'

        self.heroes = {
            'arthur': Arthur,
            'merlin': Merlin,
        }
        self.Arthur_attributes = assets.CHARACTERS['arthur'].copy()
        self.Merlin_attributes = assets.CHARACTERS['merlin'].copy()

    def choose_hero(self, id: str) -> None:
        """Choose hero to play with."""
        if id == 'arthur':
            self.ui.ids.arthur.source = assets.HOME_IMAGES['arthur'][1]
            self.ui.ids.merlin.source = assets.HOME_IMAGES['merlin'][0]
            self.hero_pick = 'arthur'
        else:
            self.ui.ids.arthur.source = assets.HOME_IMAGES['arthur'][0]
            self.ui.ids.merlin.source = assets.HOME_IMAGES['merlin'][1]
            self.hero_pick = 'merlin'

    def load_game(self) -> None:
        """Load the game from an encoded save file."""
        try:
            self.f = open('./saves/main.save', 'r')
            f_read = self.f.read().split()
            decoded_1 = self.coder(f_read[0], 'dencode')
            decoded_2 = self.coder(f_read[1], 'decode')
            self.f.close()
            self.temp_dict = literal_eval(decoded_1).copy()
            self.assign_loaded_attributes(self.Arthur_attributes)
            self.temp_dict = literal_eval(decoded_2).copy()
            self.assign_loaded_attributes(self.Merlin_attributes)
            del self.temp_dict
            print('Game loaded')
            self.loaded = True
        except IOError as err:
            self.loaded = False
            print(err)

    def assign_loaded_attributes(self, dict: dict) -> None:
        """Set loaded attributes to the heroes."""
        dict['hero_stage'] = self.temp_dict['hero_stage']
        dict['xp'] = self.temp_dict['xp']
        dict['lvl'] = self.temp_dict['lvl']
        dict['skill_points'] = self.temp_dict['skill_points']
        dict['stamina'] = self.temp_dict['stamina']
        dict['strength'] = self.temp_dict['strength']
        dict['agility'] = self.temp_dict['agility']
        dict['ability_power'] = self.temp_dict['ability_power']
        dict['weapon_name'] = self.temp_dict['weapon_name']

    def start_game(self, stage='default') -> None:
        """Start the game."""
        self.load_game()
        self.hero_attributes = (
            self.Arthur_attributes
            if self.hero_pick == 'arthur'
            else self.Merlin_attributes
        )
        self.current_stage = assets.GAME_STAGES[
            self.hero_attributes['hero_stage']
        ]
        if stage != 'default':
            self.current_stage = assets.GAME_STAGES[stage]
        if self.loaded and self.first_start:
            self.proceed_game('again')
        else:
            self.typewriter = Typewriter(self.ui)
            self.enemy_attributes: dict = assets.CHARACTERS[
                self.current_stage['enemy_codename']
            ]
            self.ui.current = 'battle'
            self.hero = self.heroes[self.hero_pick](self.hero_attributes)
            self.enemy = Enemy(self.enemy_attributes)
            self.typewriter.print(self.current_stage['story'])
            self.buttons_disable_event = Clock.schedule_interval(
                self.buttons_disable,
                1 / 24,
            )
            self.enemy_turn_event = Clock.create_trigger(
                self.enemy_turn,
                1 / 24,
                True,
            )
            self.battle_result_event = Clock.create_trigger(
                self.battle_result,
                1 / 24,
                True,
            )
            self.battle_update_ui()

    def buttons_disable(self, dt: float) -> None:
        """[async] Disable player buttons during enemy turn."""
        self.ui.ids.hero_ability_1.disabled = True
        self.ui.ids.hero_ability_2.disabled = True
        if self.typewriter.typewriter_finished:
            self.ui.ids.hero_ability_1.disabled = False
            if self.hero.sp_ability_1_cd == 0:
                self.ui.ids.hero_ability_2.disabled = False
            self.buttons_disable_event.cancel()

    def enemy_turn(self, dt: float) -> None:
        """[async] Perform enemy turn."""
        if self.typewriter.typewriter_finished:
            self.enemy_turn_event.cancel()
            if (
                self.hero.codename == 'merlin'
                and self.hero.sp_ability_1_cd > 0
                and self.enemy.current_hp > 0
            ):
                attack = self.hero.special_attack_1(self.enemy, dot=True)
                self.popup(
                    attack[1], attack[2], self.ui.ids.enemy_damaged, attack[3],
                )
            if self.hero.current_hp > 0 and self.enemy.current_hp > 0:
                if self.enemy.ultimate and self.enemy.ultimate_cd == 0:
                    attack = eval(
                        f'self.enemy.{self.enemy.ultimate}(self.hero)',
                    )
                else:
                    attack = self.enemy.attack(self.hero)
                self.popup(attack[1], attack[2], self.ui.ids.hero_damaged)
                self.hero.sp_ability_1_cd -= (
                    1 if self.hero.sp_ability_1_cd > 0 else 0
                )
                self.typewriter.print('\n' + attack[0])
                self.battle_update_ui()
            if self.hero.current_hp > 0 and self.enemy.current_hp > 0:
                self.buttons_disable_event()
            else:
                winner = (
                    self.hero.name
                    if self.hero.current_hp > 0
                    else self.enemy.name
                )
                new_line = (
                    '^' if len(self.ui.ids.chat.text.split('\n')) > 3 else '\n'
                )
                self.typewriter.print(
                    f'{new_line}Бой закончен. {winner} победил.',
                )
                self.battle_result_event()

    def hero_turn(self, attack_type: str) -> None:
        """Perform hero turn."""
        if self.typewriter.typewriter_finished:
            self.ui.ids.hero_ability_1.disabled = True
            self.ui.ids.hero_ability_2.disabled = True
            if attack_type == 1:
                attack = self.hero.attack(self.enemy)
                self.popup(attack[1], attack[2], self.ui.ids.enemy_damaged)
            elif attack_type == 2:
                attack = self.hero.special_attack_1(self.enemy)
                target_sp_1 = (
                    self.ui.ids.enemy_damaged
                    if attack[3] == 'enemy'
                    else self.ui.ids.hero_damaged
                )
                self.popup(attack[1], attack[2], target_sp_1, attack[3])
            self.typewriter.print('^' + attack[0])
            self.enemy.ultimate_cd -= 1 if self.enemy.ultimate_cd > 0 else 0
            self.battle_update_ui()
            self.enemy_turn_event()

    def battle_update_ui(self) -> None:
        """Update UI during gameplay."""
        self.ui.ids.hero_ava.source = self.hero.avatar
        self.ui.ids.enemy_img.source = self.enemy.avatar
        self.ui.ids.hero_weapon.source = assets.WEAPONS[self.hero.weapon_name][
            0
        ][self.hero.codename]
        self.ui.ids.hero_ability_1.background_normal = assets.ABILITIES[
            self.hero.codename
        ][0][0]
        self.ui.ids.hero_ability_1.background_disabled_normal = (
            assets.ABILITIES[self.hero.codename][0][1]
        )
        self.ui.ids.hero_ability_2.background_normal = assets.ABILITIES[
            self.hero.codename
        ][1][0]
        self.ui.ids.hero_ability_2.background_disabled_normal = (
            assets.ABILITIES[self.hero.codename][1][1]
        )
        self.ui.ids.hero_ability_2.opacity = 1 if self.hero.lvl >= 5 else 0
        self.ui.ids.hero_lvl.text = f'Lvl {self.hero.lvl}'
        self.ui.ids.hero_hp.text = f'HP {self.hero.current_hp}/{self.hero.hp}'
        self.ui.ids.enemy_lvl.text = f'Lvl {self.enemy.lvl}'
        self.ui.ids.enemy_hp.text = (
            f'HP {self.enemy.current_hp}/{self.enemy.hp}'
        )
        if self.hero.current_hp / self.hero.hp > 0.5:
            self.ui.ids.hero_hp.color = '248a27'
        else:
            self.ui.ids.hero_hp.color = '8a243c'
            if self.hero.current_hp < 0:
                self.ui.ids.hero_hp.text = 'МЕРТВ'
        if self.enemy.current_hp / self.enemy.hp > 0.5:
            self.ui.ids.enemy_hp.color = '248a27'
        else:
            self.ui.ids.enemy_hp.color = '8a243c'
            if self.enemy.current_hp < 0:
                self.ui.ids.enemy_hp.text = 'МЕРТВ'
        self.ui.ids.checkout_btn.opacity = 0
        self.ui.ids.checkout_btn.disabled = True
        self.ui.ids.again_btn.size = (120, 60)
        self.ui.ids.again_btn.opacity = 0
        self.ui.ids.again_btn.disabled = True

    def popup(
        self, damage: int, crit: bool, char, ab_type: str = 'enemy',
    ) -> None:
        """Animate effects over the portraits."""
        if crit:
            char.color = 'yellow'
        elif ab_type == 'hero':
            char.color = 'green'
        else:
            char.color = 'white'
        char.font_size = 100 if crit else 80
        char.text = str(damage)
        char.opacity = 1
        Animation(opacity=0, duration=3).start(char)

    def battle_result(self, dt: float):
        """[async] Show EOR buttons."""
        if self.typewriter.typewriter_finished:
            self.battle_result_event.cancel()
            if self.hero.current_hp > 0:
                self.ui.ids.checkout_btn.opacity = 1
                self.ui.ids.checkout_btn.disabled = False
                self.ui.ids.again_btn.size = (1, 1)
            else:
                self.ui.ids.again_btn.size = (120, 60)
                self.ui.ids.again_btn.opacity = 1
                self.ui.ids.again_btn.disabled = False

    def checkpoint(self) -> None:
        """Show the result of the game round."""
        self.ui.current = 'checkpoint'
        # Exp gained.
        if self.hero.lvl < self.enemy.lvl:
            self.hero.xp += 20
        elif self.hero.lvl == self.enemy.lvl:
            self.hero.xp += 10
        else:
            self.hero.xp += 1
        # Level Up.
        if self.hero.xp >= 100:
            self.hero.lvl += 1
            self.hero.skill_points += 1
            self.hero.xp -= 100
        self.weapon_drop()
        self.round_result = (
            f'Уровень {self.current_stage["stage_title"]} пройден!\n'
            f'Ваш текущий опыт: {self.hero.xp}/100 '
            f'(Очки талантов: {self.hero.skill_points})'
        )
        self.result_update_event = Clock.create_trigger(
            self.result_update, 1 / 24, True,
        )
        self.result_update_event()

    def weapon_drop(self) -> None:
        """Get weapon drop."""
        if (
            assets.WEAPONS[self.current_stage['stage_weapon']][1]
            > assets.WEAPONS[self.hero.weapon_name][1]
        ):
            if choices(
                (1, 0),
                weights=(
                    assets.WEAPONS[self.current_stage['stage_weapon']][2],
                    100
                    - assets.WEAPONS[self.current_stage['stage_weapon']][2],
                ),
            )[0]:
                self.hero.weapon_name = self.current_stage['stage_weapon']
                print('New weapon acquired!')

    def spend_sp(self, stat: str) -> None:
        """Spend skill points."""
        if stat == 'stamina':
            self.hero.stamina += 1
        elif stat == 'strength':
            self.hero.strength += 1
        elif stat == 'agility':
            self.hero.agility += 1
        elif stat == 'ability_power':
            self.hero.ability_power += 1
        self.hero.skill_points = 0

    def result_update(self, dt: float) -> None:
        """[async] Update UI of the result of the round."""
        self.ui.ids.hero_ava_chpt.source = self.hero.avatar
        self.ui.ids.hero_weapon_chpt.source = assets.WEAPONS[
            self.hero.weapon_name
        ][0][self.hero.codename]
        self.ui.ids.round_result.text = str(self.round_result)
        self.ui.ids.stamina_label.text = str(self.hero.stamina)
        self.ui.ids.strength_label.text = str(self.hero.strength)
        self.ui.ids.agility_label.text = str(self.hero.agility)
        self.ui.ids.ability_power_label.text = str(self.hero.ability_power)
        if self.hero.skill_points == 0:
            self.ui.ids.stamina_spend.disabled = True
            self.ui.ids.strength_spend.disabled = True
            self.ui.ids.agility_spend.disabled = True
            self.ui.ids.ability_power_spend.disabled = True
            self.ui.ids.continue_btn.disabled = False
            self.result_update_event.cancel()
        else:
            self.ui.ids.stamina_spend.disabled = False
            self.ui.ids.strength_spend.disabled = False
            self.ui.ids.agility_spend.disabled = False
            self.ui.ids.ability_power_spend.disabled = False
            self.ui.ids.continue_btn.disabled = True

    def save_game(self) -> None:
        """Save the game in an encoded file."""
        if self.hero.name == 'Артур':
            self.Arthur_attributes['hero_stage'] = self.hero.hero_stage
            self.Arthur_attributes['xp'] = self.hero.xp
            self.Arthur_attributes['lvl'] = self.hero.lvl
            self.Arthur_attributes['skill_points'] = self.hero.skill_points
            self.Arthur_attributes['stamina'] = self.hero.stamina
            self.Arthur_attributes['strength'] = self.hero.strength
            self.Arthur_attributes['agility'] = self.hero.agility
            self.Arthur_attributes['ability_power'] = self.hero.ability_power
            self.Arthur_attributes['weapon_name'] = self.hero.weapon_name
        else:
            self.Merlin_attributes['hero_stage'] = self.hero.hero_stage
            self.Merlin_attributes['xp'] = self.hero.xp
            self.Merlin_attributes['lvl'] = self.hero.lvl
            self.Merlin_attributes['skill_points'] = self.hero.skill_points
            self.Merlin_attributes['stamina'] = self.hero.stamina
            self.Merlin_attributes['strength'] = self.hero.strength
            self.Merlin_attributes['agility'] = self.hero.agility
            self.Merlin_attributes['ability_power'] = self.hero.ability_power
            self.Merlin_attributes['weapon_name'] = self.hero.weapon_name
        if Path(self.save_file).exists():
            Path(self.save_file).replace(self.save_file_backup)
        with open('./saves/main.save', 'w') as f:
            f.write(self.coder(str(self.Arthur_attributes), 'encode') + '\n')
            f.write(self.coder(str(self.Merlin_attributes), 'encode') + '\n')
            print('Game saved')

    def coder(self, string: str, mode: str) -> str:
        """Encode or decode a given string."""
        if mode == 'encode':
            code = ' '.join(str(ord(i)) for i in string)
            code_shift = ' '.join(str(int(i) << 3) for i in code.split())
            return code_shift.replace(' ', '&')
        decode_shift_split = string.replace('&', ' ')
        decode_shift = ' '.join(
            str(int(i) >> 3) for i in decode_shift_split.split()
        )
        return ''.join(chr(int(i)) for i in decode_shift.split())

    def proceed_game(self, mode: str) -> None:
        """Handle different game states."""
        if mode == 'continue':
            if self.hero.hero_stage < (len(assets.GAME_STAGES) - 1):
                self.hero.hero_stage += 1
                print('Hero stage now is ', self.hero.hero_stage)
                self.first_start = False
            else:
                # Add end of the game screen.
                print('You beat the game!')
                self.save_game()
                self.typewriter.typewriter_event.cancel()
                self.buttons_disable_event.cancel()
                del self.hero
                del self.enemy
                del self.typewriter
                self.stages()
                return
            self.save_game()
        if hasattr(self, 'enemy'):
            self.typewriter.typewriter_event.cancel()
            self.buttons_disable_event.cancel()
            del self.hero
            del self.enemy
            del self.typewriter
        if mode == 'restart':
            self.ui.current = 'home'
            return
        if mode == 'reset':
            Path('saves/main.save').unlink(missing_ok=True)
            self.Arthur_attributes = assets.CHARACTERS['arthur'].copy()
            self.Merlin_attributes = assets.CHARACTERS['merlin'].copy()
            self.first_start = True
            self.ui.current = 'home'
            return
        if mode == 'again':
            self.first_start = False
            self.stages()
            return
        self.start_game()

    def stages(self):
        """Show game stage list."""
        for i in range(1, 101):
            exec(f'self.ui.ids.stage_{i}.disabled = True')
        self.ui.current = 'stages'
        if self.hero_attributes['hero_stage'] == (len(assets.GAME_STAGES) - 1):
            self.ui.ids.game_beat.opacity = 1
            self.ui.ids.exit_btn.opacity = 1
        for i in range(1, self.hero_attributes['hero_stage'] + 2):
            exec(f'self.ui.ids.stage_{i}.disabled = False')


class Typewriter:
    """Typewriter for game messages."""

    def __init__(self, ui: Manager) -> None:
        """Initialize the typewriter and run it asynchronously."""
        self.ui = ui
        self.typewriter_text = ''
        self.typewriter_finished = False
        self.typewriter_event = Clock.create_trigger(self.tw_callback, 1 / 24)

    def print(self, text: str) -> None:
        """
        Typewriter print method.

        Schedules a Clock event with a callback function that
        "prints" a passed string at the specified interval.

        Args:
            text: The string to print. Supports special characters
                '^' - clear current printed text.
                '#' - adds a 1 second pause before the next printed character.
            dt: The delta time (optional)
        """
        self.typewriter_text = text
        self.typewriter_finished = False
        self.typewriter_event()

    def tw_callback(self, dt: float) -> None:
        """[async] Typewriter callback."""
        if len(self.typewriter_text) > 0:
            if self.typewriter_text[0] == '^':
                self.ui.ids.chat.text = ''
            elif self.typewriter_text[0] == '#':
                sleep(1)
            else:
                self.ui.ids.chat.text += self.typewriter_text[0]
            self.typewriter_text = self.typewriter_text[1:]
            self.typewriter_event()
        else:
            self.typewriter_finished = True


class Character:
    """The base class of a game character."""

    def __init__(
        self,
        attributes: dict[str, int],
    ) -> None:
        """Initialize attributes of the basic character."""
        self.attributes = attributes
        self.codename = self.attributes['codename']
        self.avatar = self.attributes['avatar']
        self.name = attributes['name']
        self.lvl = self.attributes['lvl']
        self.avatar = attributes['avatar']
        self.base_hp = attributes['base_hp']
        self.base_dmg = attributes['base_dmg']
        self.base_special_dmg = attributes['base_special_dmg']
        self.crit_chance = attributes['crit_chance']
        # Calculated stats.
        self.hp = int(self.base_hp + self.base_hp * self.lvl * 0.1)
        self.dmg = int(self.base_dmg + self.base_dmg * self.lvl * 0.1)
        self.current_hp = self.hp

    def attack(self, target) -> tuple[str, int, bool]:
        """Attack enemy character."""
        crit = (
            self.dmg
            * choices(
                (1, 0), weights=(self.crit_chance, 100 - self.crit_chance),
            )[0]
        )
        crited = ' КРИТ' if crit else ''
        damage_done = randint(int(self.dmg / 2), self.dmg) + crit
        target.current_hp -= damage_done
        target_name = (
            f'{target.name}у' if isinstance(target, Hero) else 'противнику'
        )
        return (
            (
                f'{self.name} наносит {target_name} '
                f'{damage_done}{crited} единиц урона.'
            ),
            damage_done,
            bool(crited),
        )


class Enemy(Character):
    """The base class of a enemy character."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize attributes of the enemy character."""
        super().__init__(*args, **kwargs)
        self.ultimate = self.attributes['ultimate']
        self.ultimate_cd = self.attributes['ultimate_cd']

    def arrow_of_darkness(self, target) -> tuple[str, int, bool, str]:
        """Use Arrow of Darkness ability."""
        self.ultimate_cd = 3
        damage_done = self.base_special_dmg * 10
        target.current_hp -= damage_done
        return (
            (
                f'{self.name} выпускает Стрелу Тьмы!\n'
                f'Она наносит герою {damage_done} единиц урона.'
            ),
            damage_done,
            True,
            'damage',
        )


class Hero(Character):
    """The base class of a hero character."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize attributes of the hero character."""
        super().__init__(*args, **kwargs)
        self.hero_stage = self.attributes['hero_stage']
        self.xp = self.attributes['xp']
        self.skill_points = self.attributes['skill_points']
        self.stamina = self.attributes['stamina']
        self.strength = self.attributes['strength']
        self.agility = self.attributes['agility']
        self.ability_power = self.attributes['ability_power']
        # Weapons Tuple elements: dmg, crit_chance, ability_power.
        self.weapons = {
            'arthur': {
                'basic': (1, 0, 0),
                'common': (3, 1, 0),
            },
            'merlin': {
                'basic': (0, 0, 1),
                'common': (0, 1, 3),
            },
        }
        self.weapon_name = self.attributes['weapon_name']
        self.weapon = self.weapons[self.codename][self.weapon_name]
        self.hp = int(
            self.base_hp + self.base_hp * self.lvl * 0.1 + self.stamina * 10,
        )
        self.current_hp = self.hp
        self.dmg = (
            int(self.base_dmg + self.base_dmg * self.lvl * 0.1)
            + self.strength * 2
            + self.weapon[0]
        )
        self.crit_chance = (
            self.attributes['crit_chance'] + self.agility + self.weapon[1]
        )
        self.special_dmg = self.attributes['base_special_dmg'] + self.weapon[2]
        self.sp_ability_1_cd = 0
        self.sp_ability_2_cd = 3


class Arthur(Hero):
    """Arthur hero class."""

    def special_attack_1(self, enemy: Enemy) -> tuple[str, int, bool, str]:
        """Arthur's special attack №1.

        Heals hero and buffs atack damage.

        Returns:
            message: Printed in the chat.
            hp_buff: Amout of healing.
            crit: Flag of crit modifier.
            target: Ability target.
        """
        self.sp_ability_1_cd = 3
        hp_buff = int(self.special_dmg * 10 + self.ability_power * 5)
        self.current_hp += hp_buff
        self.dmg += self.special_dmg + self.ability_power * 2
        return (
            (
                f'{self.name} использует Благословение могущества!\n'
                'Текущее здоровье и наносимый урон повышены.'
            ),
            hp_buff,
            False,
            'hero',
        )


class Merlin(Hero):
    """Merlin hero class."""

    def special_attack_1(self, enemy, dot=False) -> tuple[str, int, bool, str]:
        """Merlin's special attack №1.

        DOT effect deals 10% of the target's initial HP in 3 turns.

        Args:
            enemy: Target to attack.
            dot: If True cooldown is not reset.

        Returns:
            message: Printed in the chat.
            damage: Damage caused by the spell.
            crit: Flag of crit modifier.
            target: Ability target.
        """
        if not dot:
            self.sp_ability_1_cd = 3
        damage_done = int(
            enemy.hp * 0.033 + self.special_dmg + self.ability_power * 3,
        )
        enemy.current_hp -= damage_done
        return (
            (
                f'{self.name} использует Вечное пламя!\n'
                f'Заклинание наносит противнику {damage_done} '
                'урона каждый ход.'
            ),
            damage_done,
            True,
            'enemy',
        )


if __name__ == '__main__':
    MainApp().run()
