def generate_html_collapsible_tree(parent_categories):
    html_tree = '<div class="collapsible-tree"><ul>'
    for category in parent_categories:
        html_tree += '<div id="category-' + str(category.id) + '" class="collapsible-tree-node">'
        subcategories = category.subcategory.all().order_by('pk')
        if len(subcategories) != 0:
            html_tree += '<span class="collapse-button">+</span><li>' + category.name + '</li>'
            html_tree += generate_html_collapsible_tree(subcategories)
        else:
            html_tree += '<li>' + category.name + '</li>'
        html_tree += '</div>'

    html_tree += '</ul></div>'
    return html_tree
