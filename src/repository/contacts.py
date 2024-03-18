from typing import List
from datetime import datetime, timedelta
# from sqlalchemy.orm import Session
from src.database.models import Contact, User
from src.schemas.contacts import ContactModel, ContactUpdate
from sqlalchemy.sql import extract, select
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession as Session


async def find_contacts(contacts_find_data : str, db: Session, user:User) -> Contact | None :
    """
    Retrieves a list of contacts for a specific user with specified pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contacts]
    """
    query = select(Contact).filter_by(user=user).filter(Contact.first_name.ilike(contacts_find_data))
    contacts = await db.execute(query)
    result = contacts.scalars().all()
    if result:
        return result
    query = select(Contact).filter(Contact.second_name.ilike(contacts_find_data))
    contacts = await db.execute(query)
    result = contacts.scalars().all()
    if result:
        return result
    query = select(Contact).filter(Contact.mail.ilike(contacts_find_data))
    contacts = await db.execute(query)
    result = contacts.scalars().all()
    if result:
        return result


#---------------
async def find_contacts_by_birthday_month_and_day(db: Session, month: int, day: int) ->list:
    """
    Retrieves a list of contacts were birthday in month:day.

    :param day: The day of birthdays.
    :type day: int
    :param month: The month of birthdays.
    :type month: int
    :param db: The database session.
    :type db: Session
    :return: A list of contacts in that day.
    :rtype: List[Contacts]
    """
    query = select(Contact).filter(
        extract('month', Contact.birthday) == month,
        extract('day', Contact.birthday) == day
        )
    contacts = await db.execute(query)
    result = contacts.scalars().all()
    return result

async def find_contacts_delta_time(contact_find_days: int, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts in clothers days range.

    :param contact_find_days: The number of days to birthdays period.
    :type contact_find_days: int
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contacts]
    """
    current_date = datetime.now().date()
    dates = []
    result = []
    for i in range(contact_find_days):
        dates.append(current_date + timedelta(days=i))
    for d in dates:
        result.extend(await find_contacts_by_birthday_month_and_day(db, month=d.month, day=d.day))
    return result
#--------------------


async def get_contacts(skip: int, limit: int, db: Session, user:User) -> List[Contact]:
    """
    Retrieves a list of contacts for a specific user with specified pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contacts]
    """
    query = select(Contact).filter_by(user=user).offset(skip).limit(limit)
    contacts = await db.execute(query)
    return contacts.scalars().all() # type: ignore


async def get_all_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    """
        Retrieves a list of contacts for a specific user with specified pagination parameters.

        :param skip: The number of contacts to skip.
        :type skip: int
        :param limit: The maximum number of contacts to return.
        :type limit: int
        :param user: The user to retrieve contacts for.
        :type user: User
        :param db: The database session.
        :type db: Session
        :return: A list of contacts.
        :rtype: List[Contacts]
    """
    query = select(Contact).offset(skip).limit(limit)
    contacts = await db.execute(query)
    return contacts.scalars().all()  # type: ignore
        

async def get_contact(contact_id: int, db: Session, user:User) -> Contact | None:
    """
    Retrieves  contact for the user with specified  parameters.

    :param contact_id: The id of contact.
    :type contact_id: in
    :param db: The database session.
    :type db: Session
    :return: A Contact if exist in db.
    :rtype: Contact | None
    """
    query = select(Contact).filter_by(user=user).filter_by(id=contact_id)
    contact = await db.execute(query)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactModel, db: Session, user:User) -> Contact:
    """
    Creating  contact in db.

    :param ContactModel: The ContactModel of contact to add.
    :type ContactModel: ContactModel
    :param db: The database session.
    :type db: Session
    :return: A new ContactModel .
    :rtype: Contact
    """
    contact = Contact(**body.model_dump(exclude_unset=True), user=user) 
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdate, db: Session, user:User) -> Contact | None:
    """
    Updating  contact in db.

    :param ContactModel: The ContactModel of contact to change.
    :type ContactModel: ContactModel
    :param db: The database session.
    :type db: Session
    :return: A  ContactModel .
    :rtype: Contact|None
    """
    query = select(Contact).filter_by(user=user).filter_by(id=contact_id)
    result = await db.execute(query)
    contact = result.scalar_one_or_none()
    if contact:
        contact.first_name = body.first_name
        contact.second_name = body.second_name   # type: ignore
        contact.mail = body.mail
        contact.birthday = body.birthday
        contact.addition = body.addition
        await db.commit()
        await db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: Session, user:User)  :
    """
    Deleting contact from  db.

    :param contact_id: The contact_id of contacts to del.
    :type contact_id: int
    :param db: The database session.
    :type db: Session
    :return: A deleted ContactModel .
    :rtype: ContactModel
    """
    query = select(Contact).filter_by(user=user).filter_by(id=contact_id)
    contact = await db.execute(query)
    contact =  contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact
    


