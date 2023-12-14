import openai
import json
from tools import read_from_file

openai.api_key = json.loads(read_from_file("dbconfig.json")).get("openai_key", "")


def updateContext(ctx, whoSaid, what):
    c = {"role": whoSaid, "content": what}
    return ctx.append(c)


basePrompt = """
You are a sales assistant for Webknot company your job is to go through the posts of a potential clients linkedin posts
and analayze the post data and create a detailed report about what experties they lack, need or focusing on.
"""


def generateReportFromPosts(postData):
    CONTEXT = []
    updateContext(CONTEXT, "system", basePrompt)
    for post in postData:
        updateContext(CONTEXT, "user", post)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=CONTEXT)
    return response.choices[0].message.content
