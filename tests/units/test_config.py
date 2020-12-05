from unittest import TestCase
from unittest.mock import Mock, patch

from deep_toggl.config import ANY_TAG, TogglWrapper, get_chosen_projects, get_chosen_tags


class TestConfig(TestCase):
    @patch("deep_toggl.config.inquirer")
    def test_get_chosen_projects(self, in_mock):
        toggl_wrap = Mock(spec=TogglWrapper)
        projects_names = ["p1", "p2"]
        toggl_wrap.get_all_projects.return_value = [Mock(name=pn) for pn in projects_names]
        in_mock.prompt.return_value = {"projects": projects_names}
        res = get_chosen_projects(toggl_wrap)

        in_mock.Checkbox.assert_called_once()
        in_mock.prompt.assert_called_once()
        self.assertEqual(projects_names, res)

    @patch("deep_toggl.config.inquirer")
    def test_get_chosen_tags(self, in_mock):
        toggl_wrap = Mock(spec=TogglWrapper)
        tags_names = ["t1", "t2"]
        full_tags_names = [ANY_TAG] + tags_names
        toggl_wrap.get_all_tags.return_value = [Mock(name=tn) for tn in tags_names]
        in_mock.prompt.return_value = {"tags": full_tags_names}
        res = get_chosen_tags(toggl_wrap, "p1")

        in_mock.Checkbox.assert_called_once()
        in_mock.prompt.assert_called_once()
        self.assertEqual(full_tags_names, res)
