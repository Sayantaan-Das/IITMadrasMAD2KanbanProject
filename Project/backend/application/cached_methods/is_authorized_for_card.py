from application.utils.cache_system import cache
from werkzeug.exceptions import Unauthorized
from application.models import TaskList as model_task, Card as model_card

@cache.memoize(100)
def is_authorized_for_the_card(id, user_id):
    if (model_task.query.filter_by(id=model_card.query.filter_by(id=id).first().card_listId).first().list_userId==user_id):
                return True
    else:
        raise Unauthorized