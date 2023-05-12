# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
import board
import simple_gyro

i2c = board.I2C()  # uses board.SCL and board.SDA
xxx = simple_gyro.SIMPLE_GYRO(i2c)

while True:
    # print("Pressure: {:.2f}hPa".format(lps.pressure))
    time.sleep(0.5)
