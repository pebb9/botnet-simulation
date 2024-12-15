FROM python:3.9-alpine
WORKDIR /app
COPY bot.py /app/
RUN apk add --no-cache curl python3 py3-pip && \
	pip install requests
CMD ["python3", "bot.py"]

