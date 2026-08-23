FROM python:3.14

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app

# FastAPI CLI imports /app/main.py as "app.main" and prepends "/" to sys.path,
# so sibling packages (config, routes, ...) must be on PYTHONPATH explicitly.
ENV PYTHONPATH=/app

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "80", "--workers", "4" ,"--reload"]
