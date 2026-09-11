from pyflink_example.di.container import build_repository
from pyflink_example.job.user_job import build_job

if __name__ == "__main__":
    repo = build_repository()
    build_job(repo)
