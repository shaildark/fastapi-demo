import math

def generate_pagination(total_items, items_per_page, current_page):
    # Calculate the total number of pages
    total_pages = math.ceil(total_items / items_per_page)
    
    # Generate the pagination list
    pagination = []
    
    for page in range(1, total_pages + 1):
        pagination.append({
            "label": page,
            "page": page,
            "active": page == current_page
        })
    
    return pagination
