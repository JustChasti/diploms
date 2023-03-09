FROM python:3
WORKDIR /balancer
COPY /balancer/requirements.txt /balancer
RUN pip install --no-cache-dir -r requirements.txt
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY /balancer /balancer
RUN mkdir -p /files
CMD ["python3", "app.py"]