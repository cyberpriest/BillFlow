def Pagination(page:int,limit:int):
    skip = (page-1)*limit
    return skip,limit