import schedule
import time
import threading
from enum import Enum
import re
import tabulate

from starrail.utils.utils import *
from starrail.bin.scheduler.config.starrail_schedule_config import StarRailScheduleConfig
from starrail.controllers.star_rail_app import HonkaiStarRail

SUBMODULE_NAME = "SR-SCL"
SUBMODULE_VERSION = "1.0"

class OperationTypes(Enum):
    START   = "Start Game"
    END     = "Stop Game"


class StartRailJob:
    def __init__(self, job_id: int, job: schedule.Job, op_type: OperationTypes):
        self.job_id = job_id
        self.op_type = op_type
        self.schedule_job = job
        
        self.interval   = job.interval
        self.unit       = job.unit
        self.last_run   = job.last_run
        self.next_run   = job.next_run

    def __str__(self):
        return f"[{Printer.to_lightpurple('JOB')}] {self.op_type} Game - Next run: {self.next_run}, Last run: {self.last_run}"
    
    def print_job(self):
        print(self.__str__())
        
    def to_dict(self):
        return {
            "id"        : self.job_id,
            "op_type"   : self.op_type.value,
            'interval'  : self.interval,
            'unit'      : self.unit,
            'next_run'  : str(self.next_run),
            'last_run'  : str(self.last_run),
        }


class StarRailScheduler:
    def __init__(self, starrail_instance: HonkaiStarRail):
        self.starrail = starrail_instance
        self.schedule_config = StarRailScheduleConfig()
        
        self.jobs: dict[int, StartRailJob] = dict()
        self.__load_schedules() # Load schedule into jobs
        
        self._stop_event = threading.Event()
        self.scheduler_thread = threading.Thread(target=self.__run_scheduler, daemon=True)
        self.scheduler_thread.start()


    # =============================================
    # =========| START/STOP FUNCTIONS | ===========
    # =============================================

    def __load_schedules(self):
        schedules: list[StartRailJob] = self.schedule_config.load_schedule()
        if schedules == None:
            return
        
        for data in schedules:
            job_id = data["id"]
            op_type = OperationTypes(data['op_type'])
            
            matched_time = re.search("[0-9]{2}:[0-9]{2}:[0-9]{2}", data['next_run'])
            if matched_time:
                schedule_time = matched_time.group(0)
            else:
                aprint(f"Failed to read schedule with data: {data}", log_type=LogType.ERROR)
                continue
            
            if op_type == OperationTypes.START:
                job = schedule.every(data['interval']).day.at(schedule_time).do(self.starrail.start)
            elif op_type == OperationTypes.END:
                job = schedule.every(data['interval']).day.at(schedule_time).do(self.starrail.terminate)
            
            job.last_run = data["last_run"]
            self.jobs[job_id] = StartRailJob(job_id, job, op_type)
        
    def __run_scheduler(self):
        while not self._stop_event.is_set():
            schedule.run_pending()
            time.sleep(1)
    
    def stop_scheduler(self):
        aprint("Stopping the scheduler...", submodule_name=SUBMODULE_NAME)
        self._stop_event.set()
        self.scheduler_thread.join()


    # =============================================
    # =========| ADD/REMOVE FUNCTIONS | ===========
    # =============================================

    def add_new_schedule(self, time_str, operation_type: OperationTypes):
        parsed_time = self.__parse_time_format(time_str)
        
        # If parsed time is invalid
        if parsed_time == None:
            aprint(f"Cannot parse time: {time_str}", log_type=LogType.ERROR)
            raise SRExit()
        
        # If scheduled job already exist at the new job time
        for job_id, job in self.jobs.items():
            if job.next_run.strftime(TIME_FORMAT) == parsed_time:
                aprint(f"{Printer.to_lightred(f'Job (ID {job_id}) is already scheduled at time {parsed_time}.')}")
                return
        
        if operation_type == OperationTypes.START:
            job = schedule.every().day.at(parsed_time).do(self.starrail.start)
        elif operation_type == OperationTypes.END:
            job = schedule.every().day.at(parsed_time).do(self.starrail.terminate)

        sr_job_id = self.__get_next_job_id()
        sr_job = StartRailJob(sr_job_id, job, operation_type)
        self.jobs[sr_job_id] = sr_job
        
        aprint(f"New scheduled job (ID {sr_job_id}) has been added to the scheduler successfully!")
        self.show_schedules()
        
        # Save new schedules list into config
        self.schedule_config.save_schedule([job.to_dict() for job in self.jobs.values()])

    def remove_schedule(self):
        self.show_schedules()
        aprint(f"Which job would you like to remove? [ID 1{'-' + str(len(self.jobs)) if len(self.jobs) > 1 else ''}] ", end="")
        user_input_id = input("")
        job_id = self.__parse_id(user_input_id)
        sr_job: StartRailJob = self.__get_job_with_id(job_id)
        
        # Removing job from schedule
        aprint(f"Removing job (ID {job_id})...", end="\r")
        schedule.cancel_job(sr_job.schedule_job)
        
        # Removing job from cache
        del self.jobs[job_id]
        
        # Reset job IDs after deletion
        new_schedule_dict = dict()
        for new_job_id, (old_job_id, sr_job) in enumerate(self.jobs.items()):
            sr_job.job_id = new_job_id+1
            new_schedule_dict[new_job_id+1] = sr_job
        self.jobs = new_schedule_dict
        
        # Saving jobs to config
        self.schedule_config.save_schedule([job.to_dict() for job in self.jobs.values()])
        aprint(f"Job (ID {job_id}) removed successfully.")

    def show_schedules(self):
        if len(self.jobs) == 0:
            aprint(f"No scheduled jobs to show.\nRun {color_cmd('schedule help', True)} for example usages.")
            return
        
        headers = ["ID", "Type", "Action", "Next Run", "Last Run"]
        headers = [Printer.to_lightpurple(title) for title in headers]
        payload = []
        for job_id, job in self.jobs.items():
            payload.append([job_id, "Scheduled Job", job.op_type.value, job.next_run, "None" if job.last_run == None else job.last_run])
        
        
        tab = tabulate.tabulate(payload, headers)
        print("\n" + tab + "\n", flush=True)
        
    def clear_schedules(self):
        if len(self.jobs) == 0:
            aprint("There is currently no schedule job to clear.")
            return
        
        self.show_schedules()
        aprint(f"Are you sure you want to clear all {len(self.jobs)} schedules? [y/n] ", end="")
        user_input = input("").lower().strip()
        if user_input == "y":
            for job_id, sr_job in self.jobs.items():
                aprint(f"Canceling schedule job (ID {job_id})...", end=" ")
                schedule.cancel_job(sr_job.schedule_job)
                print("Done")
                time.sleep(0.1)
            
            self.jobs.clear()
            self.schedule_config.save_schedule([])
            aprint("All scheduled jobs have been canceled successfully.")
            
        else:
            aprint("Clear operation canceled.")
        
        
    # =============================================
    # ===========| HELPER FUNCTIONS | =============
    # =============================================

    def __parse_time_format(self, str_time: str):
        str_time = str_time.strip().lower()
        
        match = re.search("[0-9]+:[0-9]+:[0-9]+", str_time)
        if match:
            return match.group(0)
        
        match2 = re.search("[0-9]+:[0-9]+", str_time)
        if match2:
            return f"{match2.group(0)}:00"
        
        try:
            digit_time = int(str_time)
            return f"{str_time}:00:00"
        except ValueError:
            pass
        
        return None

    def __parse_id(self, str_id: str):
        try:
            str_id = int(str_id)
        except TypeError:
            aprint(f"Invalid ID: {str_id}", log_type=LogType.ERROR)
            raise SRExit()
        return str_id

    def __get_job_with_id(self, job_id: int):
        try:
            target_job = self.jobs[job_id]
            return target_job
        except KeyError:
            aprint(f"Invalid ID: {job_id}", log_type=LogType.ERROR)
            raise SRExit()

    def __get_next_job_id(self):
        return len(self.jobs) + 1


# # # Usage example
# sr = HonkaiStarRail()
# scheduler = SRScheduler(sr)
# scheduler.add_new_schedule("17:52", OperationTypes.START)  # Schedules ABC to run every 10 minutes
# scheduler.add_new_schedule("22:12", OperationTypes.END)  # Schedules ABC to run every 10 minutes

# while True:
#     user_input = input("Enter 'show' to display the schedule or 'exit' to quit: ").strip().lower()
#     if user_input == 'show':
#         scheduler.show_schedules()
#     if user_input == 'remove':
#         scheduler.remove_schedule()
#     elif user_input == 'exit':
#         scheduler.stop_scheduler()
#         break
