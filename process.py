'''
This is the code for processing different operation of ResumeAssistant 
'''

from pdf2image import convert_from_path
# ImageWorker takes in the path to jpg resume image and returns the contents of the resume in a json format. 
from resumeassistant.operator.worker import ImageWorker, TextWorker
from resumeassistant.data.candidate_record import Record, QA_Knowledge
from openai import OpenAI
import json



def get_img(pdf_path, img_path):
      # Method for converting pdf resumes to jpg images. 
      images = convert_from_path(pdf_path)
      for i in range(len(images)):
            # Save pages as images in the pdf
            images[i].save(img_path + str(i) +'.jpg', 'JPEG')



with open('gpt_key.json', 'r') as file:
      data = json.load(file)
      api_key = data["api_key"]

#GPT-client
client = OpenAI(api_key=api_key)

#Converting pdf resume to image
get_img('Resume_PhD.pdf', './Harish_Resume')


#Resume Parsing
sys_prompt = "You are a resume parser. Given the image of the resume, parse every section and provide the output in a JSON format."
user_prompt="Can you parse all sections of this resume?"
image_worker = ImageWorker(client=client, model_id="gpt-4o-mini", sys_prompt=sys_prompt, user_prompt=user_prompt)
parsed_resume = image_worker.get_output('Harish_Resume0.jpg')
print(f'parsed_resume: \n{parsed_resume}', flush=True)

#Old cover-letter
old_cl = "Hello Hiring Team, \nI am pursuing my Ph.D. in the Computer Engineering department at Stevens Institute of Technology; my research is focused on Natural Language Processing. I work on applications related to the areas of Misinformation Research and Investigative Journalism using Evidence Extraction, Fact Verification and Key-Phrase analysis; I research and work with Generative Models, Deep Learning models, Attention Networks, and Large Language Models for Extraction and Verification Tasks. My Dissertation Project is based on Fact-Verification and Evidence-Extraction using an Explainable Prompt-Engineering Model I proposed. \nEven though I chose the use cases of NLP as the focus of my research, my work is more comprehensive than NLP-based models;  I have also created a low-cost Derivative-Free Optimization Method for parameter optimization in ML; I am working on obtaining a Provisional Patent for this research. I am immensely passionate about learning and analyzing the underlying Mathematical Concepts of Machine Learning Models; I like educating myself on all the specifics of any problem statement, following the motivation of the research, chronological evolution of the Problem-Solution framework, and feature analysis from historical to the SOTA models. \nI am currently seeking a job opportunity to hone my skills and work with a proficient team for an inspirational cause where AI can be efficacious. \nRegards, \nHarish Sista, Ph.D. candidate, \nComputer Engineering Department, \nStevens Institute of Technology."

#Initialize Candidate Record
record = Record(client=client, resume=parsed_resume, cl=old_cl)


#Job description
with open('job_description2.txt', 'r') as f:
    job_description2 = f.read()
new_cl = record.generate_cl(job_description=job_description2)
print(f'New Cover Letter: \n{new_cl}', flush=True)

#Resume Screening
key_questions = record.screen_resume_CL(job_description=job_description2)
print(f'Screening Question on missing candidate information: \n{key_questions}', flush=True)


#Clreate Additional Knowledge record
add_knowledge = QA_Knowledge(0, key_questions)

key_q2 = {'keywords': 
          [{'keyword': 'data preprocessing and feature engineering', 
            'question': 'Can you explain how your resume reflects proficiency in data preprocessing and feature engineering techniques?, particularly scikit-learn?'}, 
            {'keyword': 'collaborate with cross-functional teams to integrate AI solutions', 
            'question': "Can you provide examples from your resume that demonstrate your experience collaborating with cross-functional teams to integrate AI solutions?"},
            {'keyword': '5+ years of experience in working with AI/LLMs', 
            'question': "How does the resume demonstrate at least 5 years of experience specifically working with AI and large language models (LLMs) in a direct capacity?"} 
           ]} 
add_knowledge.add_key_questions(2, key_q2) # This is the code to add human generated knowledge to QA_Knowledge instance


#Record answers into QA_Knowledge instance
key_knowledge = {'5+ years of experience in working with AI/LLMs': 
                 {'question': 'How does the resume demonstrate at least 5 years of experience specifically working with AI and large language models (LLMs) in a direct capacity?',
                    'answer': 'As a part of my six years of PhD research in NLP, I have worked on various projects based on knowledge extraction from scholarly data and evidence extraction and fact verification of social-media data using web-scraped real-world data. I used LLMs for building all these projects.'
                 }, 
                 'data preprocessing and feature engineering':{ 
                'question': 'Can you explain how your resume reflects proficiency in data preprocessing and feature engineering techniques?',
                 'answer': 'In my PhD program, I have worked on different varieties of datasets like medical data(CORD-19, PubMed), social media data(CoVerifi), scholarly data(FEVER-dataset), and real-world data(AVeriTec). All these datasets use different feature spaces. To process these datasets I have used various feature engineering techniques like Prompt Engineering, Entity Extraction, key-word extraction, parts-of-speech tagging and text denoising using Python\'s RegEx library.'}, 
                 'Experience with big data tools and technologies (e.g., Hadoop, Spark)': { 
                  'question': 'How does the resume and cover letter demonstrate experience with big data tools and technologies such as Hadoop or Spark?',
                 'answer': None}, 
                 'strong understanding of machine learning algorithms and techniques':{
                  'question': 'How does your resume showcase a strong understanding of various machine learning algorithms and their techniques?',
                 'answer': None}, 
                 'collaborate with cross-functional teams to integrate AI solutions': { 
                  'question': 'Can you provide examples from your resume that demonstrate your experience collaborating with cross-functional teams to integrate AI solutions?',
                 'answer': 'In my previous job at \'Fresh Digital Group,\' I have collaborated with various teams like content writers and UI designers to brainstorm on building structure for chat applications and designing UI for mobile applications.'}}
add_knowledge.add_knowledge(key_knowledge)
print(f'Additional Knowledge to be saved: \n{add_knowledge.get_knowledge()}', flush=True)


#Record QA_Knowledge instance to candidate record
record.add_knowledge.update(add_knowledge.get_knowledge())


#Candidate Record in JSON format
print(f'Candidate Record in JSON format: \n{record.get_record()}', flush=True)


#Generate new cover letter based on job_description2
with open('job_description2.txt', 'r') as f:
    job_description2 = f.read()
new_cl = record.generate_cl(job_description=job_description2)
print(f'New Cover Letter after adding add_knowledge: \n{new_cl}', flush=True)


