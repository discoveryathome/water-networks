FROM python:3.12-slim
WORKDIR /pilot
RUN python -m pip install --no-cache-dir uv==0.11.8
COPY . .
RUN sh tools/setup.sh
CMD [".venv/bin/python", "tools/check.py"]
