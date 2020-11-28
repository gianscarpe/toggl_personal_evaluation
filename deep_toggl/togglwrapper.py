from typing import Set, Union

import pendulum
from toggl import api, utils

from .config import ANY_TAG


def _parse_tags(tags: list) -> Union[Set, None]:
    if ANY_TAG in tags:
        return None
    return {*tags}


def load_from_toggl(project_name: str, tags: list, token, timezone) -> list:
    config = utils.Config.factory(
        None
    )  # Without None it will load the default config file
    config.api_token = token
    config.timezone = timezone

    start = pendulum.now().start_of("year")

    project = api.Project.objects.filter(name=project_name, config=config)[0]
    project_entries = api.TimeEntry.objects.filter(
        project=project,
        start=start,
        tags=_parse_tags(tags),
        config=config,
        contain=False,
    )
    return project_entries
