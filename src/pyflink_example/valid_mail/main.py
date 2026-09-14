from pyflink_example.valid_mail.di.container import build_repository
from pyflink_example.valid_mail.job.user_job import build_job

if __name__ == "__main__":
    repo = build_repository()
    build_job(repo)
