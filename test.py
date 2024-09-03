from openai import OpenAI
import json
import base64
import requests
import os
# OpenAI API Key
api_key = "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"

# Function to encode the image
def encode_image(image_path):
	with open(image_path, "rb") as image_file:
		return base64.b64encode(image_file.read()).decode('utf-8')


client = OpenAI(api_key=api_key)

# Path to your image
image_path = "Resume_0.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)



response = client.chat.completions.create(
		model="gpt-4o-mini",
		response_format={ "type": "json_object" },
		messages=[
			{
			"role": "system",
			"content": [
									{
									"type": "text",
									"text": "you are a resume parser. Given the image of the resume, parse every section and provide the output in a json format."
									}
								]
			},
			{
				"role": "user",
				"content": [
				{
						"type": "text",
						"text": "can you parse all sections of this resume?"
					},
					{
						"type": "image_url",
						"image_url": {
							"url": f"data:image/jpeg;base64,{base64_image}"
						}
					}  
				],
			}
		],
		max_tokens=1500
)

output = json.loads(response.choices[0].message.content)
print(type(output))
print(output)
print(output['name'])

