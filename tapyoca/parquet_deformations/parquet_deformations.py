"""
Generate intermediate images between any two images. That is, images that will give you the impression that
one image is being transformed into another.

Like parquet deformations, but not really parquets.

You can input color images, but they will be transformed to pure Black and White (every pixel is black, or white,
no grey).

The way it works is that a mapping between start and end black pixels is computed.
Every start pixel must have a end pixel matched, and visa-versa.
Then equally spaced points on the lines between matched coordinates are computed, and that's what defines the
intermediate images.

Here, the mapping is computed with a knn-based algo (essentially the union of the 1-nearest-neighbor of start in end,
and end in start).

"""
from sklearn.neighbors import NearestNeighbors
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

from io import BytesIO

import itertools

from py_fonts import courrier_ttf

def get_image(source):
    if isinstance(source, np.ndarray):
        source = image_from_matrix(source)
    elif isinstance(source, str):
        if os.path.isfile(source):
            source = Image.open(source)
        else:
            source = image_of_text(source)
    if not isinstance(source, Image.Image):
        raise TypeError("source type is not recognized")
    return source


def nonzero_coord_matrix(a):
    return np.array(list(zip(*np.nonzero(boolean_matrix_of_image(a)))))


def coordinates(*mats):
    return [nonzero_coord_matrix(m) for m in mats]


def knn_coordinates_mapping(start_mat, end_mat):
    # get matrix of coordinates of non-zero elements of images
    start_coords, end_coords = coordinates(start_mat, end_mat)

    # get a mapping between start coordinates and their closest end coordinates
    knn = NearestNeighbors(n_neighbors=1).fit(end_coords)
    _, start_to_end_knn_idx = knn.kneighbors(start_coords, n_neighbors=1)
    start_to_end_knn_idx = np.ravel(start_to_end_knn_idx)

    # but not all end_coords are ensured to be covered...
    unmatched_end_idx = list(set(range(len(end_coords))).difference(start_to_end_knn_idx))
    # print(len(unmatched_end_idx))
    unmatched_end_coords = end_coords[unmatched_end_idx]
    # ... so match remaining end coordinates to their closest start coord
    knn = NearestNeighbors(n_neighbors=1).fit(start_coords)
    _, end_to_start_knn_idx = knn.kneighbors(unmatched_end_coords, n_neighbors=1)
    end_to_start_knn_idx = np.ravel(end_to_start_knn_idx)

    # the union of both start->end and unmatched_end->start edges is what we want
    from_coord = np.vstack((start_coords[end_to_start_knn_idx], start_coords))
    to_coord = np.vstack((unmatched_end_coords, end_coords[start_to_end_knn_idx]))

    assert from_coord.shape == to_coord.shape, "from_coord.shape == to_coord.shape"

    return from_coord, to_coord


def knn2(start_mat, end_mat):
    # get matrix of coordinates of non-zero elements of images
    start_coords, end_coords = coordinates(start_mat, end_mat)

    # get a mapping between start coordinates and their closest end coordinates
    knn1 = NearestNeighbors(n_neighbors=1).fit(end_coords)
    _, start_to_end_knn_idx = knn1.kneighbors(start_coords, n_neighbors=1)
    start_to_end_knn_idx = np.ravel(start_to_end_knn_idx)

    knn2 = NearestNeighbors(n_neighbors=1).fit(start_coords)
    _, end_to_start_knn_idx = knn2.kneighbors(end_coords, n_neighbors=1)
    end_to_start_knn_idx = np.ravel(end_to_start_knn_idx)

    # the union of both start->end and unmatched_end->start edges is what we want
    from_coord = np.vstack((start_coords[end_to_start_knn_idx], start_coords))
    to_coord = np.vstack((end_coords, end_coords[start_to_end_knn_idx]))

    assert from_coord.shape == to_coord.shape, "from_coord.shape == to_coord.shape"

    return from_coord, to_coord


def scan_mapping(start_mat, end_mat):
    start_coords, end_coords = coordinates(start_mat, end_mat)
    if len(start_coords) >= len(end_coords):
        from_coord = np.array(start_coords)
        to_coord = np.array(list(itertools.islice(itertools.cycle(end_coords), len(start_coords))))
    else:
        to_coord = np.array(end_coords)
        from_coord = np.array(list(itertools.islice(itertools.cycle(start_coords), len(end_coords))))

    assert from_coord.shape == to_coord.shape, "from_coord.shape == to_coord.shape"

    return from_coord, to_coord


def random_mapping(start_mat, end_mat):
    from_coord, to_coord = scan_mapping(start_mat, end_mat)
    return from_coord, np.random.permutation(to_coord)


coordinate_mapping_maker_for = {
    'knn1': knn_coordinates_mapping,
    'knn2': knn2,
    'scan': scan_mapping,
    'random': random_mapping,
}


def get_coordinate_mapping_maker(coordinate_mapping_maker=None):
    if coordinate_mapping_maker is None:
        return knn_coordinates_mapping
    elif callable(coordinate_mapping_maker):
        return coordinate_mapping_maker
    elif isinstance(coordinate_mapping_maker, str):
        if coordinate_mapping_maker in coordinate_mapping_maker_for:
            return coordinate_mapping_maker_for[coordinate_mapping_maker]
        else:
            raise ValueError(f"Didn't find the coordinate_mapping_maker for: {coordinate_mapping_maker}")


def intify(x):
    """
    Return a rounded int or rounded int array corresponding to x.
    :param x:
    :return:
    """
    if isinstance(x, np.ndarray):
        return np.round(x).astype(int)
    else:
        return int(round(x))


def boolean_matrix_of_image(image_mat, cutoff=0.5):
    """
    Make a bool matrix from the input image_mat
    :param image_mat: a 2d or 3d matrix of ints or floats
    :param cutoff: The threshold to use to make the image pure black and white. Is applied to the max-normalized matrix.
    :return:
    """
    if not isinstance(image_mat, np.ndarray):
        image_mat = np.array(image_mat)
    if image_mat.ndim == 3:
        image_mat = image_mat.sum(axis=2)
    elif image_mat.ndim > 3 or image_mat.ndim == 1:
        raise ValueError("The image_mat needs to have 2 or 3 dimensions")

    if image_mat.dtype != np.dtype('bool'):
        image_mat = image_mat.astype('float')
        image_mat = image_mat / image_mat.max()
        image_mat = image_mat > cutoff
    return image_mat


def separate_stationary_coordinates(from_coord, to_coord):
    # separate stationary coordinates (i.e. matched to the same coordinate)
    stationary_coords_lidx = np.all(from_coord == to_coord, axis=1)
    stationary_coords = from_coord[stationary_coords_lidx]
    from_coord = from_coord[~stationary_coords_lidx]
    to_coord = to_coord[~stationary_coords_lidx]
    return stationary_coords, from_coord, to_coord


def generate_coord_path(stationary_coords, from_coord, to_coord, n_steps=5, shape=None):
    if shape is None:
        shape = (np.vstack((stationary_coords, from_coord, to_coord)).max(axis=0) + 1).shape

    for coords in np.linspace(from_coord, to_coord, n_steps):
        int_coords = intify(coords)  # intify
        int_coords = np.vstack((stationary_coords, int_coords))  # append to stationary
        mask = np.zeros(shape)
        mask[tuple(zip(*int_coords))] = 1
        yield mask


def generate_image_path(start_im, end_im, n_steps=5, coordinate_mapping_maker=knn_coordinates_mapping):
    """
    Generate intermediate images between two given images.

    :param start_im: Start image (PIL.Image.Image, numpy array, or filepath)
    :param end_im: End image (PIL.Image.Image, numpy array, or filepath)
    :param n_steps: Number of steps between images (including start and end)
    :param coordinate_mapping_maker: function that takes two images as an input and produces a (from_coord, to_coord)
        pair that specifies how the pixels of each image are that are mapped to each other.
    :return:
    """
    coordinate_mapping_maker = get_coordinate_mapping_maker(coordinate_mapping_maker)
    start_im = get_image(start_im)
    end_im = get_image(end_im)

    # handle shape
    shape = start_im.size
    if end_im.size != shape:
        end_im = end_im.resize(shape)
    assert shape == end_im.size, "The start_im and end_im sizes must be the same"

    # transform image mats to boolean (i.e. B/W) mats
    start_im = boolean_matrix_of_image(start_im)
    end_im = boolean_matrix_of_image(end_im)
    # find the coordinates of non-zero entries, and map the start to end coordinates
    from_coord, to_coord = coordinate_mapping_maker(start_im, end_im)
    # separate stationary coordinates from those that need to move
    stationary_coords, from_coord, to_coord = \
        separate_stationary_coordinates(from_coord, to_coord)

    shape = (shape[1], shape[0])
    yield from generate_coord_path(stationary_coords, from_coord, to_coord,
                                   n_steps=n_steps, shape=shape)


def image_of_text(text, pixel_height=600, saveas=None, font=courrier_ttf, font_size=100):
    """
    Get an image of a string.

    :param text: A string you want to get an image of.
    :param pixel_height: Something about size, but not really pixel height
    :param saveas: If you want to save the image, this should be the filepath to save to
    :param font: a filename (or it's bytes) of the font definition
    :param font_size: As it says.
    :return:
    """
    if isinstance(font, bytes):
        font = BytesIO(font)
    correction_factor = int(font_size / 12)  # got 1.2 by trial and error with courrier
    font = ImageFont.truetype(font, font_size)
    img = Image.new('1', (0, 0))
    d = ImageDraw.Draw(img)
    text_width, text_height = d.textsize(text + '.')
    text_length = len(text)

    # and here, some trial and error correction of the size...
    img = Image.new('1', (int(correction_factor * (text_width + text_length * 1.3)),
                          int(correction_factor * text_height)))
    d = ImageDraw.Draw(img)
    d.text((0, 0), text, fill=255, font=font)

    img = crop_bw_image(img, pad=0)
    img = resize_image_to_be_able_to_fit_shape(img, (pixel_height, 1000 * pixel_height))

    if saveas is not None:
        if os.path.isdir(saveas):
            folder = saveas
            saveas = os.path.join(folder, text + '.png')
        elif saveas.startswith('.'):
            saveas = text + '.png'
        img.save(saveas)

    return img


def crop_binary_matrix(m, pad=0):
    t = m.any(axis=0)
    min_y = max(0, np.where(t)[0][0] - pad)
    max_y = min(len(t), np.where(t)[0][-1] + pad)

    t = m.any(axis=1)
    min_x = max(0, np.where(t)[0][0] - pad)
    max_x = min(len(t), np.where(t)[0][-1] + pad)
    return m[min_x:max_x, min_y:max_y]


def image_from_matrix(m):
    return Image.fromarray((m.astype(float) * 255).astype(np.uint8))


def crop_bw_image(im, pad=0):
    """Crop image to only contain foreground stuff."""
    im = get_image(im)
    return image_from_matrix(crop_binary_matrix(np.asarray(im), pad=pad))


def resize_image_to_be_able_to_fit_shape(im, shape):
    im = get_image(im)
    if isinstance(shape, (int, float)):
        shape = (shape, shape)

    factor = min(np.array(shape) / np.array(im.size))
    new_size = tuple(intify(factor * np.array(im.size)))
    return im.resize(new_size)


def concatenate_images(images, axis=0, common_shape=None):
    """
    Concatenate images on a given access (and resizing them to do so).
    :param images: List of images (PIL.Image.Image, numpy array, or filepath)
    :param axis: Axis to concatenate on.
    :param common_shape:
    :return:
    """
    images = list(map(get_image, images))
    # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
    if common_shape is None:
        common_shape = sorted([(np.sum(i.size), i.size) for i in images])[0][1]
    # imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
    # for a vertical stacking it is simple: use vstack
    imgs_comb = None
    if axis == 0:
        imgs_comb = np.vstack(tuple(np.asarray(i.resize(common_shape)) for i in images))
    elif axis == 1:
        imgs_comb = np.hstack(tuple(np.asarray(i.resize(common_shape)) for i in images))
    else:
        raise ValueError("axis must be 0 or 1")

    imgs_comb = Image.fromarray(imgs_comb)
    return imgs_comb


def permute(x):
    c = list()
    for i in np.random.permutation(len(x)):
        c.append(x[i])
    return c


def make_start_and_end_images_with_words(start_words, end_words, perm: bool = False, repeat=1, size=150):
    """
    Make two images from two sets of words.
    :param start_words: Words to use for the first image.
    :param end_words: Words to use for the second image
    :param perm: Whether the words should be permuted or not
    :param repeat: How many times the words should be repeated
    :param size: The size of the image (a number or tuple)
    :return: An image
    """
    start_images = list()
    for word in start_words:
        start_images.append(image_of_text(word))

    end_images = list()
    for word in end_words:
        end_images.append(image_of_text(word))

    start_images = start_images * repeat
    end_images = end_images * repeat

    if perm:
        start_images = permute(start_images)
        end_images = permute(end_images)

    start_im = concatenate_images(start_images)
    end_im = concatenate_images(end_images)
    end_im = resize_image_to_be_able_to_fit_shape(end_im, size)
    end_im = end_im.resize(start_im.size)

    return start_im, end_im


def start_and_end_image(start_im, end_im, pad_factor=1):
    """
    Concatenate start and end image.
    :param start_im: Start image (PIL.Image.Image, numpy array, or filepath)
    :param end_im: End image (PIL.Image.Image, numpy array, or filepath)
    :param pad_factor:
    :return:
    """
    start_im = get_image(start_im)
    end_im = get_image(end_im)

    size = start_im.size
    pad_im = image_from_matrix(intify(np.zeros((int(size[1] * pad_factor), int(size[1] * 1)))))
    try:
        return concatenate_images([start_im, pad_im, end_im], axis=1)
    except:
        end_im = end_im.resize(size)
        start_im = image_from_matrix(boolean_matrix_of_image(start_im))
        end_im = image_from_matrix(boolean_matrix_of_image(end_im))
        return concatenate_images([start_im, pad_im, end_im], axis=1)


from tempfile import gettempdir
import imageio


def _name_from_two_strings(str1, str2):
    name1 = os.path.splitext(os.path.basename(str1))[0]
    name2 = os.path.splitext(os.path.basename(str2))[0]
    return f"{name1} - {name2}"


def mk_deformation_image(start_im, end_im, n_steps=7, save_to_file=None,
                         kind=None, coordinate_mapping_maker=knn_coordinates_mapping):
    """Make an image that deforms one image to another, gradually.

    :param start_im: Image or word
    :param end_im: Image or word
    :param n_steps: Number of steps from start to end image
    :param save_to_file: path to file to save too (if not given, will just return the image object)
    :param kind: 'gif', 'horizontal_stack', or 'vertical_stack'
    :param coordinate_mapping_maker: A function that will return the mapping between start and end.
        This function should return a pair (from_coord, to_coord) of aligned matrices whose
        2 columns are the the (x, y) coordinates, and the rows represent aligned positions that
        should be mapped.
    :return:
    """
    coordinate_mapping_maker = get_coordinate_mapping_maker(coordinate_mapping_maker)
    if kind is None:
        if save_to_file is not None:
            _, ext = os.path.splitext(save_to_file)
            if ext == '.gif':
                kind = 'gif'
            else:
                kind = 'horizontal_stack'
        else:
            kind = 'horizontal_stack'
    if kind in {'horizontal_stack', 'stacked', 'horizontal', 'h'}:
        return mk_stacked_deformation_image(start_im, end_im, n_steps=n_steps, save_to_file=save_to_file,
                                            coordinate_mapping_maker=coordinate_mapping_maker, axis=1)
    elif kind in {'vertical_stack', 'vertical', 'v'}:
        return mk_stacked_deformation_image(start_im, end_im, n_steps=n_steps, save_to_file=save_to_file,
                                            coordinate_mapping_maker=coordinate_mapping_maker, axis=0)
    elif kind in {'gif', 'animated'}:
        return mk_gif_of_deformations(start_im, end_im, n_steps=n_steps, save_to_file=save_to_file,
                                      coordinate_mapping_maker=coordinate_mapping_maker)
    else:
        raise ValueError(f"Unrecognized kind: {kind}")


def mk_stacked_deformation_image(start_im, end_im, n_steps=7, save_to_file=None,
                                 coordinate_mapping_maker=knn_coordinates_mapping, axis=1):
    coordinate_mapping_maker = get_coordinate_mapping_maker(coordinate_mapping_maker)
    mm = list()
    for m in generate_image_path(start_im, end_im, n_steps=n_steps, coordinate_mapping_maker=coordinate_mapping_maker):
        mm.append(m)
    if axis == 1:
        mm = np.hstack(mm)
    elif axis == 0:
        mm = np.vstack(mm)
    im = image_from_matrix(mm)

    if save_to_file is None:
        return im
    else:
        im.save(save_to_file)


def mk_gif_of_deformations(start_im, end_im, n_steps=10, save_to_file='deformation.gif',
                           coordinate_mapping_maker=knn_coordinates_mapping):
    """
    Make a gif file exhibiting the deformation from one image to another
    :param start_im: Start image (PIL.Image.Image, numpy array, or filepath)
    :param end_im: End image (PIL.Image.Image, numpy array, or filepath)
    :param n_steps: Number of steps between images (including start and end)
    :param save_to_file: File to save the gif to.
    :return:
    """
    coordinate_mapping_maker = get_coordinate_mapping_maker(coordinate_mapping_maker)
    if save_to_file is None:
        if isinstance(start_im, str) and isinstance(end_im, str):
            save_to_file = _name_from_two_strings(start_im, end_im) + '.gif'
        else:
            save_to_file = 'deformation.gif'
    start_im = get_image(start_im)
    end_im = get_image(end_im)

    tmp_dir = gettempdir()
    it = generate_image_path(start_im, end_im, n_steps=n_steps, coordinate_mapping_maker=coordinate_mapping_maker)
    filenames = list()
    for i, iim in enumerate(it):
        png_file = os.path.join(tmp_dir, f"im_{i:02.0f}.png")
        image_from_matrix(iim).save(png_file)
        filenames.append(png_file)

    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    for filename in filenames[::-1]:
        images.append(imageio.imread(filename))

    imageio.mimsave(save_to_file, images)

    for f in filenames:
        os.remove(f)


def mk_gif_deformations_from_strings(str1, str2, n_steps=20, save_to_file=None):
    """
    Make a gif that deforms one string to another and back.
    :param str1: One of the string to transform to the other
    :param str2: The other string
    :param n_steps: Total number of frames in the gif
    :param save_to_file: Name of the gif file to save as (will default to a concatenation of the strings)
    :return:
    """
    if save_to_file is None:
        save_to_file = _name_from_two_strings(str1, str2) + '.gif'
    im1 = image_of_text(str1)
    im2 = image_of_text(str2)
    mk_gif_of_deformations(im1, im2, n_steps=n_steps, save_to_file=save_to_file)


def overlay(background_im, overlay_im, alpha=0.5):
    """Overlay an image on a background image"""
    return Image.blend(background_im.convert('RGBA'), overlay_im.convert('RGBA'), alpha=alpha)


def display_gif(gif_file):
    """Display gif in ipython notebook"""
    from IPython import display
    # Note: the random part is so that an image will be refreshed when the file content changes
    return display.HTML('<img src="{}?{}">'.format(gif_file, np.random.randint(0, int(1e8))))


if __name__ == '__main__':
    import argh

    argh.dispatch_command(mk_deformation_image)
    # parser = argh.ArghParser()
    # parser.add_commands([mk_gif_of_deformations, mk_gif_deformations_from_strings])
    # parser.dispatch()
