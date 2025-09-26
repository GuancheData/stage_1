import schedule

class BookRequestSchedule:
    def scheduleTask(self, task, booksNumber):
        for _ in range(booksNumber):
            schedule.every(1).minute.do(task)
        while True:
            schedule.run_pending()
