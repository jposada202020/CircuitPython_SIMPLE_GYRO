# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
import board
import simple_gyro

display = board.DISPLAY

gyro = simple_gyro.Gyro()
display.show(gyro.group)

for i in range(0, -10, -1):
    gyro.update_tilt(i)
    time.sleep(0.1)

for i in range(0, -15, -1):
    gyro.update_roll(i)
    gyro.update_pitch(i * -1)
    time.sleep(0.1)
