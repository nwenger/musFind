from python

WORKDIR ./src
ADD . ./src

ENV NAME musicfind

RUN mkdir /usr/sql
RUN chmod 644 /usr/sql

ADD ["src/mf.py","/src/mf.py"]
ADD ["src/req.txt","/src/req.txt"]

RUN pip install -r /src/req.txt
RUN python /src/mf.py
