import schedule
import time, os


def fetchLatestCompanyPost():
    # Replace this function with your actual implementation
    print("DID A")
    time.sleep(5)
    print("DID A")
    time.sleep(5)
    print("DID A")
    time.sleep(5)


def loading_animation():
    animations = ["-", "\\", "|", "/"]
    idx = 0

    try:
        # Run the loading animation until the scheduled task is executed
        while True:
            print("Waiting for next execution " + animations[idx], end="\r")
            idx = (idx + 1) % len(animations)
            time.sleep(0.1)
    except KeyboardInterrupt:
        # Handle keyboard interrupt (e.g., when the user presses Ctrl+C)
        print("\nScript terminated.")


# Schedule the task
schedule.every(10).seconds.do(fetchLatestCompanyPost)
while True:
    schedule.run_pending()
    print(".", end="\r")
    time.sleep(1)
    print("..", end="\r")
    time.sleep(1)
    print("...", end="\r")
    time.sleep(1)
    os.system("cls" if os.name == "nt" else "clear")
