import requests,re,datetime,json,calendar
from rest_framework import generics, mixins
from django.db.models.functions import ExtractYear, ExtractMonth
from django.db.models import Count
from projectapp.serializers import *
from projectapp.base.utils import *

# 获取月中时间
def getMonthLastDay(year=None, month=None):
    """
    :param year: 年份，默认是本年，可传int或str类型
    :param month: 月份，默认是本月，可传int或str类型
    """
    if year:
        year = int(year)
    else:
        year = datetime.date.today().year

    if month:
        month = int(month)
    else:
        month = datetime.date.today().month

    # 获取当月第一天的星期和当月的总天数
    firstDayWeekDay, monthRange = calendar.monthrange(year, month)

    # 获取当月的第一天
    centerDay = datetime.date(year=year, month=month, day=monthRange)

    return centerDay

def getMonthCenterDay(year=None, month=None):
    """
    :param year: 年份，默认是本年，可传int或str类型
    :param month: 月份，默认是本月，可传int或str类型
    """
    if year:
        year = int(year)
    else:
        year = datetime.date.today().year

    if month:
        month = int(month)
    else:
        month = datetime.date.today().month

    # 获取当月第一天的星期和当月的总天数
    firstDayWeekDay, monthRange = calendar.monthrange(year, month)

    # 获取当月的第一天
    centerDay = datetime.date(year=year, month=month, day=int(monthRange-15))

    return centerDay

def getYearAgo():
    date = datetime.datetime.today()
    start_year = date.year
    start_month = date.month
    if start_month != 12:
        start_year = start_year - 1

    year_ago = datetime.date(year=start_year, month=start_month, day=1)
    return year_ago

def getMonthAgo():
    date = datetime.datetime.today()
    month_ago = date - datetime.timedelta(days=30)
    return month_ago.strftime("%Y-%m-%d")

def getDaysAgo(days):
    date = datetime.datetime.today()
    days_ago = date - datetime.timedelta(days=days)
    return days_ago.strftime("%Y-%m-%d")

def getTheMonth(date, n):
    month = date.month
    year = date.year
    for i in range(n):
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
    return datetime.date(year, month, 1)  # .strftime('%Y-%m')

def getPreviousMonth(num):
    today = datetime.datetime.today()
    date_arr = []
    for i in range(num):
        previous_date = getTheMonth(today, i)
        date_arr.append(previous_date)
    return date_arr

# 获取版本数量
class Versions(generics.GenericAPIView):
    '''# 获取版本数量'''

    @retResponse()
    def get(self, request):

        # {
        #     xAxis: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', ...],
        #     series: [10, 52, 200, 334, 390, 330, 220, ...]
        # }

        xAxis = []
        series = []

        # 当天时间
        date_arr = getPreviousMonth(12)
        # 获取一年前时间
        year_ago = getYearAgo()

        temp = Version.objects.filter(delete=1).filter(online_plan_time__gte=year_ago).annotate(
            year=ExtractYear('online_plan_time'), month=ExtractMonth('online_plan_time')
        ).values('year', 'month').order_by('year', 'month').annotate(c=Count('id'))

        # 简单转为 json
        temp_list = list(temp)
        for temp_date in date_arr:
            xAxis.append(temp_date.strftime('%Y-%m'))
            flag = False
            for temp_dic in temp_list:
                if temp_date.month == temp_dic["month"] and temp_date.year == temp_dic["year"]:
                    series.append(temp_dic['c'])
                    flag = True
            if flag == False:
                series.append(0)
        xAxis.reverse()
        series.reverse()
        return True,{"xAxis": xAxis, "series": series}

# 获取达标率
class Standard(generics.GenericAPIView):
    '''获取达标率'''

    @retResponse()
    def get(self, request):

        xAxis, series = [], []

        year_ago, month_ago, half_month_ago = getYearAgo(), getMonthAgo(), getDaysAgo(15)
        # 查询上线时间在一个自然月内，需求完成时间小于 15 天的需求
        month_sumCount = StoryPlan.objects.\
            filter(delete=1).\
            filter(online_time__gte=month_ago).\
            filter(status='已上线').\
            filter(duration_days__lte=15).count()

        # 查询上线时间在一个自然月内，完成的总需求数
        month_complete_count = StoryPlan.objects.\
            filter(delete=1).\
            filter(online_time__gte=month_ago).\
            filter(status='已上线').count()

        # 查询进行中超过两周的需求
        month_over_twoweak_count = StoryPlan.objects.\
            filter(delete=1). \
            filter(status='进行中').\
            filter(create_time__lte=half_month_ago).count()

        # 总需求数
        total_count = StoryPlan.objects. \
            filter(delete=1). \
            filter(create_time__gte=month_ago).count()

        sumCount = month_complete_count + month_over_twoweak_count
        if sumCount == 0:
            standardRate = 0
        else:
            standardRate = round(month_sumCount / sumCount,2)

        # 每个月十五天内完成的需求
        standard_arr = StoryPlan.objects. \
            filter(delete=1). \
            filter(duration_days__lte=15). \
            filter(status='已上线'). \
            filter(online_time__gte=year_ago). \
            annotate(year=ExtractYear('online_time'), month=ExtractMonth('online_time')). \
            values('year', 'month'). \
            order_by('year', 'month'). \
            annotate(c=Count('id'))

        standard_arr = list(standard_arr)

        # 每个月内完成的需求
        complete_arr = StoryPlan.objects.\
            filter(delete=1). \
            filter(status='已上线'). \
            filter(online_time__gte=year_ago). \
            annotate(year=ExtractYear('online_time'), month=ExtractMonth('online_time')). \
            values('year', 'month'). \
            order_by('year', 'month'). \
            annotate(c=Count('id'))

        complete_arr = list(complete_arr)

        doing_arr = []
        #
        # 每个月超过两周天未完成的需求
        # 月中之前之前创建的
        temp_date_arr = getPreviousMonth(12)
        temp_date_arr.reverse()

        for date in temp_date_arr:
            month_center_day = getMonthCenterDay(date.year, month=date.month)
            month_last_day= getMonthLastDay(date.year, month=date.month)

            doing_a = StoryPlan.objects.\
                filter(delete=1). \
                filter(status='进行中'). \
                filter(create_time__lte=month_center_day).\
                count()
            doing_b = StoryPlan.objects. \
                filter(delete=1). \
                filter(status='已完成'). \
                filter(online_time__gt=month_last_day). \
                count()
            doing_arr.append({'year': date.year, 'month': date.month, 'c': int(doing_a + doing_b)})

        date_arr = getPreviousMonth(12)
        date_arr.reverse()

        for i in range(12):
            temp_date = date_arr[i]
            if len(standard_arr) <= i:
                standard_arr.insert(i, {"year": temp_date.year, "month": temp_date.month, "c": 0})
            else:
                temp_dic = standard_arr[i]
                if temp_dic["year"] != temp_date.year or temp_dic["month"] != temp_date.month:
                    standard_arr.insert(i, {"year": temp_date.year, "month": temp_date.month, "c": 0})

            if len(complete_arr) <= i:
                complete_arr.insert(i, {"year": temp_date.year, "month": temp_date.month, "c": 0})
            else:
                temp_dic = complete_arr[i]
                if temp_dic["year"] != temp_date.year or temp_dic["month"] != temp_date.month:
                    complete_arr.insert(i, {"year": temp_date.year, "month": temp_date.month, "c": 0})



        for i in range(12):

                temp_date = date_arr[i]
                xAxis.append(temp_date.strftime('%Y-%m'))
                standard = standard_arr[i].get('c')
                complete = complete_arr[i].get('c')
                doing = doing_arr[i].get('c')

                value = 0
                if (doing + complete) != 0:
                    value = standard / (doing + complete)

                if i == 11:
                    series.append(standardRate)
                else:
                    series.append(value)


        return True,{"sumCount": sumCount,
                "complete_count": month_sumCount,
                "totalCount": total_count,
                "standardRate": standardRate,
                "xAxis": xAxis,
                "series": series}

# 获取近一年的需求分布
class DemandYear(generics.GenericAPIView):
    '''获取近一年的需求分布'''

    @retResponse()
    def get(self, request):

        # {
        #     xAxis: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', ...],
        #     series: [10, 52, 200, 334, 390, 330, 220, ...]
        # }
        data = request.query_params
        print(data)
        xAxis = []
        series = []

        # 当天时间
        date_arr = getPreviousMonth(12)
        # 获取去年时间
        year_ago = getYearAgo()

        filter_dict = dict()
        product_title = data.get("product_title")
        if product_title:
            filter_dict["product_name"] = product_title

        temp = StoryPlan.objects.filter(delete=1).filter(**filter_dict).filter(create_time__gte=year_ago).annotate(
            year=ExtractYear('create_time'), month=ExtractMonth('create_time')
        ).values('year', 'month').order_by('year', 'month').annotate(c=Count('id'))

        # 简单转为 json
        temp_list = list(temp)
        for temp_date in date_arr:
            xAxis.append(temp_date.strftime('%Y-%m'))
            flag = False
            for temp_dic in temp_list:
                if temp_date.month == temp_dic["month"] and temp_date.year == temp_dic["year"]:
                    series.append(temp_dic['c'])
                    flag = True
            if flag == False:
                series.append(0)
        xAxis.reverse()
        series.reverse()
        return True,{"xAxis": xAxis, "series": series}

# 获取需求数量
class Demand(generics.GenericAPIView):
    '''获取需求数量'''

    @retResponse()
    def get(self, request):
        plan_count = StoryPlan.objects.filter(delete=1).filter(status='进行中').count()
        unplan_count = StoryPlan.objects.filter(delete=1).filter(version_id=0, status='未安排').count()
        return True,[{'name': "当前进行的需求数", 'value': plan_count}, {'name': "未被安排的需求数", 'value': unplan_count}]
