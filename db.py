from datetime import datetime


class Reading:
    # TODO: change this to represent whatever information is needed
    def __init__(self, time, name, value) -> None:
        self.time = time
        self.name = name
        self.value = value

    def to_json(self):
        return {
            "time": self.time,
            "name": self.name,
            "value": self.value
        }

# This is a fake database which stores data in-memory while the process is running
# Feel free to change the data structure to anything else you would like
database: list[Reading] = []


def add_reading(reading: Reading) -> None:
    """
    Store a reading in the database using the given key
    """
    database.append(reading)


def get_reading(fromDate: datetime.date, toDate: datetime.date) -> Reading | None:
    """
    Retrieve a reading from the database using the given key
    """
    filteredRecords = [ record for record in database if (record.time.date() >=fromDate) and (record.time.date() <=toDate)]
    return filteredRecords