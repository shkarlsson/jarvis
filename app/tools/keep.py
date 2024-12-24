# %%

import gkeepapi
import json

from difflib import get_close_matches

from app.helpers.paths import APP_DIR
from app.helpers.env_vars import GOOGLE_TOKEN as master_token, SHOPPING_LIST_TITLE


def connect_to_keep():
    keep = gkeepapi.Keep()
    success = keep.authenticate("", master_token)
    return keep, success


# %%


def get_note_by_title(keep):

    note = next((n for n in keep.all() if n.title == SHOPPING_LIST_TITLE), None)
    if note is None:
        print(f"Note '{SHOPPING_LIST_TITLE}' not found.")

    return note


def add_to_shopping_list(items):
    keep, success = connect_to_keep()
    """Add items to the shopping list (separate several items with commas)"""
    note = get_note_by_title(keep)
    if note is None:
        return

    if isinstance(items, str):
        if "," in items:
            items = items.split(",")
        else:
            items = [items]

    for item in items:
        note.add(item.strip().capitalize(), False)
    keep.sync()

    return f"Added items to the shopping list: {items}"


def check_shopping_list():
    """Check the items on the shopping list"""
    keep, success = connect_to_keep()
    note = get_note_by_title(keep)
    if note is None:
        return

    return [item.text for item in note.items if not item.checked]


def remove_from_shopping_list(remaining_items):
    """Remove items from the shopping list (separate several items with commas)"""
    keep, success = connect_to_keep()
    note = get_note_by_title(keep)
    if note is None:
        return "Couldn't get the list. 🤔"

    if not note.items:
        return "No items to remove. List is empty. 🙀"

    if isinstance(remaining_items, str):
        if "," in remaining_items:
            remaining_items = remaining_items.split(",")
        else:
            remaining_items = [remaining_items]

    remaining_items = [item.lower().strip() for item in remaining_items]

    deleted_items = []

    for note_item in note.items:
        # If item is checked, skip it
        if note_item.checked:
            continue

        # Use fuzzy matching to find close matches
        close_matches = get_close_matches(
            note_item.text, remaining_items, n=1, cutoff=0.8
        )

        if close_matches:
            item_to_remove = close_matches[0]
            note_item.checked = True
            remaining_items.remove(item_to_remove)
            deleted_items.append(note_item.text)

    keep.sync()

    return {
        "deleted": deleted_items,
        "not_found": remaining_items,
    }


def test_shopping_list_tools():
    test_str = (
        "Test1639343"  # Should be capitalized because it is how it is added to the list
    )
    try:
        add_to_shopping_list([test_str])

        if test_str not in check_shopping_list():
            print("Error adding item to shopping list")
            return False
        remove_from_shopping_list([test_str])
        if test_str in check_shopping_list():
            print("Error removing item from shopping list")
            return False
        return True
    except Exception as e:
        print(f"Error testing shopping list tools: {e}")
        return False
