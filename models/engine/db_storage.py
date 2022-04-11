from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from os import getenv
from models.base_model import Base
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.review import Review
from models.user import User
from models.place import Place


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Creates the engine for the database"""
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        database = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")
    
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(user, passwd, host, database), pool_pre_ping=True)
        if env == "test":
            Base.metadata.drop_all(self.__engine) 

    def all(self, cls=None):
        """
        Query on the current database session all objects
        depending of the class name (cls)
        Args:
            self (class instance)
            cls (Instance of the class)
        """
        clsDict = {}
        typeOfObjects = {"City": City, "State": State, "Amenity": Amenity, "Place": Place, "Review": Review, "User": User}
        if cls:
            for instance in self.__session.query(typeOfObjects[cls]).all():
                key = instance.__class__.__name__ + "." + instance.id
                clsDict[key] = instance
                if "_sa_instance_state" in instance.__dict__:
                    del instance.__dict__["_sa_instance_state"]
        else:
            for obj in typeOfObjects.values():
                for instance in self.__session.query(obj).all():
                    key = instance.__class__.__name__ + '.' + instance.id
                    clsDict[key] = instance
                    if "_sa_instance_state" in instance.__dict__:
                        del instance.__dict__["_sa_instance_state"]
        return clsDict
            
    def new(self, obj):
        """
        Add a new element into the database session
        Args:
            self (class instance)
            obj (BaseModel instance or child) : New obj to 
                    add into the database
        Return: Nothing
        """
        self.__session.add(obj)
        

    def save(self):
        """
        Commit all change into the database
        Args:
            self (class instance)
        Nothing: Nothing
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete an element from the database session
        Args:
            self (class instance)
            obj (BaseModel instance or child) : obj to 
                    delete from the database
        Return: Nothing
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and the session
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session
        