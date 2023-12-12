import schedule
import time
import json
from get_latest_linkedin_post import get_latest_linked_post


def job():
    output = get_latest_linked_post()
    with open("/tmp/out.txt", "w") as f:
        f.writelines(json.dumps(output))


schedule.every(10).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(10 * 60)
