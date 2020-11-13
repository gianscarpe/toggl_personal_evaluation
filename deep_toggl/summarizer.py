import calmap
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def format_time(time):
    time = time / 60
    return "{0:01.0f}:{1:02.0f} hours".format(*divmod(time, 60))


class Summarizer:
    def __init__(self, evaluator):
        self.evaluator = evaluator

    def print_averages(self, date):
        deep_work_today = self.evaluator._get_day_duration(date)
        avg_deep_work_this_week = self.evaluator._get_week_average(date)
        avg_deep_work_this_month = self.evaluator._get_month_average(date)

        print(f"Summary for {self.evaluator.name}")
        print(f"AVG deep work this week {format_time(avg_deep_work_this_week)}")
        print(f"AVG deep work this month {format_time(avg_deep_work_this_month)}")
        print(f"Deep work for today {format_time(deep_work_today)}")

        if deep_work_today < avg_deep_work_this_month:
            print(
                f"You need another {format_time(avg_deep_work_this_month - deep_work_today)} to reach your average!"
            )

    def plot(self, date):
        try:
            data = self.evaluator._get_flat_data_until(date)
            all_days = pd.date_range("1/1/2020", periods=len(data), freq="D")
            events = pd.Series(data, index=all_days)
            ax = plt.subplot(111)

            calmap.yearplot(events, year=2020, ax=ax)
            plt.title(f"Deep Work Calendar for {self.evaluator.name}")
            plt.show()
        except Exception as ex:
            print(ex)
            with np.printoptions(precision=3, suppress=True):
                print(data)
