# import module
from pdf2image import convert_from_path

def get_img(pdf_path):
      images = convert_from_path(pdf_path)
      print(type(images))
      for i in range(len(images)):
        
            # Save pages as images in the pdf
          images[i].save('page'+ str(i) +'.jpg', 'JPEG')


get_img('Harish_Resume_PhD.pdf')