import time
import queue
import threading

from typing import Optional
from pathlib import Path
from datetime import datetime

from qwave.models import Job, Track
from qwave.database import session_scope
from qwave.utils.log_item import log_item
from qwave.services.file_service import build_track_path
from qwave.services.transcode_service import transcode, transcode_verify

_worker_thread: Optional[threading.Thread] = None
_job_queue: queue.Queue = queue.Queue()
_stop_event = threading.Event()

def process_job(job: Job):
    log_item(content=f"Processing {job.id} ({job.type})", type="JOB")

    with session_scope() as session:
        db_job = session.query(Job).filter(Job.id == job.id).first()
        if not db_job:
            log_item(f"Job {job.id} not found in db", "ERROR")
            return
        db_job.status = "running"
        db_job.started_at = datetime.now()
        session.commit()

        track = session.query(Track).filter(Track.id == job.track_id).first()
        if not track:
            fail_job(job, "Track {job.track_id} not found")
            return

        temp_file = Path(track.file_path)

        if not temp_file.exists():
            fail_job(job, "File not found at {temp_file}")
            return

        output_path = build_track_path(
            artist_name = track.artists[0].name if track.artists else "Unknown Artist",
            track_title = track.title,
            album_title = track.album.title if track.album else None,
            album_year  = track.album.release_date.year if track.album and track.album.release_date else None,
            track_number = track.track_number if track.track_number else None
        )

        log_item(f"Transcoding to {output_path}", "INFO")

        success, error = transcode(temp_file, output_path)

        if not success:
            fail_job(job, f"Transcode failed: {error}")
            return

        success, error = transcode_verify(temp_file, output_path)

        if not success:
            fail_job(job, f"Transcode couldn't be verified: {error}")
            if output_path.exists():
                output_path.unlink()
            return

        track.opus_path = str(output_path)

        try:
            temp_file.unlink()
        except Exception as e:
            log_item(f"Could not delete temp file: {e}", "ERROR")

        db_job.status = "complete"
        db_job.completed_at = datetime.now()
        session.commit()

        log_item(f"Completed {job.id}", "JOB")

# def process_job():
#     if job.type == "transcode":
#         transcode_job(job)
#     else:
#         log_item(f"Invalid job type: {job.type}", ERROR)

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
                        session.commit()

            _job_queue.task_done()

        except queue.Empty:
            with session_scope() as session:
                pending_jobs = session.query(Job).filter(Job.status == "pending").all()
                for job in pending_jobs:
                    _job_queue.put(job)
                session.commit()

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

def fail_job(job: Job, message: str):
    with session_scope() as session:
        db_job = session.query(Job).filter(Job.id == job.id).first()
        if db_job:
            db_job.status = "failed"
            db_job.error_message = message
            db_job.completed_at = datetime.now()
            session.commit()
            log_item(message, "ERROR")
