import queue
from datetime import datetime
import threading
from typing import Optional

from qwave.database import session_scope
from qwave.models import Job
from qwave.utils.log_item import log_item

_worker_thread: Optional[threading.Thread] = None
_job_queue: queue.Queue = queue.Queue()
_stop_event = threading.Event()

def process_job(job: Job):
    log_item(content=f"Processing {job.id} ({job.type})", type="JOB")

    with session_scope() as session:
        db_job = session.query(Job).filter(Job.id == job.id).first()
        if db_job:
            db_job.status = "running"
            db_job.started_at = datetime.now()
        
    # TODO: actually do the job lmao
    ...

    with session_scope() as session:
        db_job = session.query(Job).filter(Job.id == job.id).first()
        if db_job:
            db_job.status = "complete"
            db_job.completed_at = datetime.now()
    
    log_item(f"Completed {job.id}", "JOB")

def worker_loop():
    log_item("Worker thread started", "SUCCESS")

    while not _stop_event.is_set():
        try:
            job = _job_queue.get(timeout=1.0)

            try:
                process_job(job)
            except Exception as e:
                log_item(f"Error processing job {job.id}: {e}", "ERROR")

                with session_scope() as session:
                    db_job = session.query(Job).filter(Job.id == job.id).first()
                    if db_job:
                        db_job.status = "failed"
                        db_job.error_message = str(e)
                        db_job.started_at = datetime.now()

            _job_queue.task_done()
        
        except queue.Empty:
            with session_scope() as session:
                pending_jobs = session.query(Job).filter(Job.status == "pending").all()
                for job in pending_jobs:
                    _job_queue.put(job)
    
    log_item("Worker thread stopped!", "WARN")

def start_worker():
    global _worker_thread
    log_item("Starting worker...", "INFO")

    if _worker_thread is not None and _worker_thread.is_alive():
        log_item("Worker is already running!!", "WARN")
        return

    _stop_event.clear()
    _worker_thread = threading.Thread(target = worker_loop, daemon = True)
    _worker_thread.start()

    with session_scope() as session:
        pending_jobs = session.query(Job).filter(Job.status == "pending").all()
        for job in pending_jobs:
            _job_queue.put(job)
        if pending_jobs:
            log_item(f"Loaded {len(pending_jobs)} jobs from db", "INFO")

def stop_worker():
    global _worker_thread

    if _worker_thread is None:
        return

    _stop_event.set()
    _worker_thread.join(timeout=5.0)
    _worker_thread = None

def queue_job(job: Job):
    _job_queue.put(job)