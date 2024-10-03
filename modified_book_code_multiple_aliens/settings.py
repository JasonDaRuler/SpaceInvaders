from colors import DARK_GREY, RED

class Settings:
    def __init__(self):
        self.scr_width = 1200
        self.scr_height = 800
        self.bg_color = DARK_GREY
        self.w_h = (self.scr_width, self.scr_height)

        # laser settings
        self.laser_speed = 3.0
        self.laser_width = 30
        self.laser_height = 15
        self.laser_color = RED

        self.ship_limit = 3
        self.fleet_drop_speed = 10

        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 10.0
        self.laser_speed = 2.5
        self.alien_speed = 1.0

        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.laser_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)


def main():
    print('\n*** message from settings.py --- run from alien_invasions.py\n')

if __name__ == "__main__":
    main()