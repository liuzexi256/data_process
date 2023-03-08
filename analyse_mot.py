'''
Author: Zexi Liu
Date: 2023-02-24 15:35:51
LastEditors: Zexi Liu
LastEditTime: 2023-02-24 17:58:09
FilePath: /data_process/analyse_mot.py
Description:

Copyright (c) 2023 by Uisee, All Rights Reserved.
'''

import sys
import os
import re
import numpy as np
import matplotlib.pyplot as plt

flog = "/data/uos_mot_det_seg_nlabel.log"

re_phase = re.compile(r".*")
re_time = re.compile(r'^(?P<time>time: .*)$')
show_phase_name = ['obst_detect', 'mot', 'filter_out_range', 'filter_out_rain_noise', 'read_rcs', 'total_time', 'total_cpu_time']


def get_mot_name():
    with open(flog, mode="r") as f:
        for line in f:
            line = line.strip()

            try:
                field_idx = re.search('fields', line).span()
                mot_name_list = line[field_idx[1] + 1:].split()
                break
            except:
                pass
    return mot_name_list


def get_time(mot_phase):
    mot_list = []
    mot_kind = {}
    with open(flog, mode="r") as f:
        for line in f:
            line = line.strip()

            try:
                time_idx = re.search('<mot_output.cc:71>', line).span()
                time = line[time_idx[1] + 3:].split()
                mot_list.append([float(x) for x in time[:len(mot_phase)]])
                if time[8] not in mot_kind:
                    mot_kind[time[8]] = 1
                else:
                    mot_kind[time[8]] += 1
            except:
                pass
    return mot_list


def main():

    # show process_stats.log
    # grep -E " 1\s+[1-5][0-9.]+\s+\S+\s+\S+\s+\S+$" process_stats.log

    # get time
    mot_name_list = get_mot_name()
    mot_list = np.array(get_time(mot_name_list))

    # delete before and after 50 frames
    mot_list = mot_list[10:-10, : ]

    # show phase in figure
    if flog.count('uos_lidar.log') > 0 or flog.count('uos_mot.log') > 0:
        # show all time_phase if flog is uos_lidar.log or uos_mot.log
        global show_phase_name
        show_phase_name = []
    elif flog.count('uos_lidar_framework.log') > 0:
        # show mean time in command line
        mean_array = time_array.mean(axis=0)
        total_idx = time_phase.index('total_time')
        cpu_idx = time_phase.index('total_cpu_time')
        obst_idx = time_phase.index('obst_detect')
        mot_idx = time_phase.index('mot')
        rcs_idx = time_phase.index('read_rcs')
        print('total_time: %.2fms' % mean_array[total_idx])
        print('cpu_time: %.2fms' % mean_array[cpu_idx])
        print('obst_time: %.2fms' % mean_array[obst_idx])
        print('mot_time: %.2fms' % mean_array[mot_idx])
        print('read_rcs_time: %.2fms' % mean_array[rcs_idx])

    # show mean time in command line
    mean_array = time_array.mean(axis=0)
    for i in range(len(mean_array)):
        if mean_array[i] > 4:
            print('%s: %.2fms' % (time_phase[i], mean_array[i]))

    # plot figure
    plt.figure(figsize = (10,5))
    plt.title(flog)

    for name in time_phase:
        if name != 'time_phase:' and name != 'frame_count':
            if len(show_phase_name) == 0:
                plt.rcParams.update({'font.size': 8})
                plt.plot(time_array[:, time_phase.index(name)], label=name)
            elif name in show_phase_name:
                plt.plot(time_array[:, time_phase.index(name)], label=name)
            else:
                pass

    plt.xlabel('frame_cnt')
    plt.ylabel('time(ms)')
    plt.tick_params(axis='both')
    plt.ylim(0, 500)
    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
