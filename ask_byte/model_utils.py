from .models import *


def get_category_tree(parent_categories):
    category_tree = list()
    for category in parent_categories:
        tree_item = {'id': category.id, 'name': category.name}
        subcategories = category.subcategory.all()
        if len(subcategories) != 0:
            tree_item['subcategories'] = get_category_tree(subcategories)
        category_tree.append(tree_item)
    return category_tree
