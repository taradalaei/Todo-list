import time
import schedule

from app.commands.autoclose_overdue import run


def job():
    count = run()
    print(f"[scheduler] closed {count} overdue tasks")


def main():
    print("Scheduler started...")

    # هر ۱۵ دقیقه یک‌بار
    schedule.every(15).minutes.do(job)

    # اگر مثلاً فقط روزی یک‌بار ساعت ۲ شب بخواهی:
    # schedule.every().day.at("02:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
