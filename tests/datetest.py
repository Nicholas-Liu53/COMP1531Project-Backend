from datetime import timezone, datetime

if __name__ == "__main__":
    now = datetime.now()
    timestamp = now.replace(tzinfo=timezone.utc).timestamp()
    print(timestamp)