from datetime import datetime
from application.utils.cache_system import cache
from application.cached_methods.summary_by_month import summary_by_month
from application.cached_methods.trendline import generate_trendline_completed
from application.cached_methods.is_authorized_for_card import is_authorized_for_the_card

def cached_data_cleaner(user_id, task_list_id=None, card_id=None):
    cache.delete_memoized(summary_by_month,user_id)
    cache.delete_memoized(summary_by_month,user_id,datetime.now().date().year,datetime.now().month)

    if task_list_id:
        cache.delete_memoized(generate_trendline_completed,task_list_id)
        print("Cache deleted")

    if card_id:
        cache.delete_memoized(is_authorized_for_the_card, user_id, card_id)


        
    
