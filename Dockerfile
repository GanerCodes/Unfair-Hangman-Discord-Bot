FROM python:3
RUN pip install discord
COPY . .
CMD ["python", "bot.py"]