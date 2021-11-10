from typing import Tuple, List, TypedDict, Union
from enum import Enum
from fpdf import FPDF
from PIL import Image
from .utils import plural


class PageSize(Enum):
    """Page size"""
    image = 'image'
    A4 = 'A4'
    A3 = 'A3'
    A2 = 'A2'
    A1 = 'A1'
    A0 = 'A0'
    letter = 'letter'
    legal = 'legal'


class ImageSize(Enum):
    """Image size"""
    image = 'image'
    page = 'page'
    page_width = 'page_width'
    page_height = 'page_height'


class to_pdf_options(TypedDict, total=False):
    """Options for to_pdf"""
    author: str
    output: str
    page_size: Union[PageSize, Tuple[int, int]]
    image_size: Union[ImageSize, Tuple[int, int]]
    page_orientation: str


def create_pdf(image_list: List[str], options: to_pdf_options) -> None:
    """Convert images to pdf"""
    options = _parse_options(options)
    pdf = FPDF('P', 'mm', 'A4')
    pdf.set_author(options['author'])
    for index, image_name in enumerate(image_list, start=1):
        width, height = _get_page_size(image_name, options)
        pdf.add_page('P', (width, height))
        width, height = _get_image_size(image_name, options)
        pdf.image(image_name, 0, 0, width, height)
        print(f'\rAdded {index} {plural(index, "page")}', end='')

    output_file = options['output']
    print(f'\nCreating output file "{output_file}"')
    pdf.output(output_file, 'F')
    print('Created output file')


def _parse_options(options: to_pdf_options) -> to_pdf_options:
    """Parse options"""
    default_options: to_pdf_options = {
        'author': '',
        'output': '000_outputFile.pdf',
        'page_size': PageSize.image,
        'image_size': ImageSize.image,
        'page_orientation': 'P',
    }
    for key, value in default_options.items():
        if key not in options:
            options[key] = value
    return options


def _get_page_size(image_name: str, options: to_pdf_options) -> Tuple[float, float]:
    if options['page_size'] == PageSize.image:  # image size
        image = Image.open(image_name)
        width, height = image.size
        image.close()
        return _pixels_to_mm(width), _pixels_to_mm(height)
    elif options['page_size'] == PageSize.A4:
        return 210, 297
    elif options['page_size'] == PageSize.A3:
        return 297, 420
    elif options['page_size'] == PageSize.A2:
        return 420, 594
    elif options['page_size'] == PageSize.A1:
        return 594, 841
    elif options['page_size'] == PageSize.A0:
        return 841, 1189
    elif options['page_size'] == PageSize.letter:
        return 216, 279
    elif options['page_size'] == PageSize.legal:
        return 216, 356
    elif isinstance(options['page_size'], tuple) and len(options['page_size']) == 2:
        return options['page_size']
    else:
        raise Exception(f'Unknown page size {options["page_size"]}')


def _get_image_size(image_name: str, options: to_pdf_options) -> Tuple[float, float]:
    page_size = _get_page_size(image_name, options)
    if options['image_size'] == ImageSize.image:
        image = Image.open(image_name)
        width, height = image.size
        image.close()
        return _pixels_to_mm(width), _pixels_to_mm(height)
    elif options['image_size'] == ImageSize.page:
        return page_size
    elif options['image_size'] == ImageSize.page_width:
        return (page_size[0], 0)
    elif options['image_size'] == ImageSize.page_height:
        return (0, page_size[1])
    elif isinstance(options['image_size'], tuple) and len(options['image_size']) == 2:
        return options['image_size']
    else:
        raise Exception(f'Unknown image size {options["image_size"]}')


def _pixels_to_mm(pixels: float) -> float:
    pixels_to_mm_factor = 0.264583
    return pixels * pixels_to_mm_factor
