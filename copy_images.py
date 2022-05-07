import argparse
import os
import shutil

from tqdm import tqdm


def main(args):
    filenames = os.listdir(args.input_path)
    os.makedirs(args.output_path, exist_ok=True)
    for filename in tqdm(filenames):
        shutil.copyfile(os.path.join(args.input_path, filename),
                        os.path.join(args.output_path, f"{args.prefix}{filename}"))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, required=True)
    parser.add_argument('--output_path', type=str, required=True)
    parser.add_argument('--prefix', type=str, default="type1_")
    main(parser.parse_args())
