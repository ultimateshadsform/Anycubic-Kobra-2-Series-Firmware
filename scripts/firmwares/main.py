import requests
import threading
import time

base_url = "https://cdn.cloud-universe.anycubic.com/ota/K2Plus/AC104_K2Plus_1.1.0_{}.{}.{}_update.zip"

# Define the maximum number of simultaneous threads
max_threads = 50

# Semaphore to limit the number of simultaneous threads
semaphore = threading.Semaphore(max_threads)

# File to store successful URLs
success_file = "successful_urls.txt"

# Do requests with a delay between them


def check_version(major, minor, patch):
    url = base_url.format(major, minor, patch)
    with semaphore:
        r = requests.head(url)
        if r.status_code == 200:
            success_message = f"Success: {url}"
            print(success_message)
            # Write successful URLs to the file
            with open(success_file, "a") as f:
                f.write(success_message + "\n")
        else:
            print(f"Failed: {url}")


# Create threads
threads = []
for major in range(0, 10):
    for minor in range(0, 10):
        for patch in range(0, 10):
            t = threading.Thread(target=check_version,
                                 args=(major, minor, patch))
            threads.append(t)
            t.start()
            # Add a small delay between starting threads
            time.sleep(0.01)

# Wait for all threads to finish
for t in threads:
    t.join()

print(f"Successful URLs written to {success_file}")
