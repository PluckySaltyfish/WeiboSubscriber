from apscheduler.schedulers.blocking import BlockingScheduler
import get_weibo
import config

def BigBrotherIsWatchingYou():
    scheduler = BlockingScheduler()
    scheduler.add_job(get_weibo.send,'cron', hour=config.send_hour, minute=config.send_min)

    try:
        scheduler.start()
    except(KeyboardInterrupt,SystemExit):
        print('aps quit')


if __name__ == '__main__':
    BigBrotherIsWatchingYou()