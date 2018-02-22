FROM mysql

WORKDIR ./db

ADD . ./db


ENV NAME mdb
ENV MYSQL_ROOT_PASSWORD trike

RUN mkdir /usr/sql
RUN chmod 644 /usr/sql

EXPOSE 3306

ADD ["db/init.sql", "/docker-entrypoint-initdb.d/init.sql"]

RUN /etc/init.d/mysql start
