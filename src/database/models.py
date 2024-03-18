import enum
from datetime import date
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey, DateTime, func, Enum, Boolean


class Base(DeclarativeBase):
    pass



class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    second_name: Mapped[str] = mapped_column(String(50))
    mail: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    birthday: Mapped[date] =  mapped_column("birthday", DateTime, nullable=True)
    addition: Mapped[str] = mapped_column(String(255), nullable=True) 
    created_at: Mapped[date] = mapped_column(
        "created_at", DateTime, default=func.now(), nullable=True)
    updated_at: Mapped[date] = mapped_column(
        "updated_at", DateTime, default=func.now(), onupdate=func.now(), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship("User", backref="contacts", lazy="joined")


# class Contact(Base):
#     __tablename__ = "contacts"
#     id = Column(Integer, primary_key=True)
#     first_name = Column(String(50), nullable=False)
#     second_name = Column(String(50), nullable=False)
#     mail = Column(String(60), unique=True, nullable=False)
#     birthday = Column(Date, nullable=True)
#     addition = Column(String(300), nullable=True)
#     created_at = Column('created_at', DateTime, default=func.now())
#     updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now())
#     user_id =  Column(Integer, ForeignKey("users.id"),nullable=True)
#     user = relationship("User" , backref="contacts", lazy="joined")
#     def __str__(self) -> str:
#         return f'-------{self.birthday}'


class Role(enum.Enum):
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"


# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     username = Column(String(255), nullable=False)
#     mail = Column(String(160), unique=True)
#     password = Column(String(255), nullable=False)
#     avatar = Column(String(255), nullable=True)
#     refresh_token = Column(String(255), nullable=True)
#     created_at = Column('created_at', DateTime, default=func.now(), nullable=True)
#     updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now())
#     role = Column("role", Enum(Role), default=Role.user) #, nullable=True
#     confirmed = Column("confirmed", Boolean, default=False)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    mail: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[date] = mapped_column("created_at", DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column(
        "updated_at", DateTime, default=func.now(), onupdate=func.now()
    )
    role: Mapped[Enum] = mapped_column(
        "role", Enum(Role), default=Role.user, nullable=True
    )
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)



