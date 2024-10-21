from datetime import datetime


class DateTimeHelper:

    @staticmethod
    def convert_seconds_to_time_string(seconds: int) -> str:
        hrs = seconds // 3600
        mins = (seconds % 3600) // 60
        secs = seconds % 60
        return f'{hrs}h {mins}m {secs}s'

    @staticmethod
    def create_datetime_from_input(date_str: str) -> datetime:  # TODO add support for other date formats
        date = datetime.strptime(date_str, '%m/%d/%Y')
        return datetime(year=date.year, month=date.month, day=date.day)

    @staticmethod
    def convert_to_seconds(hours: int, minutes: int) -> int:
        return 3600 * hours + 60 * minutes

    @staticmethod
    def convert_datetime_to_string(selected_date: datetime) -> str:  # TODO add support for other date formats
        return selected_date.strftime('%d. %m. %Y')
