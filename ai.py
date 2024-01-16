import openai
import json, constants
from tools import read_from_file

openai.api_key = json.loads(read_from_file("dbconfig.json")).get("openai_key", "")


class AI:
    def __init__(self):
        self.CONTEXT = []

    def updateContext(self, ctx, whoSaid, what):
        c = {"role": whoSaid, "content": what}
        return ctx.append(c)

    def generateReportFromPosts(
        self, postData, newBasePrompt=None, aboutData="", webPageData=""
    ):
        basePrompt = constants.BASE_PROMPT
        CONTEXT = self.CONTEXT
        if newBasePrompt:
            basePrompt = newBasePrompt
        self.updateContext(CONTEXT, "system", basePrompt)
        for post in postData:
            self.updateContext(CONTEXT, "user", post)
        if aboutData:
            self.updateContext(
                CONTEXT, "user", "use this linkedin about section data as well"
            )
            self.updateContext(CONTEXT, "user", aboutData)
        if webPageData:
            self.updateContext(
                CONTEXT, "user", "use this company's website data as well"
            )
            self.updateContext(CONTEXT, "user", aboutData)
        self.updateContext(
            CONTEXT, "user", "anyalyze everything and generate the report"
        )
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=CONTEXT)
        return response.choices[0].message.content
