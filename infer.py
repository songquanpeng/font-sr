import ntpath
import os

from tqdm import tqdm

from data import create_dataset
from models import create_model
from options.test_options import TestOptions
from util import util

if __name__ == '__main__':
    opt = TestOptions().parse()  # get test options
    # hard-code some parameters for test
    opt.num_threads = 0  # test code only supports num_threads = 0
    opt.batch_size = 1  # test code only supports batch_size = 1
    opt.serial_batches = True  # disable data shuffling; comment this line if results on randomly chosen images are needed.
    opt.no_flip = True  # no flip; comment this line if results on flipped images are needed.
    opt.display_id = -1  # no visdom display; the test code saves the results to a HTML file.
    dataset = create_dataset(opt)  # create a dataset given opt.dataset_mode and other options
    model = create_model(opt)  # create a model given opt.model and other options
    model.setup(opt)  # regular setup: load and print networks; create schedulers

    output_path = os.path.join('results', opt.name, os.path.basename(opt.dataroot))
    os.makedirs(output_path, exist_ok=True)

    model.eval()
    for i, data in tqdm(enumerate(dataset), total=len(dataset)):
        model.set_input(data)  # unpack data from data loader
        model.test()  # run inference
        visuals = model.get_current_visuals()  # get image results
        image_path = model.get_image_paths()  # get image paths
        short_path = ntpath.basename(image_path[0])
        name = os.path.splitext(short_path)[0]
        ims_dict = {}
        for label, im_data in visuals.items():
            if label == 'fake_B':
                im = util.tensor2im(im_data)
                save_path = os.path.join(output_path, f'{name}.png')
                util.save_image(im, save_path, aspect_ratio=opt.aspect_ratio)
