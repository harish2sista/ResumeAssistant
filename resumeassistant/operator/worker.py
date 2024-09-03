import re
import json
import base64
import requests
from openai import OpenAI

__all__ = ['ImageWorker', 'TextWorker']

class ImageWorker:
	def __init__(self, client, model_id, sys_prompt=None, user_prompt=None):
		self.client = client
		self.model_id = model_id
		self.sys_prompt = sys_prompt
		self.user_prompt = user_prompt
	def __get_messages(self, base64_image):
		return [
				{
				"role": "system",
				"content": [
							{
							"type": "text",
							"text": self.sys_prompt
							}
						]
				},
				{
				"role": "user",
				"content": [
							{
							"type": "text",
							"text": self.user_prompt
							},
							{
							"type": "image_url",
							"text": {
									"url": f"data:image/jpeg;base64,{base64_image}"
								}
							}
						]
				}
				]

	def encode_image(self, image_path):
		with open(image_path, "rb") as image_file:
			return base64.b64encode(image_file.read()).decode('utf-8')

	def get_output(self, image_path):
		base64_image = self.encode_image(image_path)
		response = self.client.chat.completions.create(
		model=self.model_id,
		response_format={ "type": "json_object" },
		messages=self.__get_messages(base64_image),
		max_tokens=1500
		)
		return json.loads(response.choices[0].message.content)

class TextWorker:
	def __init__(self, client, model_id, sys_prompt=None, user_prompt=None):
		self.client = client
		self.model_id = model_id
		self.sys_prompt = sys_prompt
		self.user_prompt = user_prompt


