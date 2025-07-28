
class CSV:
    def __init__(self):
        self.__header = None
        self.__rows = None

    def set_header(self, header):
        self.__header = header

    def set_rows(self, rows):
        self.__rows = rows

    def export(self):
        result = self.__header + "\n"
        for row in self.__rows:
            for item in row.values():
                result += f'{item},'
            result = result[:-1]
            result += "\n"

        return result