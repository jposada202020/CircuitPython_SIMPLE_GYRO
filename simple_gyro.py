# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`simple_gyro`
================================================================================

Displayio Gyro representation


* Author(s): Jose D. Montoya


"""
# pylint: disable=too-many-arguments, unused-variable
import math
import time
import board
import displayio
from bitmaptools import draw_circle
import vectorio


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_SIMPLE_GYRO.git"


display = board.DISPLAY


class Gyro:
    """
    Gyro Graphical Representation
    """

    def __init__(self, posx=100, posy=100, radius=50, padding=10, line_roll_heigth=10):
        self.radius = radius
        self.padding = padding
        palette = displayio.Palette(3)
        palette.make_transparent(0)
        palette[1] = 0x440044
        palette[2] = 0xFF00FF

        self.needle_palette = displayio.Palette(4)
        self.needle_palette[0] = 0x123456
        self.needle_palette[1] = 0xFF0000
        self.needle_palette[2] = 0x00FF00
        self.needle_palette[3] = 0x0000FF
        group = displayio.Group()
        line_roll_lenght = (2 * radius - 2 * padding) // 2

        points_polygono = [
            (0, 0),
            (line_roll_lenght, 0),
            (line_roll_lenght, line_roll_heigth),
            (-line_roll_lenght, line_roll_heigth),
            (-line_roll_lenght, 0),
        ]

        self.needle = vectorio.Polygon(
            points=points_polygono,
            pixel_shader=self.needle_palette,
            x=posx,
            y=posy,
        )
        self.original_values = self.needle.points

        points_indicator = [(0, 0), (20, 0), (20, -6), (0, -6)]
        self.indicator = vectorio.Polygon(
            points=points_indicator,
            pixel_shader=self.needle_palette,
            x=posx - 5,
            y=posy - 30,
        )

        group.append(self.needle)
        group.append(self.indicator)
        dial_bitmap = displayio.Bitmap(2 * radius + 1, 2 * radius + 1, 10)
        background = displayio.TileGrid(
            dial_bitmap, pixel_shader=palette, x=posx - radius, y=posy - radius
        )
        group.append(background)
        draw_circle(dial_bitmap, radius, radius, radius, 2)

        display.show(group)

        self.indicator_original_values = self.indicator.points
        self.indix, self.indiy = self.indicator.location

        for i in range(-180, 180):
            self.update_roll(i)
            self.update_pitch(i)
            time.sleep(0.01)

    def update_roll(self, angle):
        """
        Update pitch/roll
        """

        angle = angle * 0.017

        deltax = math.ceil((self.radius - 2 * self.padding) * math.cos(angle))
        deltay = math.ceil((self.radius - 2 * self.padding) * math.sin(angle))

        self.indicator.location = (self.indix + deltax + 5, self.indiy + deltay + 30)

        dummy = [(0, 0), (0, 0), (0, 0), (0, 0)]
        for j, element in enumerate(self.indicator.points):
            dummy[j] = math.ceil(
                self.indicator_original_values[j][0] * math.cos(angle)
                - self.indicator_original_values[j][1] * math.sin(angle)
            ), math.ceil(
                self.indicator_original_values[j][1] * math.cos(angle)
                + self.indicator_original_values[j][0] * math.sin(angle)
            )
        self.indicator.points = dummy

    def update_pitch(self, angle):
        """
        Update pitch/roll
        """

        angle = angle * 0.017

        self.needle.points = [
            (
                math.ceil(
                    self.original_values[0][0] * math.cos(angle)
                    - self.original_values[0][1] * math.sin(angle)
                ),
                math.ceil(
                    self.original_values[0][1] * math.cos(angle)
                    + self.original_values[0][0] * math.sin(angle)
                ),
            ),
            (
                math.ceil(
                    self.original_values[1][0] * math.cos(angle)
                    - self.original_values[1][1] * math.sin(angle)
                ),
                math.ceil(
                    self.original_values[1][1] * math.cos(angle)
                    + self.original_values[1][0] * math.sin(angle)
                ),
            ),
            (
                math.ceil(
                    self.original_values[2][0] * math.cos(angle)
                    - self.original_values[2][1] * math.sin(angle)
                ),
                math.ceil(
                    self.original_values[2][1] * math.cos(angle)
                    + self.original_values[2][0] * math.sin(angle)
                ),
            ),
            (
                math.ceil(
                    self.original_values[3][0] * math.cos(angle)
                    - self.original_values[3][1] * math.sin(angle)
                ),
                math.ceil(
                    self.original_values[3][1] * math.cos(angle)
                    + self.original_values[3][0] * math.sin(angle)
                ),
            ),
            (
                math.ceil(
                    self.original_values[4][0] * math.cos(angle)
                    - self.original_values[4][1] * math.sin(angle)
                ),
                math.ceil(
                    self.original_values[4][1] * math.cos(angle)
                    + self.original_values[4][0] * math.sin(angle)
                ),
            ),
        ]


Gyro()
