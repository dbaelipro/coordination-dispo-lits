import enum
from sqlalchemy_utils import generic_relationship, ChoiceType

from model.abc import db, Base


class OrganisationType(enum.IntEnum):
    finess_et = 1
    company = 2

    @classmethod
    def get_value(cls, name):
        return getattr(cls, name).value

    @classmethod
    def get_name(cls, value):
        return cls(value).name

    def __int__(self):
        return self.value


class Platform(Base):
    __tablename__ = 'orga_platform'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)


class Address(Base):
    __tablename__ = 'orga_address'

    to_json_filter = ('id', "organization", )
    print_filter = ('organization', )

    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(50))
    zipcode = db.Column(db.String(10))
    city = db.Column(db.String(50))
    lon = db.Column(db.Integer)
    lat = db.Column(db.Integer)

    organization = db.relationship("Organization", uselist=False, back_populates="address")


class Organization(Base):
    __tablename__ = 'orga_organization'

    to_json_filter = ('object_type', 'object_id',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    type = db.Column(ChoiceType(OrganisationType, impl=db.Integer()),
                     nullable=False, default=OrganisationType.finess_et)

    address_id = db.Column(db.Integer, db.ForeignKey('orga_address.id'))
    address = db.relationship(Address, back_populates="organization")

   # This is used to discriminate between the linked tables.
    object_type = db.Column(db.Unicode(255))
    # This is used to point to the primary key of the linked row.
    object_id = db.Column(db.Integer)
    data = generic_relationship(object_type, object_id)


class FinessEtablissement(Base):
    __tablename__ = 'orga_finesset'

    id = db.Column(db.Integer, primary_key=True)
    finess_et = db.Column(db.String(15), nullable=False)
    finess_ej = db.Column(db.String(15), nullable=False)


class Company(Base):
    __tablename__ = 'orga_company'

    id = db.Column(db.Integer, primary_key=True)
    siret = db.Column(db.String(15), nullable=False)

