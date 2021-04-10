FROM python:3.8

RUN python -m pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

# ADD docker-entrypoint.sh /docker-entrypoint.sh
# RUN chmod a+x /docker-entrypoint.sh
COPY . .
# ENTRYPOINT ["/docker-entrypoint.sh"]
