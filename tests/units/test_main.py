from unittest import TestCase, mock

import deep_toggl


class TestLauncher(TestCase):
    @mock.patch("deep_toggl.get_config")
    @mock.patch("deep_toggl.summarize_all")
    @mock.patch("deep_toggl.summarize_project")
    @mock.patch("pendulum.now")
    def test_summarize_dispatch_to_project(
        self, mocked_pendulum, mocked_summ_project, mocked_summ_all, mocked_get_config
    ):
        project_name = "test"
        mocked_config = mock.MagicMock()
        mocked_now = mock.MagicMock()
        mocked_get_config.return_value = mocked_config
        mocked_pendulum.return_value = mocked_now

        deep_toggl.summarize_dispatch(project_name)
        mocked_get_config.assert_called_once()
        mocked_summ_project.assert_called_once_with(
            project_name, mocked_config, mocked_now
        )
        mocked_summ_all.assert_not_called()

    @mock.patch("deep_toggl.get_config")
    @mock.patch("deep_toggl.summarize_all")
    @mock.patch("deep_toggl.summarize_project")
    @mock.patch("pendulum.now")
    def test_summarize_dispatch_to_all(
        self, mocked_pendulum, mocked_summ_project, mocked_summ_all, mocked_get_config
    ):
        project_name = "all"
        mocked_config = mock.MagicMock()
        mocked_now = mock.MagicMock()
        mocked_get_config.return_value = mocked_config
        mocked_pendulum.return_value = mocked_now

        deep_toggl.summarize_dispatch(project_name)
        mocked_get_config.assert_called_once()
        mocked_summ_all.assert_called_once_with(mocked_config, mocked_now)
        mocked_summ_project.assert_not_called()

    @mock.patch("deep_toggl.get_evaluator")
    @mock.patch("deep_toggl.Summarizer")
    def test_summarize_project(self, mocked_summarizer_init, mocked_get_eval):
        project_name = "test"
        mocked_config = mock.MagicMock()
        mocked_now = mock.MagicMock()
        mocked_eval = mock.MagicMock()

        mocked_get_eval.return_value = mocked_eval

        deep_toggl.summarize_project(project_name, mocked_config, mocked_now)

        mocked_get_eval.assert_called_once()
        mocked_summarizer_init.return_value.print_averages.assert_called_once_with(
            mocked_now
        )

    @mock.patch("deep_toggl.summarize_project")
    def test_summarize_all(self, mocked_summ_project):
        mocked_config = {"projects": ["test1", "test2"]}
        mocked_now = mock.MagicMock()

        deep_toggl.summarize_all(mocked_config, mocked_now)
        mocked_summ_project.assert_has_calls(
            [mock.call("test1", mocked_config, mocked_now)]
        )
