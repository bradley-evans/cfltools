def validateDB(conn):
    c = conn.cursor()
    create_ipaddrs = """
        CREATE TABLE IF NOT EXISTS ipaddrs(
            id INTEGER,
            ip TEXT,
            number_occurances INTEGER,
            incident_id TEXT,
            start_time INTEGER,
            end_time INTEGER,
            country_code TEXT,
            country TEXT,
            asn TEXT,
            asn_description TEXT,
            whois_done TEXT,
            is_tor_exit_node TEXT,
            PRIMARY KEY (id),
            FOREIGN KEY (asn) REFERENCES isp(asn),
            FOREIGN KEY (incident_id) REFERENCES incidents(incident_id)
            )
        """
    create_incidents = """
        CREATE TABLE IF NOT EXISTS incidents(
            incident_id INTEGER UNIQUE,
            incident_name TEXT UNIQUE,
            folder_loc TEXT UNIQUE,
            description TEXT,
            PRIMARY KEY(incident_id)
            )
        """
    create_isp = """
        CREATE TABLE IF NOT EXISTS isp(
            id INTEGER UNIQUE,
            asn TEXT UNIQUE,
            description TEXT,
            contact_name TEXT,
            online_service TEXT,
            online_attn TEXT,
            online_serv_address TEXT,
            phone TEXT,
            fax TEXT,
            email TEXT,
            notes TEXT,
            req_nda TEXT,
            PRIMARY KEY(id)
            )
        """
    create_seenfiles = """
        CREATE TABLE IF NOT EXISTS seenfiles(
            filename TEXT,
            md5 TEXT UNIQUE,
            incident_id TEXT,
            FOREIGN KEY (incident_id) REFERENCES incidents(incident_id)
            )
        """
    c.execute(create_isp)
    c.execute(create_incidents)
    c.execute(create_ipaddrs)
    c.execute(create_seenfiles)
    conn.commit()
