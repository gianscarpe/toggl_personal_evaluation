import numpy as np


class Evaluator:
    END_OF_WEEK = 5

    def __init__(self, entries: list, name: str = "Evaluator"):
        self.name = name
        self.init_data(entries)

    def init_data(self, entries):
        self.data = np.zeros((52, 7))
        for e in entries:
            self._add_entry(e)

    def _get_flat_data_until(self, date):
        data = self.data[: date.day_of_year].flatten()[
            date.start_of("year").day_of_week - 1 :
        ]
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
        first_week_of_month = date.start_of("month").week_of_year - 1
        last_week_of_month = date.end_of("month").week_of_year - 1
        return self.data[first_week_of_month:last_week_of_month, :]

    def _get_week_average(self, date):
        return self._get_week_durations(date)[: Evaluator.END_OF_WEEK].mean()

    def _get_week_average_until(self, date):
        return self._get_until(date, start_of="week").mean()

    def _get_month_average_until(self, date):
        return self._get_until(date, start_of="month").mean()

    def _get_until(self, date, start_of):
        end = (
            date.day_of_week - Evaluator.END_OF_WEEK
            if (Evaluator.END_OF_WEEK > date.day_of_week)
            else 0
        )

        data = self.data[
            date.start_of(start_of).week_of_year - 1 : date.week_of_year,
            : Evaluator.END_OF_WEEK,
        ].flatten()[:end]

        return data

    def _get_month_average(self, date):
        return self._get_month_durations(date)[:, : Evaluator.END_OF_WEEK].mean()
