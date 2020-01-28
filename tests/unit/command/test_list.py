from dvc.cli import parse_args
from dvc.command.list import CmdList


def test_list(mocker):
    cli_args = parse_args(["list", "repo_url"])
    assert cli_args.func == CmdList

    cmd = cli_args.func(cli_args)
    m = mocker.patch("dvc.repo.Repo.list_outs")

    assert cmd.run() == 0

    m.assert_called_once_with("repo_url", [], recursive=False, rev=None)
