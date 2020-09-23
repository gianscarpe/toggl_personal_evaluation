from unittest import TestCase, expectedFailure, mock

import deep_toggl
import deep_toggl.evaluator as evaluator

PROJECT = "Thesis"
DEEP_TAG = {"deep"}


def _get_mocked_date(week, day, starting_day_of_year):
    date = mock.MagicMock(day_of_week=day,
                          week_of_year=week,
                          day_of_year=day + (week - 1) * 7 -
                          starting_day_of_year + 1)

    return date


def _date_start_of_side_effect(x, week, day, starting_day_of_year):
    if x == 'year':
        return _get_mocked_date(1, 1, starting_day_of_year)
    elif x == 'week':
        return _get_mocked_date(week, 1, starting_day_of_year)
    elif x == 'month':
        return _get_mocked_date(week, 1, starting_day_of_year)


def get_mocked_entry(duration, week, day, starting_day_of_year=1):
    date = _get_mocked_date(week, day, starting_day_of_year)
    date.start_of.side_effect = lambda x: _date_start_of_side_effect(
        x, week, day, starting_day_of_year)
    mocked = mock.MagicMock(duration=duration, start=date)

    return mocked


class TestToggl(TestCase):
    @mock.patch('deep_toggl.api')
    def test_load_data(self, mocked_api):
        with mock.patch('deep_toggl.api.Project.objects.filter',
                        return_value=['testing']) as mocked_project_filter_api:

            deep_toggl._load_from_toggl(PROJECT, DEEP_TAG)
            mocked_project_filter_api.assert_called_once_with(PROJECT,
                                                              contain=False)
            mocked_api.TimeEntry.objects.filter.assert_called_once()
            _, kwargs = mocked_api.TimeEntry.objects.filter.call_args
            self.assertEqual(kwargs['project'], 'testing')
            self.assertEqual(kwargs['tags'], DEEP_TAG)


class TestEvaluator(TestCase):
    def test_init_single_entry(self):
        mocked1 = get_mocked_entry(10, 1, 1)
        entries = [mocked1]

        test_evaluator = evaluator.Evaluator(entries)

        self.assertEqual(test_evaluator._get_day_duration(mocked1.start), 10)
        self.assertEqual(
            sum(test_evaluator._get_week_durations(mocked1.start)), 10)

    def test_init_multi_entries(self):
        mocked1 = get_mocked_entry(duration=10, week=1, day=1)
        mocked2 = get_mocked_entry(duration=10, week=1, day=2)
        mocked3 = get_mocked_entry(duration=20, week=50, day=2)
        mocked_entries = [mocked1, mocked2, mocked3]
        with mock.patch.object(evaluator.Evaluator, 'END_OF_WEEK', 5):
            # Week end on friday
            test_evaluator = evaluator.Evaluator(mocked_entries)

            for mocked_entry in mocked_entries:
                self.assertEqual(
                    test_evaluator._get_day_duration(mocked_entry.start),
                    mocked_entry.duration)

            self.assertEqual(
                sum(test_evaluator._get_week_durations(mocked1.start)), 20)
            self.assertEqual(
                sum(test_evaluator._get_week_durations(mocked2.start)), 20)
            self.assertEqual(
                sum(test_evaluator._get_week_durations(mocked3.start)), 20)

    @mock.patch.object(evaluator.Evaluator, 'END_OF_WEEK', 5)
    def test_averages(self):
        mocked1 = get_mocked_entry(duration=10, week=1, day=1)
        mocked2 = get_mocked_entry(duration=10, week=1, day=2)
        mocked3 = get_mocked_entry(duration=10, week=2, day=2)
        week1_average = 20 / 5
        week2_average = 10 / 5
        month1_average = (week1_average + week2_average) / 4
        mocked_entries = [mocked1, mocked2, mocked3]
        mocked_evaluator = evaluator.Evaluator(mocked_entries)

        self.assertEqual(mocked_evaluator._get_week_average(mocked1.start),
                         week1_average)

        self.assertEqual(mocked_evaluator._get_week_average(mocked1.start),
                         mocked_evaluator._get_week_average(mocked2.start))

        self.assertEqual(mocked_evaluator._get_month_average(mocked1.start),
                         month1_average)

    @mock.patch.object(evaluator.Evaluator, 'END_OF_WEEK', 5)
    def test_flat_monday_first_day(self):
        mocked1 = get_mocked_entry(duration=10, week=1, day=1)
        mocked2 = get_mocked_entry(duration=10, week=1, day=2)
        mocked3 = get_mocked_entry(duration=100, week=2, day=2)
        mocked_entries = [mocked1, mocked2, mocked3]

        mocked_evaluator = evaluator.Evaluator(mocked_entries)
        data = mocked_evaluator._get_flat_data_until(mocked3.start)

        self.assertEqual(data[mocked1.start.day_of_year - 1], 10)
        self.assertEqual(data[mocked2.start.day_of_year - 1], 10)
        self.assertEqual(data[mocked3.start.day_of_year - 1], 100)

    @mock.patch.object(evaluator.Evaluator, 'END_OF_WEEK', 5)
    def test_flat_friday_first_day(self):
        starting_day_of_year = 1
        mocked1 = get_mocked_entry(duration=10,
                                   week=1,
                                   day=6,
                                   starting_day_of_year=starting_day_of_year)
        mocked2 = get_mocked_entry(duration=10,
                                   week=2,
                                   day=1,
                                   starting_day_of_year=starting_day_of_year)
        mocked3 = get_mocked_entry(duration=100,
                                   week=4,
                                   day=1,
                                   starting_day_of_year=starting_day_of_year)

        mocked_entries = [mocked1, mocked2, mocked3]
        mocked_evaluator = evaluator.Evaluator(mocked_entries)
        data = mocked_evaluator._get_flat_data_until(mocked3.start)

        self.assertEqual(data[mocked1.start.day_of_year - 1], 10)
        self.assertEqual(data[mocked2.start.day_of_year - 1], 10)
        self.assertEqual(data[mocked3.start.day_of_year - 1], 100)

    @expectedFailure
    def test_init_single_entry_fail(self):
        mocked1 = get_mocked_entry(10, 10, 10)
        mocked_failed_entries = [mocked1]
        evaluator.Evaluator(mocked_failed_entries)
