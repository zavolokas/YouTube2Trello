from os import listdir
from os.path import isfile, join, splitext, basename
import logging
import csv


logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(filename='log.txt',level=logging.DEBUG)

MY_PATH = "./data"

def convert_txt_to_csv(file_path):
    logging.debug(splitext(file_path))
    path, extension = splitext(file_path)
    if extension != ".txt":
        return

    video_id = basename(path)

    csv_file_name = path + ".csv"
    logging.info(f"Convert {file_path} to CSV({csv_file_name})")
    with open(csv_file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["video_id", "order", "star_time", "end_time", "content"])

        order = 0
        with open(file_path) as input_file:
            time_line = input_file.readline()
            text_line = input_file.readline()
            empty_line = input_file.readline()
            while text_line:
                start, end = _parse_start_end(time_line)
                text = text_line.rstrip('\n')
                writer.writerow([video_id, order, start, end, text])
                time_line = input_file.readline()
                text_line = input_file.readline()
                empty_line = input_file.readline()
                order += 1


def _parse_start_end(line):
    start, end = line.rstrip('\n').split(',')
    return start, end

if __name__ == "__main__":
    input_files = [join(MY_PATH, f) for f in listdir(MY_PATH) if isfile(join(MY_PATH, f))]
    logging.info(f"Found files: {input_files}")

    for file_name in input_files:
        convert_txt_to_csv(file_name)