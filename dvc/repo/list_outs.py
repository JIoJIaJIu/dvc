import logging
import os


logger = logging.getLogger(__name__)


@staticmethod
def list_outs(url, targets=[], rev=None, recursive=None):
    if os.path.exists(url):
        path = os.path.abspath(url)
        return _list_outs_local_repo(path, targets, recursive)

    return _list_outs_git_repo(url, targets, rev, recursive)


def _list_outs_local_repo(path, targets=[], recursive=None):
    from dvc.repo import Repo
    from dvc.path_info import PathInfo

    repo = Repo(path)

    outs = set()
    for stage in repo.stages:
        outs = outs.union(stage.outs)

    matched_outs = []
    if len(targets):

        def func(out, path_info, is_dir):
            if out.scheme == "local" and out.path_info == path_info:
                return True

            if is_dir:
                if recursive and out.path_info.isin(path_info):
                    return True
                elif out.path_info.isin(path_info, 1):
                    return True

            return False

        for path in targets:
            abs_path = os.path.abspath(path)
            path_info = PathInfo(abs_path)
            is_dir = os.path.isdir(abs_path)
            matched = set()
            for out in outs:
                if func(out, path_info, is_dir):
                    matched.add(out)
                    matched_outs.append(out)
            outs.difference_update(matched)
    else:
        matched_outs = outs

    logger.info("\n".join(map(str, matched_outs)))


def _list_outs_git_repo(url, targets=[], rev="master", recursive=None):
    from dvc.external_repo import external_repo

    with external_repo(url, rev, sparse=True) as repo:
        targets = list(map(lambda t: os.path.join(repo.root_dir, t), targets))
        return _list_outs_local_repo(repo.root_dir, targets, recursive)
