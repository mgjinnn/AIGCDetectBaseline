import os
import time
import torch

from core.aigc_detector import AIGCDetector


def process_val(data_path):
    detector = AIGCDetector()
    t0 = time.time()
    ap, len_data = detector.val(data_path)
    time_cost = time.time() - t0
    print(f'time_cost: {time_cost}s')
    return ap, len_data/time_cost


if __name__ == '__main__':
    result_file = 'result.txt'
    if os.path.exists(result_file):
        os.remove(result_file)

    data_path = 'test_data'
    ap, speed = process_val(data_path)

    with open(result_file, 'a') as f:
        f.write('ap,' + str(round(ap, 4)) + ',' + str(round(speed, 4)) +'\n' )
