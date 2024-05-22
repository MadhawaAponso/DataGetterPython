import xml.etree.ElementTree as ET
import psycopg2
import multiprocessing
import sys
from collections import Counter
from services import get_file_names, has_repeated_immediate_child_tags
from Database_Functions import create_table_and_insert_data
from Recursive_Function import reccursiveMethod

sys.stdout.reconfigure(encoding='utf-8')

def parallel_process(args):
    root, target_tag, path , repeatTags = args
    out1 = {}
    Flist1 = []
    datasets = reccursiveMethod(root, target_tag, path, out1, Flist1, repeatTags)
    return Flist1

# REQUIREMENTS_COMP : D:\\Projects\\DataGetter\\Requiremnts
# REAUIREMENTS DETAILED : D:\\Projects\\DataGetter\\RequirementsDetailed
#D:\\Projects\\DataGetter\\TestCaseDetailed

def main():
    connection_string = "dbname='XMLDB' user='postgres' host='localhost' password='madhawa'"
    folder_path = "D:\\Projects\\DataGetter\\hasanga"
    file_list = get_file_names(folder_path)
    table_name = "hasanga"
    max_processes = 4

    Final_List = []
    l = []

    for file in file_list:
        xml_file = f'D:\\Projects\\DataGetter\\hasanga\\{str(file)}'
        print(xml_file)
        tree = ET.parse(xml_file)
        root1 = tree.getroot()

        target_list = [tag for tag in root1 if has_repeated_immediate_child_tags(tag)]
        if target_list == []:
            target_tag1 = list(root1)[-1]
        else:
            target_tag1 = target_list[0]

        path1 = 'Root'

        multi_process_tags = [tag for tag in target_tag1 if len(list(tag)) > 0]
        
        repeatTags = multiprocessing.Manager().list()

        # Create a pool of processes
        with multiprocessing.Pool(processes=max_processes) as pool:
            args = [(root1, tag, f'{str(root1.tag)}_{target_tag1.tag}', repeatTags) for tag in multi_process_tags]

            result_list = pool.map(parallel_process, args)

        for sublist in result_list:
            for item in sublist:
                if item not in Final_List:
                    Final_List.append(item)
        print(file, "is processed")

    print(l)
    element_counts = Counter(l)
    repeated_elements_dict = {element: count for element, count in element_counts.items() if count > 1}
    print("Repeated elements and their counts:", repeated_elements_dict)

    try:
        with psycopg2.connect(connection_string) as conn:
            with conn.cursor() as cursor:
                create_table_and_insert_data(cursor, Final_List, table_name)
                conn.commit()
                print("Table created and data inserted successfully!")
    except psycopg2.Error as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
