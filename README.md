# tablemanager

I had a series of projects where I needed tables with filter, sort, 
and pagination options to be available, and I needed to keep a record
of the status that tables was in, when the user navigates away from the
given page.

The original code used the Django session manager and pagination classes
but I've updated this, so its framework agnostic. 

The system works by having a dataclass TableSession, which holds the
status of the table request. This object can then be placed in session data,
in the db, or cached. It just need to be placed somewhere it be accessed
across requests.

The Table Session then needs to be passed to the TableManager object
along with the data for the table. This is set to use a list of dictionaries.
It does not take query objects.


## getting Started.

* Create/extract a Table session object.
* make updates (if old session) to the Table session
* Extract records from the database using any preset filters or sorting you want, but extract
* directly to a list of dictionaries, not to a queryset.
* Pass the TableSession and data to the TableManager
* Pass the TableManager object to your template


```python
from table_manager import TableSession
from table_manager import TableManager
from models import MyModel

session = TableSession("user1_table1", ["id", "user", "field1", "field2"], 
                       filter_options=["user", "field1"], filter_text="", 
                       page_number=1, page_size=10, sort_options=["id", "user", "field2"], 
                       sort_by="id")

data = MyModel.objects.filter(user=request.user).values()
table_object = TableManager(session, data)
table_object.paginator.page()  ## current page records
table_object.paginator.has_next()  ## is there a next page
table_object.paginator.has_previous() ## is there a previous page
table_object.table_session.display_fields  ## list of headers/keys in order
table_object.table_session.sort_options  ## list of sort options
table_object.table_session.sort_by  ## current sort setting
table_object.table_session.filter_text  ## current filter text
table_object.table_session.page_number  ## current page
```
