"""
This Python file contains database objects
and schema for CFLTools.
"""

from sqlalchemy import Column, ForeignKey, Integer, \
                       String, DateTime, Boolean, \
                       create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from cfltools.config import log_generator


# Instantiate the logger.
logger = log_generator(__name__)


# Define the sqlalchemy base class.
Base = declarative_base()
BaseSession = sessionmaker()


# Define global vars
# Lengths of various string fields.
# TODO: Adjust these lengths to be sensible.
IPv4_ADDR_LEN = 250
IPv6_ADDR_LEN = 250
INCIDENT_ID_LEN = 250
INCIDENT_NAME_LEN = 250
COUNTRY_CODE_LEN = 250
COUNTRY_LEN = 250
ASN_LEN = 250
ASN_DESC_LEN = 250
FOLDER_LOC_LEN = 500
DESC_LEN = 1000
SHORT_DESC_LEN = 1000
PHONE_LEN = 250
EMAIL_LEN = 250
MD5_LEN = 250

# Configuration file.


class Incident(Base):
    """
    Database object to store information about
    specific incidents.
    """
    __tablename__ = 'incidents'
    id = Column(Integer, primary_key=True)
    incident_id = Column(Integer, unique=True)
    incident_name = Column(String(INCIDENT_NAME_LEN))
    folder_loc = Column(String(FOLDER_LOC_LEN))
    description = Column(String(DESC_LEN))

    # An incident is related to many IP Addresses.
    ipaddrs = relationship("IPAddr", back_populates="incident")

    def __repr__(self):
        return  """
            <Incident(incident_id={}, incident_name={}, folder_loc={},
                      description={})
                """ % (self.incident_id, self.incident_name, self.folder_loc,
                       self.description)


class IPAddr(Base):
    """
    Database object to store all IP addresses seen by the
    system.
    IP addresses may appear multiple times in the database.
    This database represents one unique IP that appeared in
    one incident. If an IP appears in multiple incidents, it
    will be listed multiple times with number of occurances
    in logs related to that incident.
    """
    __tablename__ = 'ipaddrs'
    id = Column(Integer, primary_key=True)
    ipv4 = Column(String(IPv4_ADDR_LEN))
    ipv6 = Column(String(IPv6_ADDR_LEN))
    number_occurances = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    whois_done = Column(Boolean, default=False)
    is_tor_exit_node = Column(Boolean, default=False)

    # An IP address is related to an ISP.
    asn = Column(Integer, ForeignKey('isp.asn'))
    isp = relationship("ISP", back_populates="ipaddrs")

    # An IP address is related to an incident.
    incident_id = Column(String(INCIDENT_ID_LEN), ForeignKey('incidents.incident_id'))
    incident = relationship("Incident", back_populates="ipaddrs")

    def __repr__(self):
        return  """
            <IPAddr(ipv4={}, ipv6={}, number_occurances={}, incident_id={},
                    start_time={}, end_time={}, country_code={}
                    country={}, asn={}
                    whois_done={}, is_tor_exit_node={}
                """ % (self.ipv4, self.ipv6, self.number_occurances,
                       self.incident_id, self.start_time, self.end_time,
                       self.country_code, self.country_code, self.asn,
                       self.whois_done, self.is_tor_exit_node)


class ISP(Base):
    """
    Database to locally track whois data obtained from
    previous queries. This is so that we don't have to
    tax APIs with whois queries, and so that we can add
    in LEO contact information for those ISPs that publish
    it.
    """
    __tablename__ = 'isp'
    id = Column(Integer, primary_key=True)
    asn = Column(Integer, unique=True)
    description = Column(String(DESC_LEN))
    contact_name = Column(String(SHORT_DESC_LEN))
    online_service = Column(String(SHORT_DESC_LEN))
    online_attn = Column(String(SHORT_DESC_LEN))
    online_serv_address = Column(String(DESC_LEN))
    phone = Column(String(PHONE_LEN))
    fax = Column(String(PHONE_LEN))
    email = Column(String(EMAIL_LEN))
    notes = Column(String(DESC_LEN))
    req_nda = Column(Boolean)

    # An ASN is related to many IP addresses.
    ipaddrs = relationship("IPAddr", back_populates="isp")

    def __repr__(self):
        return  """
            <ISP(asn={}, online_service={}) >
                """ % (self.asn, self.online_service)


class SeenFile(Base):
    """
    Database object to store information about an
    already seen file. We'll use this later to avoid
    double or redundant imports.
    """
    __tablename__ = 'seenfiles'
    id = Column(Integer, primary_key=True)
    filename = Column(String(FOLDER_LOC_LEN))
    md5 = Column(String(MD5_LEN))
    incident_id = Column(Integer, unique=True)

    def __repr__(self):
        return  """
            <SeenFile(filename={}) >
                """ % (self.filename)


def makesession(db_file=None):
    """
    Creates a database session.
    If the database parameter is not given, it will create a new
    database in memory for testing.
    """
    if db_file == None:
        logger.warning("Instantiating an in-memory-only database for testing.")
        db_file = 'sqlite:///:memory:'
    engine = create_engine(db_file, echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
