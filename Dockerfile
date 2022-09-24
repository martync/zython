FROM python:3.9-slim

WORKDIR /usr/src/app/

COPY requirements.txt ./
RUN pip install --disable-pip-version-check --no-warn-script-location --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000
ENTRYPOINT ["/usr/src/app/scripts/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
