import time
from datetime import datetime, date, timedelta

PRINTER_TYPE = ["N1", "N2", "Pro2", "Pro2 Plus", "Unknown"]

SOFTWARE = ["printing settings\n打印设置",
            "raisetouch&firmware触屏及固件",
            "request(im/raisetuch/hardware)",
            "ideamaker instruction",
            "wi-fi",
            "3rd party filament recommendation",
            "serial number",
            "full size out of print bed\n打印尺寸超出热床",
            "uneven extrusion on raft \nraft 挤出的不平整"]

SOFTWARE_ID = [16, 1, 118, 115, 51, 117, 120, 24, 35]


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


def last_few_days(n):
    """
    获取n天前和此刻的时间戳
    :param n:
    :return: stamp -> last few days, now
    """
    today = date.today()
    before_day = today - timedelta(days=n)
    start_time = int(time.mktime(time.strptime(str(before_day), '%Y-%m-%d')))*1000
    end_time = int(time.time())*1000
    return start_time, end_time
