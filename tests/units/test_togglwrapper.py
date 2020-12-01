from unittest import TestCase, mock

import deep_toggl.togglwrapper as toggl

PROJECT = "Thesis"
DEEP_TAG = ["deep"]
TOKEN = "asdf"
TZ = "utc"


class TestToggl(TestCase):
    @mock.patch("deep_toggl.togglwrapper.api")
    def test_load_data(self, mocked_api):
        with mock.patch(
            "deep_toggl.togglwrapper.api.Project.objects.filter",
            return_value=["testing"],
        ) as mocked_project_filter_api:

            toggl.load_from_toggl(PROJECT, DEEP_TAG, TOKEN, TZ)
            mocked_project_filter_api.assert_called_once()
            mocked_api.TimeEntry.objects.filter.assert_called_once()
            _, kwargs = mocked_api.TimeEntry.objects.filter.call_args
            self.assertEqual(kwargs["project"], "testing")
            self.assertEqual(kwargs["tags"], {*DEEP_TAG})
