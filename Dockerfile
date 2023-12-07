FROM python:3.11.6-slim

ENV APP_DIR=ufpa_sd_tiktaktoe

WORKDIR /$APP

COPY pyproject.toml .
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY $APP/ .

ENV PYTHONDEBUG=0
ENTRYPOINT ["python", "ufpa_sd_tiktaktoe"]
CMD ["-c"]
