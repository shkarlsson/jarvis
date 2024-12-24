# %%

import gkeepapi
import json

from difflib import get_close_matches

from app.helpers.paths import APP_DIR
from app.helpers.env_vars import GOOGLE_TOKEN as master_token, SHOPPING_LIST_TITLE

keep = gkeepapi.Keep()
success = keep.authenticate("", master_token)


# %%


def get_note_by_title(title):
    note = next((n for n in keep.all() if n.title == title), None)
    if note is None:
        print(f"Note '{title}' not found.")

    return note


def add_to_shopping_list(items):
    """Add items to the shopping list (separate several items with commas)"""
    note = get_note_by_title(SHOPPING_LIST_TITLE)
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
    note = get_note_by_title(SHOPPING_LIST_TITLE)
    if note is None:
        return

    return [item.text for item in note.items if not item.checked]


# %%


def remove_from_shopping_list(remaining_items):
    """Remove items from the shopping list (separate several items with commas)"""
    note = get_note_by_title(SHOPPING_LIST_TITLE)
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
            print(f"Checked item: {note_item.text}")
            remaining_items.remove(item_to_remove)
            deleted_items.append(note_item.text)

    keep.sync()

    return {
        "deleted": deleted_items,
        "not_found": remaining_items,
    }
