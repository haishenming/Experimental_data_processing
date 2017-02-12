#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = HaiShenMing
# 2017/2/6 15:11

import pickle
import matplotlib.pyplot as plt


with open('zhuanfa_frequency.pickle', 'rb') as f_zhuanfa, \
        open('pinglun_frequency.pickle', 'rb') as f_pinglun, \
        open('zhuanfa_percent.pickle', 'rb') as f_zhuanfa_percent, \
        open('pinglun_percent.pickle', 'rb') as f_pinglun_percent:
    zhuanfa_frequency = pickle.load(f_zhuanfa)
    pinglun_frequency = pickle.load(f_pinglun)
    zhuanfa_percent = pickle.load(f_zhuanfa_percent)
    pinglun_percent = pickle.load(f_pinglun_percent)

def percentage_chart(dic, ty, start=None, end=None, run=False, num=None):
    for k in dic:
        runis = run
        minute = []
        number = []
        fig = plt.figure()
        for i in sorted(list(dic[k].items())):
            minute.append(i[0])
            number.append(i[1])
        if runis:
            lis = []
            a = 0
            b = 0
            for i in number:
                b += 1
                if runis:
                    lis.append(i)
                    if i == 0:
                        a += 1
                        if a == num:
                            end=b
                            runis = False
                    if i != 0:
                        a = 0
                        runis = True
        drawing_range_x = minute
        drawing_range_y = number
        plt.plot(drawing_range_x[start:end], drawing_range_y[start:end])
        plt.title('travel time({}-{})'.format(k,ty))
        plt.xlabel('{}'.format(k))
        plt.ylabel('numbers')
        plt.savefig('{}-{}.png'.format(k, ty), dpi=fig.dpi)

if __name__ == '__main__':
    # print(zhuanfa_frequency)
    percentage_chart(zhuanfa_frequency, 'zhuanfa_frequency')
    percentage_chart(pinglun_frequency, 'pinglun_frequency')
    percentage_chart(pinglun_percent, 'pinglun_percent')
    percentage_chart(zhuanfa_percent, 'zhuanfa_percent')
