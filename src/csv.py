
class CSV:
    def __init__(self, header, rows):
        self.__header = header
        self.__rows = rows

    def output(self):
        result = self.__header + "\n"
        for row in self.__rows:
            for item in row.values():
                result += f'{item},'
            result = result[:-1]
            result += "\n"

        return result