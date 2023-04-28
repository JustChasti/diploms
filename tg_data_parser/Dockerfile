FROM python:3
WORKDIR /tg_data_parser
COPY /tg_data_parser/requirements.txt /tg_data_parser
RUN pip install --no-cache-dir -r requirements.txt
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY /tg_data_parser /tg_data_parser
CMD ["python3", "app.py"]