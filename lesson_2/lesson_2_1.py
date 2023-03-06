import re
import csv


def get_data():
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []

    main_data = [["Изготовитель системы", "Название ОС", "Код продукта", "Тип системы"]]

    for file_num in range(1, 4):
        with open(f"info_{file_num}.txt") as f:
            file_data = f.read()

            os_prod = re.findall(r"Изготовитель ОС:\s+(.*)", file_data)[0]
            os_name = re.findall(r"Название ОС:\s+(.*)", file_data)[0]
            os_code = re.findall(r"Код продукта:\s+(.*)", file_data)[0]
            os_type = re.findall(r"Тип системы:\s+(.*)", file_data)[0]

            os_prod_list.append(os_prod)
            os_name_list.append(os_name)
            os_code_list.append(os_code)
            os_type_list.append(os_type)

            main_data.append([os_prod, os_name, os_code, os_type])

    return os_prod_list, os_name_list, os_code_list, os_type_list, main_data


def write_to_csv(file_path):
    os_prod_list, os_name_list, os_code_list, os_type_list, main_data = get_data()

    with open(file_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        for row in main_data:
            writer.writerow(row)

    print(f"Данные сохранены в файл {file_path}")


write_to_csv("report.csv")
