import os

os.chdir('..')

DATASET = "data_example_1.ttl"
OUTFILE_NAME = "data.txt"
DATA_DIR = os.path.join(os.getcwd(), "data")
DATA_PATH = os.path.join(DATA_DIR, DATASET)
OUTPUT_PATH = os.path.join(DATA_DIR, OUTFILE_NAME)
