from rest_framework.pagination import  PageNumberPagination,LimitOffsetPagination,CursorPagination
# its page size pagination
class WatchListPagination(PageNumberPagination):
    page_size =  10
    # page_query_param = 'p'# update page= 2 to p=2
    page_size_query_param='size'# need to submit the size add, ?size = 10 to the URL
    max_page_size = '1000'# max we could add to one page = 1000
    last_page_strings ='end'# ?p=last
    
class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit =  10
    limit_query_param = 'limit'
    offset_query_param =  'start'
    # from 5 position
class WatchListCPagination(CursorPagination):
    page_size = 5
    ordering  = 'created'# -created by default
    cursor_query_param = 'record'
    
    
    
# works with viewset or generic classes only
    


