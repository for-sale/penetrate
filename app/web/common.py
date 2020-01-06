import time
from datetime import datetime


def str_2_timestamp(str_time):
    """
    str_time = "20180411" 字符串转13位时间戳
    :param str_time: "20180411"
    :return: 1523376000000
    """
    time_stamp = time.mktime(time.strptime(str_time, '%Y%m%d'))
    return int(time_stamp) * 1000


def timestamp_to_str(timestamp):
    """
    时间戳字符串转时间格式
    :param timestamp: int-> 1523376000000
    :return:  "20180411"
    """
    timestamp = int(timestamp)
    return time.strftime('%Y%m%d', time.localtime(timestamp / 1000))


def str_2_weeks(str_time):
    """
    时间转换为当年的第几周
    :param str_time:  "20180411"
    :return:  int -> year week
    """
    year = int(str_time[:4])
    month = int(str_time[4:6])
    day = int(str_time[6:8])
    tmp = datetime(year, month, day).isocalendar()
    return tmp[0], tmp[1]


def issue_type_2_id(issue_type):
    """
    issue type 转 issue num
    :param issue_type:  list [Jam, Cabe lose, ]
    :return: list [id1, id2]
    """
    


# data = str_2_weeks("20200103")
# print(data)
# import time
#
# a1 = "2018-04-11"
# # 先转换为时间数组
# timeArray = time.strptime(a1, "%Y-%m-%d")
#
# # 转换为时间戳
# timeStamp = int(time.mktime(timeArray))
# print(timeStamp)


# # time.strftime('%Y-%m-%d',time.localtime(timestamp/1000))
# # print(len("1523376000000"))
#
#
# timeStamp = 1523376000000/1000
# timeArray = time.localtime(timeStamp)
# otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
# print(otherStyleTime)