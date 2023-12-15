import openai
import json
from tools import read_from_file

openai.api_key = json.loads(read_from_file("dbconfig.json")).get("openai_key", "")


def updateContext(ctx, whoSaid, what):
    c = {"role": whoSaid, "content": what}
    return ctx.append(c)


def generateReportFromPosts(postData, newBasePrompt=None):
    basePrompt = """
    You are a sales assistant for Webknot. You will be provided with scrapped data 
    of LinkedIn posts of a different comapny. You need to analyse the posts data 
    and generate a report outlining the areas of knowledge that they stress, need, 
    and might not have.
    """
    CONTEXT = []
    if newBasePrompt:
        basePrompt = newBasePrompt
    updateContext(CONTEXT, "system", basePrompt)
    for post in postData:
        updateContext(CONTEXT, "user", post)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=CONTEXT)
    return response.choices[0].message.content
