#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
FROM debian:stable
MAINTAINER Tim Sutton<tim@kartoza.com>

RUN  export DEBIAN_FRONTEND=noninteractive
ENV  DEBIAN_FRONTEND noninteractive
RUN  dpkg-divert --local --rename --add /sbin/initctl

RUN apt-get -y update; apt-get -y install gnupg2 wget ca-certificates rpl pwgen
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

#-------------Application Specific Stuff ----------------------------------------------------

# We add postgis as well to prevent build errors (that we dont see on local builds)
# on docker hub e.g.
# The following packages have unmet dependencies:
RUN apt-get update; apt-get install -y postgresql-client-10 postgresql-common postgresql-10 postgresql-10-postgis-2.4 postgresql-10-pgrouting netcat

# Open port 5432 so linked containers can see them
EXPOSE 5432

# Run any additional tasks here that are too tedious to put in
# this dockerfile directly.
COPY ./compose/production/docker-postgis-develop/env-data.sh /
COPY ./compose/production/docker-postgis-develop/setup.sh /
RUN chmod +x /setup.sh
RUN /setup.sh

# We will run any commands in this when the container starts
COPY ./compose/production/docker-postgis-develop/docker-entrypoint.sh /
COPY ./compose/production/docker-postgis-develop/setup-conf.sh /
COPY ./compose/production/docker-postgis-develop/setup-database.sh /
COPY ./compose/production/docker-postgis-develop/setup-pg_hba.sh /
COPY ./compose/production/docker-postgis-develop/setup-replication.sh /
COPY ./compose/production/docker-postgis-develop/setup-ssl.sh /
COPY ./compose/production/docker-postgis-develop/setup-user.sh /
COPY ./compose/production/docker-postgis-develop/postgresql.conf /tmp/
RUN chmod +x /docker-entrypoint.sh

# Optimise postgresql
RUN echo "kernel.shmmax=543252480" >> /etc/sysctl.conf
RUN echo "kernel.shmall=2097152" >> /etc/sysctl.conf

ENTRYPOINT /docker-entrypoint.sh
