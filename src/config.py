import postgres_local

remote_postgre = {
    "url": "mentcare.cfteod2es6ye.us-east-1.rds.amazonaws.com",
    "port": "5432",
    "username": "postgres",
    "passwd": "(mfgaH3)",
    "database": "MentCare",
}

Damon_local = {
    "host":"localhost",
    "port": "5432",
    "username": "shaw",
    "passwd": "740202",
    "database": "postgres",
    "schema": "public"

}

DBconnect = postgres_local.PostgresToolBox(Damon_local["database"],
                                           Damon_local["username"],
                                           Damon_local["passwd"],
                                           Damon_local["host"],
                                           Damon_local["port"],
                                           )
schema = Damon_local["schema"]
# self.postgresDB = postgres_connect.PostgresHandler(config.remote_postgre["url"],
#                                                       config.remote_postgre["port"],
#                                                       config.remote_postgre["username"],
#                                                       config.remote_postgre["passwd"],
#                                                       config.remote_postgre["database"])