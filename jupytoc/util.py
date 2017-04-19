import os


def find_notebooks_recursively(root_path='.'):
    for root, _, files in os.walk(root_path, topdown=True):
        for name in files:
            if os.path.join(root, name).endswith(NOTEBOOK_EXTENSION) and os.path.basename(root) not in TO_EXCLUDE:
                yield os.path.join(root, name)


def get_tuple_without_item(original_tuple, element_to_remove):
    list_ = list(original_tuple)
    list_.remove(element_to_remove)
    return tuple(list_)


def is_file_not_empty(filepath):
    return os.path.getsize(filepath) > 0
