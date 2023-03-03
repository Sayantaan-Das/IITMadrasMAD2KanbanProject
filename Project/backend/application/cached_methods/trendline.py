from application.models import Card as model_card
from matplotlib import dates as mdates
from matplotlib.figure import Figure
from datetime import timedelta
from io import BytesIO
import base64
from flask import current_app
from application.utils.cache_system import cache


@cache.memoize(900)
def generate_trendline_completed(task_list):
    current_app.logger.info("Generating Trendline function Started!")
    cards_list=model_card.query.filter_by(card_listId=task_list).all()
    data={
        "card_completed_on":[],
        "card_title":[]
    }
    
    if cards_list:
        current_app.logger.info("Cards Found!")
        for card in cards_list:
            if (card.card_status):
                data["card_completed_on"].append(card.card_completed_on)
                current_app.logger.error(card.card_completed_on)
                data["card_title"].append(card.card_title)
                current_app.logger.error(card.card_completed_on)
            
        if data["card_completed_on"]:

            current_app.logger.info("Generating Trendline!")

            fig=Figure()
            ax=fig.subplots()
            ax.yaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

            ax.plot_date(data["card_title"],data["card_completed_on"],linestyle="solid")

            plotting_bytes=BytesIO()
            fig.tight_layout()
            fig.savefig(plotting_bytes,format="png")
            plotting_bytes.seek(0)
            trendline_base64_string=base64.b64encode(plotting_bytes.getbuffer()).decode("ascii")

            return (trendline_base64_string)

    else:
        return 0







