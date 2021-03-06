import time
from datetime import date, timedelta

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

ISSUE_TYPE = {1: 'RaiseTouch & Firmwares', 2: 'Broken/Loose Ribbon Cable', 3: 'No response to Touch', 4: 'Jam/Clogging',
              5: 'Loose Connection/ Broken Cables', 6: 'Broken PSU', 7: 'Cracked PC Covers',
              8: 'Shipping Stripe Loose ', 9: 'Gantry Mis-Aligned', 10: 'Broken LED Stripe',
              11: 'Side Door Mis-Aligned with Frame', 12: 'Broken Flash Drive', 13: 'Scratches on Front Door',
              14: 'Camrea Out Of Focuse', 15: 'Lack of Information', 16: 'Printing Settings',
              17: 'Scraches on Build Surface', 18: 'Filament Run-out Sensor Mis-Triggered', 19: 'Printer Swap',
              20: 'Feeding Tube Scratching Top Cover', 21: 'No Extrusion', 22: 'Broken Coupler', 23: 'Weird Noise',
              24: 'Full Size Printing Out of Build Plate', 25: 'Extruder Motor Overheated', 26: 'Loose Screws',
              27: 'Gantry Binding', 28: 'Hotend', 29: 'Offset Calibration', 30: 'Builtak/ Heated Bed',
              31: 'Broken Screen Controller Board', 32: 'Wavy Texture in Z Direction',
              33: 'Nozzle Temperature Fluctuation', 34: '?', 35: 'Uneven First Layer', 36: 'Un-leveled Bed',
              37: 'Broken Z Limit Switch', 38: 'Ethernet', 39: 'Rusty Rod', 40: 'Weird Lines on Model',
              41: 'Nozzle Jogging', 42: 'Motion Controller Board', 43: 'Heated Bed Connecting Terminal Block',
              44: 'Thermocoupler', 45: 'Sliding Block', 46: 'Fans', 47: 'Missing Accessory Tools', 48: 'Shipping',
              49: 'Heater Rod', 50: 'Motor', 51: 'Wi-Fi', 115: 'Using ideaMaker', 116: 'power supply filter failed',
              117: '3rd Party Filament', 118: 'Feature Request', 119: 'Filament Run-Out Sensor', 120: 'Serial Number',
              121: 'Thread/ Screws Worn Out', 122: 'Filament', 123: 'Touchscreen ', 124: 'EndStop', 125: 'Camera',
              126: 'Coupler', 127: 'Bed Adhesion/ Not Sticking'}


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
    # year = int(str_time[:4])
    # month = int(str_time[4:6])
    # day = int(str_time[6:8])
    # tmp = datetime(year, month, day).isocalendar()
    # return tmp[0], tmp[1]
    time_array = time.strptime(str_time, "%Y%m%d")  # 把时间字符串 格式化成 时间数组
    year = time.strftime("%Y", time_array)
    week = time.strftime("%W", time_array)
    return int(year), int(week) + 1


def issue_type_2_id(issue_type):
    """
    issue type 转 issue num
    :param issue_type:  list [Jam, Cabe lose, ]
    :return: list [id1, id2]
    """


def week_2_day(serial_no):
    if len(serial_no) == 11:
        yw = str(serial_no)[4:8]
        if yw.startswith('1') or yw.startswith('2'):
            year_week = "20" + yw[0:2] + "-" + str(int(yw[2:4]) - 1) + "-" + "1"
            struct_time = time.strptime(year_week, '%Y-%W-%w')
            mon_day = time.strftime("%Y%m%d", struct_time)
            return mon_day
    return "20190101"


def last_few_days(n):
    """
    获取n天前和此刻的时间戳
    :param n:
    :return: stamp -> last few days, now
    """
    today = date.today()
    before_day = today - timedelta(days=n)
    start_time = int(time.mktime(time.strptime(str(before_day), '%Y-%m-%d'))) * 1000
    return start_time


def get_year_week(t_time):
    """
    获取 1905 格式的日期
    :param t_time: "2019-05"
    :return: year, week
    """
    tup_time = t_time.split("-")
    t_year = tup_time[0]
    t_week = tup_time[1]
    return int(t_year), int(t_week)


def id_2_type(t_id):
    """
    根据分类id获取问题分类名称
    :param t_id: type_id
    :return: issue_type
    """
    i_type = ISSUE_TYPE.get(t_id)
    return i_type


type_dic = {
    "N1": "",
    "N2": "",
    "Pro2": "",
    "Pro2 Plus": ""
}


def type_2_printer_type(issue_type):
    types = type_dic.get(issue_type)
    return types
