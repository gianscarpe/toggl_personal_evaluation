import calmap
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def format_time(time):
    time = time / 60
    return '{0:01.0f}:{1:02.0f} hours'.format(*divmod(time, 60))


class Evaluator:
    END_OF_WEEK = 5

    def __init__(self, entries):
        self.init_data(entries)

    def init_data(self, entries):
        self.data = np.zeros((52, 7))
        for e in entries:
            self._add_entry(e)

    def print_averages(self, date):
        deep_work_today = self._get_day_duration(date)
        avg_deep_work_this_week = self._get_week_average(date)
        avg_deep_work_this_month = self._get_month_average(date)

        print(
            f"AVG deep work this week {format_time(avg_deep_work_this_week)}")
        print(
            f"AVG deep work this month {format_time(avg_deep_work_this_month)}"
        )
        print(f"Deep work for today {format_time(deep_work_today)}")

        if deep_work_today < avg_deep_work_this_month:
            print(
                f"You need another {format_time(avg_deep_work_this_month - deep_work_today)} to reach your average!"
            )

    def plot(self, date):
        try:
            data = self._get_flat_data_until(date)
            all_days = pd.date_range('1/1/2020', periods=len(data), freq='D')
            events = pd.Series(data, index=all_days)
            ax = plt.subplot(111)

            calmap.yearplot(events, year=2020, ax=ax)
            plt.title("Deep Work Calendar")
            plt.show()
        except Exception as ex:
            print(ex)
            with np.printoptions(precision=3, suppress=True):
                print(self.data)

    def _get_flat_data_until(self, date):

        data = self.data[:date.week_of_year].flatten(
        )[date.start_of('year').day_of_week - 1:]
        return data

    def _add_entry(self, entry):
        day = entry.start
        self.data[day.week_of_year - 1][day.day_of_week - 1] += entry.duration

    def _get_day_duration(self, date):
        day = date.day_of_week - 1
        week = date.week_of_year - 1
        return self.data[week, day]

    def _get_week_durations(self, date):
        week = date.week_of_year - 1
        return self.data[week, :]

    def _get_month_durations(self, date):
        first_week_of_month = date.start_of('month').week_of_year - 1
        return self.data[first_week_of_month:first_week_of_month + 4, :]

    def _get_week_average(self, date):
        return self._get_week_durations(date)[:Evaluator.END_OF_WEEK].mean()

    def _get_month_average(self, date):
        return self._get_month_durations(
            date)[:, :Evaluator.END_OF_WEEK].mean()
