import argparse
import ast
import glob
import os


import cv2
import pandas as pd

from utils import process_image


def main():
    parser = argparse.ArgumentParser(
        prog='test_visual.py', description='Given an input directory, creates a new directory in there, where the pictures have the corresponding keypoints and lines on them.')

    parser.add_argument(
        'input_dir',  help='The input directory. Should have pictures and corresponding labels.csv inside.')
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = input_dir + '/test_visual'
    os.makedirs(output_dir, exist_ok=True)

    files = glob.glob(input_dir + '/*.png')
    files = sorted(files)

    df = pd.read_csv(input_dir + '/labels.csv')

    def to_tuple(str_tuple):
        return ast.literal_eval(str_tuple)

    for file in files:
        np_array, image = process_image(file)
        # from now on only basename needed
        file = os.path.basename(file)
        csv_row = df[df['image_name'] == file]
        if csv_row.empty:
            continue
        csv_row = csv_row.iloc[0]
        vp = to_tuple(csv_row.iloc[1])
        ll = to_tuple(csv_row.iloc[2])
        lr = to_tuple(csv_row.iloc[3])

        image = cv2.circle(image, (vp[0], vp[1]), 5, (255, 0, 0), -1)
        image = cv2.circle(image, (ll[0], ll[1]), 5, (0, 255, 0), -1)
        image = cv2.circle(image, (lr[0], lr[1]), 5, (0, 0, 255), -1)

        cv2.imwrite(os.path.join(output_dir, file[:-4] + '_test.png'), cv2.cvtColor(
            image, cv2.COLOR_RGB2BGR))


if __name__ == '__main__':
    main()
