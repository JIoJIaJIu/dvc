import argparse
import logging

from dvc.command.base import append_doc_link
from dvc.command.base import CmdBaseNoRepo
from dvc.exceptions import DvcException


logger = logging.getLogger(__name__)


class CmdList(CmdBaseNoRepo):
    def run(self):
        from dvc.repo import Repo

        try:
            Repo.list_outs(
                self.args.url,
                self.args.targets,
                rev=self.args.rev,
                recursive=self.args.recursive,
            )
            return 0
        except DvcException:
            logger.exception("failed to list '{}'".format(self.args.url))
            return 1


def add_parser(subparsers, parent_parser):
    LIST_HELP = "List DVC outputs in the repo"
    list_parser = subparsers.add_parser(
        "list",
        parents=[parent_parser],
        description=append_doc_link(LIST_HELP, "list"),
        help=LIST_HELP,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    list_parser.add_argument(
        "url",
        help="Supported urls:\n"
        "/path/to/file\n"
        "/path/to/directory\n"
        "C:\\\\path\\to\\file\n"
        "C:\\\\path\\to\\directory\n"
        "https://github.com/path/to/repo\n"
        "git@github.com:path/to/repo.git\n",
    )
    list_parser.add_argument(
        "-R",
        "--recursive",
        action="store_true",
        help="Recursively list files under directory targets.",
    )
    list_parser.add_argument(
        "--rev", nargs="?", help="Git revision (e.g. branch, tag, SHA)"
    )
    list_parser.add_argument(
        "targets",
        nargs="*",
        help="Paths to directories within the repository to list outputs for.",
    )
    list_parser.set_defaults(func=CmdList)
