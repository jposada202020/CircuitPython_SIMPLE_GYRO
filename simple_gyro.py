# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`simple_gyro`
================================================================================

Displayio Gyro representation


* Author(s): Jose D. Montoya


"""
# pylint: disable=too-many-arguments, unused-variable, too-many-locals, too-many-statements
from math import pi, cos, sin
import board
import displayio
from bitmaptools import draw_circle, rotozoom
from vectorio import Polygon


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_SIMPLE_GYRO.git"


DEG_TO_RAD = pi / 180

display = board.DISPLAY


class Gyro:
    """
    Gyro Graphical Representation
    """

    def __init__(self, posx=100, posy=100, radius=50, padding=10, line_roll_heigth=10):
        self.radius = radius
        self.padding = padding

        palette = displayio.Palette(6)
        palette.make_transparent(0)
        palette[1] = 0x440044
        palette[2] = 0xFF00FF
        palette[3] = 0x0000FF
        palette[4] = 0xFFFF00
        palette[5] = 0xFF0000

        self.needle_palette = displayio.Palette(5)
        self.needle_palette[0] = 0x123456
        self.needle_palette[1] = 0xFF0000
        self.needle_palette[2] = 0x00FF00
        self.needle_palette[3] = 0x0000FF

        group = displayio.Group()
        line_roll_lenght = (2 * radius - 2 * padding) // 2

        points_level = [
            (0, 0),
            (line_roll_lenght - 10, 0),
            (line_roll_lenght - 10, line_roll_heigth // 3),
            (-line_roll_lenght + 10, line_roll_heigth // 3),
            (-line_roll_lenght + 10, 0),
        ]
        self.level = Polygon(
            points=points_level,
            pixel_shader=self.needle_palette,
            x=posx,
            y=posy - line_roll_heigth // 2,
            color_index=1,
        )
        self.level_origin_y = self.level.y

        points_polygono = [
            (0, 0),
            (line_roll_lenght, 0),
            (line_roll_lenght, line_roll_heigth),
            (-line_roll_lenght, line_roll_heigth),
            (-line_roll_lenght, 0),
        ]

        self.needle = Polygon(
            points=points_polygono,
            pixel_shader=self.needle_palette,
            x=posx,
            y=posy,
        )
        self.original_values = self.needle.points

        points_indicator = [(0, 0), (20, 0), (20, -6), (0, -6)]
        self.indicator = Polygon(
            points=points_indicator,
            pixel_shader=self.needle_palette,
            x=posx - 5,
            y=posy - 30,
        )
        group.append(self.level)
        group.append(self.needle)
        group.append(self.indicator)
        dial_bitmap = displayio.Bitmap(2 * radius + 1, 2 * radius + 1, 10)
        background = displayio.TileGrid(
            dial_bitmap, pixel_shader=palette, x=posx - radius, y=posy - radius
        )
        group.append(background)

        tick_stroke = 1
        tick_length = 6

        tick_bitmap = displayio.Bitmap(tick_stroke, tick_length, 5)
        tick_bitmap.fill(3)
        pos = [-90, -85, -80, -75, -70, -65, -60, -95, -100, -105, -110, -115, -120]
        for i in pos:
            this_angle = i * DEG_TO_RAD

            target_position_x = radius + radius * cos(this_angle)
            target_position_y = radius + radius * sin(this_angle)

            rotozoom(
                dial_bitmap,
                ox=round(target_position_x),
                oy=round(target_position_y),
                source_bitmap=tick_bitmap,
                px=round(tick_bitmap.width / 2),
                py=0,
                angle=0,  # in radians
            )

        tick2_stroke = 2
        tick2_length = 12

        tick2_bitmap = displayio.Bitmap(tick2_length, tick2_stroke, 5)
        tick2_bitmap.fill(4)
        pos = [0, 15, 30, -15, -30]
        for i in pos:
            this_angle = i * DEG_TO_RAD

            target_position_x = (radius * cos(this_angle)) + radius - tick2_length
            target_position_y = (radius * sin(this_angle)) + radius

            rotozoom(
                dial_bitmap,
                ox=round(target_position_x),
                oy=round(target_position_y),
                source_bitmap=tick2_bitmap,
                px=0,
                py=0,
                angle=0,  # in radians
            )

        pos = [150, 165, 180, 195, 210]
        for i in pos:
            this_angle = i * DEG_TO_RAD

            target_position_x = (radius * cos(this_angle)) + radius
            target_position_y = (radius * sin(this_angle)) + radius

            rotozoom(
                dial_bitmap,
                ox=round(target_position_x),
                oy=round(target_position_y),
                source_bitmap=tick2_bitmap,
                px=0,
                py=0,
                angle=0,  # in radians
            )

        draw_circle(dial_bitmap, radius, radius, radius, 2)

        display.show(group)

        self.indicator_original_values = self.indicator.points
        self.indix, self.indiy = self.indicator.location

    def update_roll(self, angle):
        """
        update roll/pitc
        """
        starting_angle = -90 * DEG_TO_RAD

        angle = (angle * DEG_TO_RAD) + starting_angle

        deltax = round((self.radius - 2 * self.padding) * cos(angle))
        deltay = round((self.radius - 2 * self.padding) * sin(angle))

        self.indicator.location = (self.indix + deltax + 5, self.indiy + deltay + 30)

        dummy = [(0, 0), (0, 0), (0, 0), (0, 0)]
        for j, element in enumerate(self.indicator.points):
            dummy[j] = round(
                self.indicator_original_values[j][0] * cos(angle)
                - self.indicator_original_values[j][1] * sin(angle)
            ), round(
                self.indicator_original_values[j][1] * cos(angle)
                + self.indicator_original_values[j][0] * sin(angle)
            )
        self.indicator.points = dummy

    def update_pitch(self, angle):
        """
        Update pitch/roll
        """

        angle = angle * 0.017
        dummy = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
        for j, element in enumerate(self.needle.points):
            dummy[j] = round(
                self.original_values[j][0] * cos(angle)
                - self.original_values[j][1] * sin(angle)
            ), round(
                self.original_values[j][1] * cos(angle)
                + self.original_values[j][0] * sin(angle)
            )
        self.needle.points = dummy

    def update_tilt(self, value):
        """
        update roll/pitch
        """
        self.level.y = value + self.level_origin_y
