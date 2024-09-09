import re 
import json

__all__ = []


class Record:
	def __init__(self, client=None, resume=None, cv=None, add_skills=None, add_work_experience=None, add_education=None, add_projects=None, add_achievements=None, add_certifications=None):
		self.client = client
		self.resume = resume
		self.cv = cv
		self.add_skills = add_skills
		self.add_work_experience = add_work_experience
		self.add_education = add_education
		self.add_projects = add_projects
		self.add_achievements = add_achievements
		self.add_certifications = add_certifications

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

	def save(self, path):
		output = {
				"resuem": self.resume, 
				"cv": self.cv, 
				"add_skills": self.add_skills,
				"add_work_experience": self.add_work_experience,
				"add_education": self.add_education, 
				"add_projects": self.add_projects,
				"add_achievements": self.add_achievements,
				"add_certifications": self.add_certifications
				}
		with open(path, 'w') as f:
			json.dump(output, f)

	def load(self, path):
		with open(path, 'r') as f:
			data = json.loads(f)
		self.resume = data.resume
		self.cv = data.cv
		self.add_skills = data.add_skills
		self.add_work_experience = data.add_work_experience
		self.add_education = data.add_education
		self.add_projects = data.add_projects
		self.add_achievements = data.add_achievements
		self.add_certifications = data.add_certifications


#------------------------LLM prompting methods------------------------
