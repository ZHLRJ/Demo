# # 1.
# # 3.  For a arrangement Arr[time1,time2,time3...timeN],
# # for a T=time_j-time_i  , i<j<N . exist a time_l-time_b>=24 , i<= b < l <=j
# # 4.
# # 5. [...,time_i-1, time_i] : last in Day_i , [time_j, time_j+1,...]  : first in Day_j,
# #  time_j - time_i >=12h , Day_j - Day_i =1
# # 6. The len([time_1,time_2,...time_day_last]) =Constant
# # 7.
# # 9. Not_work_days={} not include in Worker.Must_worktime
# # 10.-#30.
# # 32-#34
# # 35.-#36.  OverWorkCount=  +/-
# # 38-#41
# class Worker():
#     def __init__(self,NumberOfWorker=123456,TotalWorkHourInMonth=80):
#         self.NumberOfWorker=NumberOfWorker
#         self.Title="组长 or 普通员工"
#         self.leaveTime={time_a,time_b,...}  # 2 休假
#         self.Must_worktime={time_1,time_2...}  #8  #22
#         self.Administrative_work={time,...}         # 行政工作时间
#         self.Check=[]                          # 18. 盘点
#         self.Week_report=[]                     # 19. 周报
#         self.Preference={}                      # 25.班次偏好
#         self.Best_work_with={}                  #28. 搭班偏好
#         self.TotalWorkHourInMonth=TotalWorkHourInMonth       #31 总工作时间
#         self.TotalWorkHourInDay                             # 0-24 最大工时
#         self.RestHourInDay=0.5*RestCount                #37
#     def can_work(self,time):
#         # May be return some score
#         if self.TotalWorkHourInMonth>SomeNUM\
#             or time in self.leaveTime or .....:
#             return False
#         return True
# Search_Space=[1,2,3,....]
# Work_list=[Work_1,Work_2,...]
# Result=[]
# for time in Search_Space:
#     for work_num in Work_list:
#         if work.can_work(time):
#             Result.append([time,work_num])
#
# A=[]
# for i in range(120):
#     A.append(str(i))
# A.sort()
# print(A)
