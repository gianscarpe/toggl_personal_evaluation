from unittest import TestCase, mock

import deep_toggl.summarizer as summarizer


class TestSummarizer(TestCase):
    def test_format_time_hours_minutes(self):
        time = 10000
        expected_result = "2:47 hours"

        result = summarizer.format_time(time)
        self.assertEqual(expected_result, result)

    def test_format_time_only_minutes(self):
        time = 1000
        expected_result = "0:17 hours"

        result = summarizer.format_time(time)
        self.assertEqual(expected_result, result)

    def test_summarizer_init(self):
        mocked_evaluator = mock.MagicMock()
        summ = summarizer.Summarizer(mocked_evaluator)

        self.assertIsNotNone(summ)

    def test_print_averages(self):
        mocked_evaluator = mock.MagicMock(name="Test")
        mocked_date = mock.MagicMock()
        mocked_evaluator._get_day_duration.return_value = 10000
        mocked_evaluator._get_week_average.return_value = 1000
        mocked_evaluator._get_month_average.return_value = 1000
        summ = summarizer.Summarizer(mocked_evaluator)

        summ.print_averages(mocked_date)
        mocked_evaluator._get_day_duration.assert_called_once_with(mocked_date)
        mocked_evaluator._get_week_average.assert_called_once_with(mocked_date)
        mocked_evaluator._get_month_average.assert_called_once_with(mocked_date)
