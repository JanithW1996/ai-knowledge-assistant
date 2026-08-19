"""Tests for the local application."""

from src.app import main


def test_main_states_synthetic_data_policy(capsys) -> None:
    """The application must clearly state its data boundary."""
    main()

    output = capsys.readouterr().out

    assert "synthetic" in output.lower()
    assert "fictional" in output.lower()