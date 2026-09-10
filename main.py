import random
import time
import urllib.error
import urllib.request

BASE_URL = "http://localhost:9080"
BACKEND_CHOICES = ("backendA", "backendB", "backendC")


def prompt_backend() -> str:
    choices = ", ".join(BACKEND_CHOICES)
    while True:
        value = input(f"Select an endpoint ({choices}): ").strip()
        if value in BACKEND_CHOICES:
            return value
        print(f"Invalid choice. Must be one of: {choices}")


def prompt_failure_rate() -> int:
    while True:
        value = input("Enter failure rate percentage (0-100) [default: 10]: ").strip()
        if not value:
            return 10
        try:
            rate = int(value)
        except ValueError:
            print("Invalid input. Must be an integer between 0 and 100.")
            continue
        if 0 <= rate <= 100:
            return rate
        print("Invalid input. Must be between 0 and 100.")


def prompt_delay() -> int:
    while True:
        value = input("Enter delay in seconds (0-60) [default: 15]: ").strip()
        if not value:
            return 15
        try:
            delay = int(value)
        except ValueError:
            print("Invalid input. Must be an integer between 0 and 60.")
            continue
        if 0 <= delay <= 60:
            return delay
        print("Invalid input. Must be between 0 and 60.")


def hit_endpoint(url: str) -> None:
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            print(f"GET {url} -> {response.status}")
    except urllib.error.HTTPError as e:
        print(f"GET {url} -> {e.code}")
    except urllib.error.URLError as e:
        print(f"GET {url} -> request failed: {e.reason}")


def main() -> None:
    backend = prompt_backend()
    failure_rate = prompt_failure_rate()
    delay = prompt_delay()

    failure_url = f"{BASE_URL}/{backend}/failure"
    success_url = f"{BASE_URL}/{backend}/success"

    print(f"\nTargeting '{backend}' with {failure_rate}% failure rate, {delay}s delay between requests.")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            if random.uniform(0, 100) < failure_rate:
                hit_endpoint(failure_url)
            else:
                hit_endpoint(success_url)
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
