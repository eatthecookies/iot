import xmltodict
from datetime import datetime
from prettytable import PrettyTable
from main import FILENAME_XML, __DATE_FORMAT__


class Parser:
    def read(self):
        with open(FILENAME_XML, 'r', encoding='utf8') as f:
            self.data = xmltodict.parse(f.read())['Data']['Record']
        print(self.data)


    # функция для отображения данных в виде таблицы
    def print_data(self):
        table = PrettyTable()

        table.field_names = ["ID", "CO2", "Sound Level", "Illuminance", "Temperature", "Date"]
        for i, data in enumerate(self.data):
            table.add_row([i + 1, data['CO2'],
                           data['Sound_Level'], data['Illuminance'],
                           data['Temperature'], datetime.strptime(data['Date'], __DATE_FORMAT__)])
        print(table)

if __name__ == "__main__":
    p = Parser()
    p.read()
    p.print_data()