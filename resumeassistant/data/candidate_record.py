import re 
import json
from resumeassistant.operator.worker import ImageWorker, TextWorker

__all__ = ['Record', 'QA_Knowledge']


class Record:
    def __init__(self, client=None, resume=None, cl=None, add_skills=None, add_work_experience=None, add_education=None, add_projects=None, add_achievements=None, add_certifications=None):
        self.client = client
        self.resume = resume
        self.cl = cl
        self.add_skills = add_skills
        self.add_work_experience = add_work_experience
        self.add_education = add_education
        self.add_projects = add_projects
        self.add_achievements = add_achievements
        self.add_certifications = add_certifications
        self.add_knowledge = {}
        self.__resume_workbench = None
        self.__record = {}

#------------------------data manipulation methods------------------------
    def update_resume(self, key, val):
        self.resume[key] = val

    def all_skills(self):
        total_skills = []
        for key in self.resume.keys():
            if 'skill' in key.lower():
                total_skills.append(self.resume[key])
        if self.add_skills:
            total_skills.append(self.add_skills)
        return total_skills

    def all_work_experience(self):
        total_work_exp = []
        for key in self.resume.keys():
            if 'work' in key.lower():
                total_work_exp.append(self.resume[key])
        if self.add_work_experience:
            total_work_exp.append(self.add_work_experience)
        return total_work_exp

    def all_education(self):
        total_education = []
        for key in self.resume.keys():
            if 'education' in key.lower():
                total_education.append(self.resume[key])
        if self.add_education:
            total_education.append(self.add_education)
        return total_education

    def all_projects(self):
        total_projects = []
        for key in self.resume.keys():
            if 'project' in key.lower():
                total_projects.append(self.resume[key])
        if self.add_projects:
            total_projects.append(self.add_projects)
        return total_projects 
    
    def all_achievements(self):
        total_achievements = []
        for key in self.resume.keys():
            if 'achievement' in key.lower():
                total_achievements.append(self.resume[key])
        if self.add_achievements:
            total_achievements.append(self.add_achievements)
        return total_achievements  

    def all_certifications(self):
        total_certifications = []
        for key in self.resume.keys():
            if 'certific' in key.lower():
                total_certifications.append(self.resume[key])
        if self.add_certifications:
            total_certifications.append(self.add_certifications)
        return total_certifications

#------------------------process methods------------------------
    def save(self, path):
        self.update_record()
        with open(path, 'w') as f:
            json.dump(self.__record, f)

    def load(self, path):
        with open(path, 'r') as f:
            data = json.loads(f)
        self.__record = data
        self.resume = data["resume"]
        self.cl = data["cl"]
        self.add_skills = data["additional skills"]
        self.add_work_experience = data["additional work experience"]
        self.add_education = data["additional education"]
        self.add_projects = data["additional projects"]
        self.add_achievements = data["additional achievements"]
        self.add_certifications = data["additional certifications"]
        self.add_knowledge = data["additional knowledge"]

    def push_resume(self):
        self.resume = self.__resume_workbench

    def commit_resume(self, new_resume):
        self.__resume_workbench = new_resume

    def add_knowledge(self, add_knowledge):
        if type(add_knowledge) == list:
            self.add_knowledge.update({"keywords": add_knowledge})
        else:
            try:
                self.add_knowledge.update(add_knowledge)
            except:
                raise Exception(f"Expected Dic, obtained {type(add_knowledge)}")

    def update_record(self):
        if self.__record == {}:
            self.__record = {"resume": self.resume,
                            "cl": self.cl, 
                            "additional skills": self.add_skills, 
                            "additional work experience": self.add_work_experience, 
                            "additional education": self.add_education, 
                            "additional projects": self.add_projects, 
                            "additional achievements": self.add_achievements, 
                            "additional certifications": self.add_certifications, 
                            "additional knowledge": self.add_knowledge}
        else:
            if self.__record["resume"] != self.resume: 
                self.__record["resume"] = self.resume
            if self.__record["cl"] != self.cl:
                self.__record["cl"] = self.cl 
            if self.__record["additional skills"] != self.add_skills:
                self.__record["additional skills"] = self.add_skills
            if self.__record["additional work experience"] != self.add_work_experience:
                self.__record["additional work experience"] = self.add_work_experience
            if self.__record["additional education"] != self.add_education:
                self.__record["additional education"] = self.add_education
            if self.__record["additional projects"] != self.add_projects:
                self.__record["additional projects"] = self.add_projects
            if self.__record["additional achievements"] != self.add_achievements:
                self.__record["additional achievements"] = self.add_achievements
            if self.__record["additional certifications"] != self.add_certifications:
                self.__record["additional certifications"] = self.add_certifications
            if self.__record["additional knowledge"] != self.add_knowledge:
                self.__record["additional knowledge"] = self.add_knowledge

    def get_record(self, resume=None, cl=None):
        self.update_record()
        return self.__record

#------------------------process methods------------------------

    def screen_resume_CL(self, job_description, candidate_info=None):
        ra_system_prompt = 'You are a resume and cover letter screener. Given the candidate information(#candidate_info) and the job description(#job_description), provide keywords from the job description where the resume and the cover letter fail to address the requirements. Provide the keywords with a question describing how the resume and the cover letter fail to meet this requirement. Present the output in the following JSON output format: \n\t{\"keywords\": [{"keyword": system keyword, "question": system keyword question}]}'
        
        if candidate_info:
            ra_user_prompt = f'#candidate_info: {candidate_info} \n#job_description: {job_description}'
        else:
            ra_user_prompt = f'#candidate_info: {self.get_record()} \n#job_description: {job_description}'
        ra_text_worker = TextWorker(client=self.client, model_id="gpt-4o-mini", sys_prompt=ra_system_prompt, user_prompt=ra_user_prompt, json_format=True)
        system_insights = ra_text_worker.get_output()
        return system_insights

    def generate_resume(self, job_description, candidate_info=None, sys_prompt=None):
        if sys_prompt:
            ro_system_prompt=sys_prompt
        else:
            ro_system_prompt = 'You are a resume optimizer. Given the candidate information(#candidate_info) and the job description(#job_description), rewrite the current resume to highlight the relevant skills, experience, and quantifiable achievements that match the job description. Provide the output in a JSON format.'
        if candidate_info:
            ro_user_prompt = f'#candidate_info: {candidate_info} \n#job_description: {job_description}'
        else:
            ro_user_prompt = f'#candidate_info: {self.get_record()} \n#job_description: {job_description}'
        
        ro_text_worker = TextWorker(client=self.client, model_id="gpt-4o-mini", sys_prompt=ro_system_prompt, user_prompt=ro_user_prompt, json_format=True)
        new_resume = ro_text_worker.get_output()
        return new_resume

    def generate_cl(self, job_description, candidate_info=None, sys_prompt=None):
        if sys_prompt:
            cl_system_prompt = sys_prompt
        else:
            cl_system_prompt = "You are a cover letter generator, given the candidate information(#candidate_info) and job description(#job_description). Generate a cover letter relevant to the job description highlighting the candidate's skills and achievements"
        if candidate_info:
            cl_user_prompt = f'#candidate_info: {candidate_info} \n#job_description: {job_description}'
        else:
            cl_user_prompt = f'#candidate_info: {self.get_record()} \n#job_description: {job_description}'
        
        cl_text_worker = TextWorker(client=self.client, model_id="gpt-4o-mini", sys_prompt=cl_system_prompt, user_prompt=cl_user_prompt)
        new_cl = cl_text_worker.get_output()
        return new_cl


class QA_Knowledge:
    def __init__(self, qa_id, key_questions):
        self.qa_id = qa_id
        self.key_questions = key_questions
        self.keywords = [entry["keyword"] for entry in self.key_questions["keywords"]]
        self.key_QA = {entry["keyword"]: {
                                        "id": self.qa_id,
                                        "question": entry["question"],
                                        "answer": None
                                        } for entry in self.key_questions["keywords"]} 

    def get_knowledge(self):
        knowledge_dic = {}
        for key in self.key_QA:
            # print(self.key_QA)
            if self.key_QA[key]["answer"]:
                knowledge_dic[key] = {"id": self.key_QA[key]["id"], "answer": self.key_QA[key]["answer"]}
        return knowledge_dic

    def add_key_questions(self,qa_id, key_questions):
        self.key_QA.update({
                            entry["keyword"]: {
                                            "id": qa_id,
                                            "question": entry["question"],
                                            "answer": None
                                            } for entry in key_questions["keywords"]
                                })

    def add_knowledge(self, key_knowledge):
        for key in key_knowledge.keys():
            if key_knowledge[key]['answer']:
                if key in self.key_QA.keys():
                    self.key_QA[key]["answer"] = key_knowledge[key]['answer']






    





