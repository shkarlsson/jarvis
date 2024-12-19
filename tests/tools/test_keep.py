# test_shopping_list.py

import pytest
from unittest.mock import MagicMock, patch

# Assuming the functions are in a module named `shopping_list`
from app.tools.keep import (
    get_note_by_title,
    add_to_shopping_list,
    check_shopping_list,
    remove_from_shopping_list,
)
from app.helpers.env_vars import SHOPPING_LIST_TITLE


@pytest.fixture
def mock_keep():
    with patch("app.tools.keep.keep") as mock_keep:
        mock_note = MagicMock()
        mock_note.title = SHOPPING_LIST_TITLE
        mock_note.items = [
            gkeepapi.node.ListItem("Apples", False),
            gkeepapi.node.ListItem("Bananas", False),
        ]
        mock_keep.all.return_value = [mock_note]
        yield mock_keep


def test_get_note_by_title(mock_keep):
    note = get_note_by_title(SHOPPING_LIST_TITLE)
    assert note is not None


def test_add_to_shopping_list(mock_keep):
    result = add_to_shopping_list("Oranges, Grapes")
    assert result == "Added items to the shopping list: ['Oranges', ' Grapes']"
    mock_keep.sync.assert_called_once()


def test_check_shopping_list(mock_keep):
    items = check_shopping_list()
    assert items == "Apples, Bananas"


def test_remove_from_shopping_list(mock_keep):
    result = remove_from_shopping_list("apples")
    assert "Apples" in result
