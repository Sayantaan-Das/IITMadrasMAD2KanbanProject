from application.models import Card as model_card, TaskList as model_task
from flask_restful import fields, marshal_with
from flask import current_app
from datetime import datetime, timezone
from application.utils.cache_system import cache


summary_request_field={
    'id':fields.Integer,
    'list_title': fields.String,
    'list_description': fields.String,
    'no_cards': fields.Integer,
    'no_cards_completed': fields.Integer,
    'no_cards_incomplete': fields.Integer,
    'no_cards_deadline_crossed_incomplete': fields.Integer,
    'no_cards_completed_within_deadline': fields.Integer

}


def cards_counter(cards_set):
    number_cards=0
    number_cards_completed=0
    number_cards_incomplete=0
    number_cards_deadline_crossed_incomplete=0
    number_cards_completed_within_deadline=0

    for card in cards_set:
        number_cards=number_cards+1
        if(card.card_status):
            number_cards_completed=number_cards_completed+1
            if(card.card_completed_within_deadline is True):
                number_cards_completed_within_deadline=number_cards_completed_within_deadline+1
        else:
            number_cards_incomplete=number_cards_incomplete+1
        if((card.card_deadline>datetime.strptime(datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),"%Y-%m-%dT%H:%M:%S.%fZ")) and (not card.card_status)):
            number_cards_deadline_crossed_incomplete=number_cards_deadline_crossed_incomplete+1

    return_value={
        'no_cards': number_cards,
    'no_cards_completed': number_cards_completed,
    'no_cards_incomplete': number_cards_incomplete,
    'no_cards_deadline_crossed_incomplete': number_cards_deadline_crossed_incomplete,
    'no_cards_completed_within_deadline': number_cards_completed_within_deadline
    }

    return(return_value)

@cache.memoize(10000)
@marshal_with(summary_request_field)
def summary_by_month(user_id,year=None,month=None):
        current_app.logger.info("Summary Page started")
        summary_response=[]
        counter=0
        current_user_lists=model_task.query.filter_by(list_userId=user_id).all()
        for current_user_list in current_user_lists:
            summary_response.append(vars(current_user_list))
            current_list_cards=[]
            current_list_cards=model_card.query.filter_by(card_listId=current_user_list.id).all()

 
            if year and month:
                    for card in current_list_cards:
                        if not (card.card_deadline.date().year==year and card.card_deadline.date().month==month):
                            current_list_cards.pop(current_list_cards.index(card))
            elif year:
                    for card in current_list_cards:
                        if not (card.card_deadline.date().year==year):
                            current_list_cards.pop(current_list_cards.index(card))

            summary_response[counter].update(cards_counter(current_list_cards))
            counter=counter+1

        return summary_response









