from aihub_email.cli import build_parser


def test_refresh_snapshot_command_accepts_expected_options():
    parser = build_parser()

    args = parser.parse_args(
        [
            "refresh-snapshot",
            "--account",
            "default",
            "--limit",
            "5",
            "--top",
            "3",
            "--ascii",
        ]
    )

    assert args.command == "refresh-snapshot"
    assert args.account == "default"
    assert args.limit == 5
    assert args.top == 3
    assert args.ascii is True
