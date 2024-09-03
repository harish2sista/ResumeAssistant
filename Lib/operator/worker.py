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
	def __get_messages(self):
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
							}
						]
				}
				]
	def get_output(self, image_path):
		base64_image = encode_image(image_path)
		response = self.client.chat.completions.create(
		model="gpt-4o-mini",
		response_format={ "type": "json_object" },
		messages=self.__get_messages(),
		max_tokens=1500
		)
		return json.loads(response.choices[0].message.content)

class TextWorker:
	def __init__(self, client, model_id, sys_prompt=None, user_prompt=None):
		self.client = client
		self.model_id = model_id
		self.sys_prompt = sys_prompt
		self.user_prompt = user_prompt


