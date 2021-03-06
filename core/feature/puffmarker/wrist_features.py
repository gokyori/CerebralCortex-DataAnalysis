# Copyright (c) 2018, MD2K Center of Excellence
# - Nazir Saleheen <nazir.saleheen@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import math
from core.feature.puffmarker.utils import *

from cerebralcortex.core.datatypes.datapoint import DataPoint
from core.feature.puffmarker.utils import moving_average_convergence_divergence, \
    smooth, magnitude
from core.feature.puffmarker.wrist_candidate_filter import filter_with_duration, \
    filter_with_roll_pitch


def calculate_roll_pitch_yaw(accel_data: List[DataPoint]):
    '''
    Computes hand orientation (roll, pitch, yaw) from accelerometer signal
    :param accel_data:
    :return: roll_list, pitch_list, yaw_list
    '''
    roll_list = calculate_roll(accel_data)
    pitch_list = calculate_pitch(accel_data)
    yaw_list = calculate_yaw(accel_data)

    return roll_list, pitch_list, yaw_list


def calculate_roll(accel_data: List[DataPoint]):
    roll_list = []
    for dp in accel_data:
        ax = dp.sample[0]
        ay = dp.sample[1]
        az = dp.sample[2]
        rll = 180 * math.atan2(ax, math.sqrt(ay * ay + az * az)) / math.pi
        roll_list.append(
            DataPoint(start_time=dp.start_time, end_time=dp.end_time,
                      offset=dp.offset, sample=rll))

    return roll_list


def calculate_pitch(accel_data: List[DataPoint]):
    pitch_list = []
    for dp in accel_data:
        ay = dp.sample[1]
        az = dp.sample[2]
        ptch = 180 * math.atan2(-ay, -az) / math.pi
        pitch_list.append(
            DataPoint(start_time=dp.start_time, end_time=dp.end_time,
                      offset=dp.offset, sample=ptch))

    return pitch_list


def calculate_yaw(accel_data: List[DataPoint]):
    yaw_list = []
    for dp in accel_data:
        ax = dp.sample[0]
        ay = dp.sample[1]
        yw = 180 * math.atan2(ay, ax) / math.pi
        yaw_list.append(
            DataPoint(start_time=dp.start_time, end_time=dp.end_time,
                      offset=dp.offset, sample=yw))

    return yaw_list


def compute_basic_statistical_features(data):
    mean = np.mean(data)
    median = np.median(data)
    sd = np.std(data)
    quartile = np.percentile(data, 75) - np.percentile(data, 25)

    return mean, median, sd, quartile


def compute_candidate_features(gyr_intersections, gyr_mag_data, roll_list,
                               pitch_list, yaw_list):
    '''
    Computes feature vector for single hand-to-mouth gesture. Mainly statistical features of hand orientation
    :param gyr_intersections:
    :param gyr_mag_stream:
    :param roll_list:
    :param pitch_list:
    :param yaw_list:
    :return:
    '''
    all_features = []
    offset = gyr_mag_data[0].offset

    for I in gyr_intersections:
        start_time = I.start_time
        end_time = I.end_time
        start_index = I.sample[0]
        end_index = I.sample[1]

        temp_roll = [roll_list[i].sample for i in range(start_index, end_index)]
        temp_pitch = [pitch_list[i].sample for i in
                      range(start_index, end_index)]
        temp_yaw = [yaw_list[i].sample for i in range(start_index, end_index)]
        Gmag_sub = [gyr_mag_data[i].sample for i in
                    range(start_index, end_index)]

        duration = 1000 * (
                end_time - start_time).total_seconds()  # convert to milliseconds

        roll_mean, roll_median, roll_sd, roll_quartile = compute_basic_statistical_features(
            temp_roll)
        pitch_mean, pitch_median, pitch_sd, pitch_quartile = compute_basic_statistical_features(
            temp_pitch)
        yaw_mean, yaw_median, yaw_sd, yaw_quartile = compute_basic_statistical_features(
            temp_yaw)

        gyro_mean, gyro_median, gyro_sd, gyro_quartile = compute_basic_statistical_features(
            Gmag_sub)

        feature_vector = [duration,
                          roll_mean, roll_median, roll_sd, roll_quartile,
                          pitch_mean, pitch_median, pitch_sd, pitch_quartile,
                          yaw_mean, yaw_median, yaw_sd, yaw_quartile,
                          gyro_mean, gyro_median, gyro_sd, gyro_quartile]

        all_features.append(
            DataPoint(start_time=start_time, end_time=end_time, offset=offset,
                      sample=feature_vector))

    return all_features


def compute_wrist_features(accel_data: List[DataPoint],
                           gyro_data: List[DataPoint],
                           fast_moving_avg_size=FAST_MOVING_AVG_SIZE,
                           slow_moving_avg_size=SLOW_MOVING_AVG_SIZE):
    gyr_mag_data = magnitude(gyro_data)

    roll_list, pitch_list, yaw_list = calculate_roll_pitch_yaw(accel_data)

    gyr_mag_800 = smooth(gyr_mag_data, fast_moving_avg_size)
    gyr_mag_8000 = smooth(gyr_mag_data, slow_moving_avg_size)

    gyr_intersections = moving_average_convergence_divergence(gyr_mag_8000,
                                                              gyr_mag_800, 0, 4)

    gyr_intersections = filter_with_duration(gyr_intersections)
    gyr_intersections = filter_with_roll_pitch(gyr_intersections, roll_list,
                                               pitch_list)

    all_features = compute_candidate_features(gyr_intersections, gyr_mag_data,
                                              roll_list, pitch_list, yaw_list)

    return all_features
