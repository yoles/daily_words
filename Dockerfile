FROM python:latest

COPY /requirements /requirements
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "zsh"]
RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true
RUN apt-get install -y xclip vim gettext
RUN pip install --no-cache-dir -r /requirements/dev.txt

WORKDIR /app/

COPY . /app/

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
