import numpy as np  # pylint: disable=import-error

from skimage.data import imread as skimage_read  # pylint: disable=import-error
from os.path import join

from utils import resize_image
from fs_utils import list_subdirs, list_files, PROJ_ROOT


def _load(data_dir):
    dataset = []
    for subdir in list_subdirs(data_dir):
        files = list_files(join(data_dir, subdir), ext='.ppm')
        for file_name in files:
            file_path = join(data_dir, subdir, file_name)
            dataset.append({
                'data': skimage_read(file_path),
                'label': subdir
            })
    return dataset


def load_training():
    return _load(f'{PROJ_ROOT}/data/btsc/training/Training')


def load_testing():
    return _load(f'{PROJ_ROOT}/data/btsc/testing/Testing')


def load_full_dataset():
    return load_training() + load_testing()


def resize_images(image_data, size=None):
    assert isinstance(size, int), 'size must be an integer'
    resized_images = []
    for image_datum in image_data:
        resized_images.append({
            'data': resize_image(image_datum['data'], size),
            'label': image_datum['label']
        })
    return resized_images


def split_images_and_labels(image_data):
    images = []
    labels = []
    for instance in image_data:
        images.append(instance['data'])
        labels.append(instance['label'])
    return (np.array(images), np.array(labels))
