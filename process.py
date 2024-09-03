'''
This is the code for parsing resumes in pdf format. 
'''

from pdf2image import convert_from_path
# ImageWorker takes in the path to jpg resume image and returns the contents of the resume in a json format. 
from resumeassistant.operator.worker import ImageWorker
from openai import OpenAI

def get_img(pdf_path):
      # Method for converting pdf resumes to jpg images. 
      images = convert_from_path(pdf_path)
      print(type(images))
      for i in range(len(images)):
        
            # Save pages as images in the pdf
          images[i].save('page'+ str(i) +'.jpg', 'JPEG')


# get_img('Harish_Resume_PhD.pdf')

client = OpenAI(api_key="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")


sys_prompt = "you are a resume parser. Given the image of the resume, parse every section and provide the output in a json format."

user_prompt="can you parse all sections of this resume?"

image_worker = ImageWorker(client=client, model_id="gpt-4o-mini", sys_prompt=sys_prompt, user_prompt=user_prompt)
# print(image_worker.get_output('page0.jpg'))
print(image_worker.get_output('Resumes_Datasets/Bing_images/Accountant_resumes/Image_43.jpg'))