import schedule
import time
import json
from get_latest_linkedin_post import get_latest_linked_post


def job():
    output = get_latest_linked_post("https://www.linkedin.com/company/accenture/")
    with open("/tmp/out.txt", "w") as f:
        f.writelines(json.dumps(output))


schedule.every(5).minutes.do(job)
job()
while True:
    schedule.run_pending()
    time.sleep(5)
