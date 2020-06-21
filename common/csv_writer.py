import csv
import codecs
import os


def writer_csv(filename, data_header, data_body):
    data = [];
    with open(filename, 'a', newline='', encoding='utf-8-sig') as csvFile:
        writer = csv.writer(csvFile)
        with open(filename, "r+", encoding='utf-8-sig', newline="") as f:
            reader = csv.reader(f)
            row_data = [row for row in reader]
            if len(row_data) == 0:
                # 先写columns_name
                writer.writerow(data_header)
                data.append(data_body)
                writer.writerows(data)
            # 写入多行用writerows
            else:
                for i, item in enumerate(row_data):
                    if item == data_body:
                        return
                data.append(data_body)
                writer.writerows(data)

