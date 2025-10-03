import schedule

class BookRequestSchedule:
    def scheduleTask(self, task, numberOfBooks):
        for _ in range(numberOfBooks):
            schedule.every(1).seconds.do(task)
        while True:
            schedule.run_pending()
