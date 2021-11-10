import pdf
from pdf.utils import find_files, confirm_files


def main():
    """Main Function"""
    pattern = '*.jpg'
    base_dir = '.'
    pattern = base_dir + pattern
    file_list = list(find_files(pattern))
    file_list.sort()
    confirmed = confirm_files(file_list)
    options: pdf.to_pdf_options = {
        'author': '',
        'output': base_dir + '000outputFile.pdf',
        'page_size': pdf.PageSize.A4,
        'image_size': pdf.ImageSize.page,
    }
    if confirmed:
        pdf.create_pdf(file_list, options)
    else:
        print('Please re-run script with correct file order')


if __name__ == '__main__':
    main()
