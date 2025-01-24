from enum import Enum


class FiltersEndpoint(Enum):
    REPORT = "action/filterBy={}/status"
    DETAILED_REPORT = "action/filterBy={}/report?pageNumber=1&pageSize=50&severity={}"
