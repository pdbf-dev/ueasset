from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

file_tags = Table('file_tags', Base.metadata,
    Column('file_id', Integer, ForeignKey('files.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class File(Base):
    __tablename__ = 'file'
    id = Column(Integer, primary_key=True)
    path = Column(String, unique=True, index=True)
    tags = relationship("Tag", secondary=file_tags, back_populates="file")

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    files = relationship("File", secondary=file_tags, back_populates="tag")

engine = create_engine('sqlite:///tags.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
