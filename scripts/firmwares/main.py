import requests
import threading

base_url = "https://cdn.cloud-universe.anycubic.com/ota/K2Max/AC104_K2Max_{}.{}.{}_{}.{}.{}_update.zip"

# Define the maximum number of simultaneous threads
max_threads = 100

# Semaphore to limit the number of simultaneous threads
semaphore = threading.Semaphore(max_threads)

# File to store successful URLs
success_file = "successful_urls.txt"

# Do requests with a delay between them
def check_version(major1, minor1, patch1, major2, minor2, patch2):
    url = base_url.format(major1, minor1, patch1, major2, minor2, patch2)
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
for major1 in range(0, 10):  # Change the range for the first major version
    for minor1 in range(0, 10):  # Change the range for the first minor version
        for patch1 in range(0, 10):
            for major2 in range(0, 10):  # Change the range for the second major version
                for minor2 in range(0, 10):  # Change the range for the second minor version
                    for patch2 in range(0, 10):
                        t = threading.Thread(target=check_version, args=(major1, minor1, patch1, major2, minor2, patch2))
                        threads.append(t)
                        t.start()
                        # Add a small delay between starting threads

# Wait for all threads to finish
for t in threads:
    t.join()

print(f"Successful URLs written to {success_file}")
