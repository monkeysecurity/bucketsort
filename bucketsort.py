"""
Bucket sort.

Usage:
  bucketsort generate_phone_numbers [--number=<number>] --file=<filename>
  bucketsort sort_numbers --file=<filename> [--num_buckets=<num_buckets>]

Options:
  -h --help     Show this screen.
  --version     Show version.
  --number=<number>   Number of phone numbers to generate. [Default: 10].
  --file=<filename>   Filename to read/write json to. [Default: output.json].
  --num_buckets=<num_buckets>  Number of buckets to use in sorting [Default: 10].
"""
from docopt import docopt
from random import randint
import json


def random_phone_number():
    phone_number = ''
    for i in range(0,10):
        phone_number += str(randint(0,9))
    return phone_number


def generate_phone_numbers(number=10):
    numbers = []
    for i in range(int(number)):
        numbers.append(random_phone_number())
    return numbers


def write_file(filename, data):
    with open(filename, 'w') as output_file:
        output_file.write(
            json.dumps(
                data,
                indent=2
            )
        )


def read_file(filename):
    with open(filename) as json_file:
        json_data = json.load(json_file)
    return json_data


def _insertion_sort(seq):
    for i in range(1, len(seq)):
        j = i
        while j > 0 and seq[j - 1] > seq[j]:
            seq[j - 1], seq[j] = seq[j], seq[j - 1]
            j -= 1


def bucket_sort(input, num_buckets=10):
    # 1) make buckets
    buckets = {i:[] for i in range(0,int(num_buckets))}

    # 2) largest value
    largest = 0
    for i in input:
        if int(i) > largest:
            largest = int(i)

    # 3) insert items into buckets
    for item in input:
        key = int(float(item) / float(largest) * int(num_buckets)-1)
        buckets[key].append(item)

        # Uncomment this and comment out step 4.
        # This method is slightly slower than step 4.
        # _insertion_sort(buckets[key])

    # print json.dumps(buckets, indent=2)

    # 4) sort individual buckets with insertion sort
    for _,bucket in buckets.items():
        bucket = _insertion_sort(bucket)

    # 5) concat all buckets into output string
    sorted_phone_numbers = []
    for i in range(0,int(num_buckets)):
        sorted_phone_numbers.extend(buckets[i])
    return sorted_phone_numbers


if __name__ == "__main__":
    arguments = docopt(__doc__)
    print arguments

    import time
    time1 = time.time()

    if arguments['generate_phone_numbers']:
        numbers = generate_phone_numbers(number=arguments['--number'])
        print json.dumps(numbers, indent=2)
        write_file(arguments['--file'], numbers)

    elif arguments['sort_numbers']:
        input = read_file(arguments['--file'])
        sorted_numbers = bucket_sort(input, num_buckets=arguments['--num_buckets'])
        # print json.dumps(sorted_numbers, indent=2)

    time2 = time.time()
    print "Took %0.1f s" % (time2-time1)