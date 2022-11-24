FROM python:3

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src
COPY data/ ./data
COPY run_page_rank.sh ./

RUN chmod u+x src/page_rank.py
RUN chmod u+x src/prepare_data.py

CMD [ "bash", "run_page_rank.sh" ]