from werkzeug.exceptions import HTTPException

class NoDataFound(HTTPException):
    code=461
    name="No Data Found"
    description="The database has no entries to be returned for this search query"


    

