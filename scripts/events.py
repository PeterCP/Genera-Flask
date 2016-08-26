from app.models import EventCategory, db

def create_or_update_event_category(cat_dict):
    cat = EventCategory.get_or_create(name=cat_dict['name'])
    # if cat.default_image_path is None:
    #     cat.default_image_path = cat_dict['default_image_path']
    cat.save(True)
