"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User

from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
            creates a user with the specified `email`
            and `hashed_password`, saves to database and returns
            the user object whose (still managed by sqlalchemy session)
        """
        user = User()
        user.email = email
        user.hashed_password = hashed_password
        try:
            self._session.add(user)
            self._session.commit()
        except Exception as e:
            print('error ocurred: {}', format(e))
            self._session.rollback()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        takes in arbitrary keyword arguments and returns the first
        row found in the users table as filtered by the
        method's input arguments
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if not user:
                raise NoResultFound()
            return user
        except NoResultFound:
            raise
        except InvalidRequestError:
            raise
        except Exception as e:
            print(f'error man: {e}')
            raise
    def update_user(self, user_id: int, **kwargs) -> None:
        """
        The method uses `find_user_by` to locate the user 
        to update, then will update the users 
        attributes as passed in the methods arguments 
        then commit changes to the database.

        If an argument that does not correspond to a user 
        attribute is passed, a ValueError is raised.
        """
        user =  self.find_user_by(id=user_id)
        if user:
            for key, val in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, val)
                else:
                    raise ValueError
