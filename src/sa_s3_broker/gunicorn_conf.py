import multiprocessing  # noqa: F401

workers = 3
worker_class = "uvicorn.workers.UvicornWorker"

timeout = 10
max_requests = 1000  # n
max_requests_jitter = 200 # m

bind = "0.0.0.0:8000"
