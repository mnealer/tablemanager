import json
from operator import itemgetter
from dataclasses import dataclass
from typing import List


@dataclass
class TableSession:
    """
    TableSession is the data that is to be stored between sessions. You can place this in
    cache or in session data etc, depending on your system.

    name: Name of the table session/manager to be stored. used to differencate between tables
    display_fields: list of the columns that should be displayed on the table
    filter_options: List of record keys that will be used to filter on.
    filter_text: text that will be used to filter on.
    sort_options: list of record keys that can be used to sort on.
    sort_by: key that will be used to sort on.
    page_number: last page that was requested on the table
    page_size: the page size requested
    """
    name: str
    display_fields: List[str]
    filter_options: List[str]
    filter_text: str
    page_number: int
    page_size: int
    sort_options: List[str]
    sort_by: str


class TablePaginator:
    """
    This is a framework agnostic class that allows you to paginate your tables.
    Data should be passed as a list of dictionaries. All dictionaries should have the same keys
    """
    def __init__(self, data, page_size, page_number):
        if not data:
            raise ValueError("No data to paginate")
        if not page_size or page_size < 1:
            raise ValueError("Page size must be > 0")
        self.data = data
        self.page_size = page_size
        self.page_count = (-(-len(self.data) // self.page_size))
        self.page_number = page_number

    def page(self):
        """
        returns the records for the current page
        :return:
        """
        return self.data[self.page_number * self.page_size: (self.page_number + 1) * self.page_size]

    def last_page(self):
        """
        Boolean used to test if the table is on the last page
        :return:
        """
        return self.data[(self.page_count-1) * self.page_size: -1]

    def has_next(self, number):
        """
        Boolean used to test if there is a next page
        :param number:
        :return:
        """
        if number < self.page_count:
            return True
        else:
            return False

    @staticmethod
    def has_previous(number):
        """
        boolean used to test if there is a previous page
        :param number:
        :return:
        """
        if number > 1:
            return True
        else:
            return False


class TableManager:
    """
    This class creates a tablemanager object you can pass to your templates or
    other objects. The Table Session object holds the current settings for the
    table, and paginator will return the records for the page as well as the
    page count etc
    """

    def __init__(self, table_session: TableSession, data: list):
        self.data = data
        self.table_session = table_session
        self.__filter__()
        self.__sort__()
        self.paginator = TablePaginator(self.data,
                                        self.table_session.page_size,
                                        self.table_session.page_number)

    def __filter__(self) -> None:
        if self.table_session.filter_text:
            self.data = [row for row in self.data if self.__filter_conditional__(row)]

    def __filter_conditional__(self, dic: dict) -> bool:
        if self.table_session.filter_options:
            for fltr in self.table_session.filter_options:
                if fltr in dic.keys():
                    if isinstance(dic[fltr], str):
                        if self.table_session.filter_text.lower() in dic[fltr].lower():
                            return True
                    elif isinstance(dic[fltr], dict) or isinstance(dic[fltr], list):
                        test_data = json.dumps(dic[fltr]).lower()
                        if self.table_session.filter_text.lower() in test_data:
                            return True
            return False
        else:
            fields = dic.keys()
            for field in fields:
                if isinstance(dic[field], str):
                    if self.table_session.filter_text.lower() in dic[field].lower():
                        return True
            return False

    def __sort__(self) -> None:
        if self.table_session.sort_by:
            if "-" in self.table_session.sort_by[0]:
                sort = self.table_session.sort_by[1:]
                self.data = sorted(self.data, key=itemgetter(sort), reverse=True)
            else:
                self.data = sorted(self.data, key=itemgetter(self.table_session.sort_by))

