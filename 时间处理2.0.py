import time
import csv
import pandas
import pickle
import threading


# import csv

def extraction_time(file):
    with open(file, 'r', encoding='utf-8') as f:
        file = csv.reader(f)
        headers = next(file)
        t_list = []
        for row in file:
            t = time.strptime(row[4], '%Y-%m-%d %H:%M')
            row[4] = time.strftime('%Y-%m-%d %H:%M', t)
            t_list.append(row[4])
    return t_list
    # t_zhuangfa.write(row[4]+'\n') #将时间按行写入新的文件


def time_changeover(t_list):
    stru_time = []
    for t in t_list:
        tim = time.strptime(t, '%Y-%m-%d %H:%M')  # 装换成元组时间
        stru_time.append(tim)
    return stru_time


def creat_time_series(time_list):
    time_list = sorted(time_list)
    time_series_day = pandas.date_range(time_list[0], time_list[-1], freq='d')
    time_series_hour = pandas.date_range(time_list[0], time_list[-1], freq='h')
    time_series_minute = pandas.date_range(time_list[0], time_list[-1], freq='min')
    return {'day': time_series_day, 'hour': time_series_hour, 'minute': time_series_minute}


def time_frequency(time_serise, time_list):
    time_frequency_day = {}
    time_frequency_hour = {}
    time_frequency_minute = {}
    time_frequency = {}
    day = 1
    hour = 1
    minute = 1

    number = 0
    for i in time_serise['day']:
        time_frequency_day[day] = 0
        i = time.strptime(str(i), '%Y-%m-%d %H:%M:%S')
        if i in stru_time_list:
            i = time.mktime(i)
            for j in stru_time_list:
                number += 1
                j = time.mktime(j)
                if j >= i and j < i + 60 * 60 * 24:
                    # print(str(i))
                    # print(j)
                    # print(str(time_serise['day'][day]))
                    time_frequency_day[day] += 1
        time_frequency['day'] = time_frequency_day
        day += 1

    for i in time_serise['hour']:
        time_frequency_hour[hour] = 0
        i = time.strptime(str(i), '%Y-%m-%d %H:%M:%S')
        if i in stru_time_list:
            i = time.mktime(i)
            for j in stru_time_list:
                j = time.mktime(j)
                if j >= i and j < i + 60 * 60:
                    time_frequency_hour[hour] += 1
        time_frequency['hour'] = time_frequency_hour
        hour += 1

    k = 0
    l = 0
    for i in time_serise['minute']:
        print('进度：{}/{}'.format(l,len(time_serise['minute'])))
        l += 1
        time_frequency_minute[minute] = 0
        i = time.strptime(str(i), '%Y-%m-%d %H:%M:%S')
        if i in stru_time_list:
            i = time.mktime(i)
            for j in stru_time_list:
                j = time.mktime(j)
                if j >= i and j < i + 60:
                    time_frequency_minute[minute] += 1
                    print('已完成{}/{}'.format(k, len(time_list)))
                    k += 1
        time_frequency['minute'] = time_frequency_minute
        minute += 1
    return time_frequency


def run(name):
    global time_list
    time_list = extraction_time(name)
    global stru_time_list
    stru_time_list = time_changeover(time_list)
    global time_serise
    time_serise = creat_time_series(time_list)
    time_list = list(map(lambda x: x + ':00', time_list))
    time_list = sorted(time_list)
    return time_frequency(time_serise, time_list)

if __name__ == '__main__':
    t_zhuanfa = threading.Thread(target=run, args=('zhuanfa.csv',))
    t_pinglun = threading.Thread(target=run, args=('pinglun.csv',))
    pinglun_time_frequency = t_pinglun.start()
    zhuanfa_time_frequency = t_zhuanfa.start()
    # zhuanfa_time_frequency = run('zhuanfa.csv')
    # pinglun_time_frequency = run('pinglun.csv')
    with open('zhuanfa_frequency.pickle', 'wb') as f_zhuanfa, \
            open('pinglun_frequency.pickle', 'wb') as f_pinglun:
        pickle.dump(zhuanfa_time_frequency, f_zhuanfa)
        pickle.dump(pinglun_time_frequency, f_pinglun)

    zhuanfa_time_frequency_percent = {}
    pinglun_time_frequency_percent = {}
    zhuanfa_long = len(extraction_time('zhuanfa.csv'))
    pinglun_long = len(extraction_time('pinglun.csv'))

    for i,j in zhuanfa_time_frequency.items():
        for k,l in j.items():
            l = l/zhuanfa_long
            j[k] = l
        zhuanfa_time_frequency_percent[i] = j
    for i,j in pinglun_time_frequency.items():
        for k,l in j.items():
            l = l/pinglun_long
            j[k] = l
        pinglun_time_frequency_percent[i] = j

    with open('zhuanfa_percent.pickle','wb') as f_zhuanfa,\
            open('pinglun_percent.pickle','wb') as f_pinglun:
        pickle.dump(zhuanfa_time_frequency_percent,f_zhuanfa)
        pickle.dump(pinglun_time_frequency_percent,f_pinglun)



