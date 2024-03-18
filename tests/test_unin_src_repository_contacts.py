
import unittest
from unittest import mock
from unittest.mock import MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact, User
from src.schemas.contacts import ContactModel, ContactUpdate
from src.repository.contacts import (
    get_contacts,
    get_contact,
    get_all_contacts,
    find_contacts,
    find_contacts_delta_time,
    find_contacts_by_birthday_month_and_day,
    create_contact,
    update_contact,
    remove_contact,
)


class TestAsyncContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)
        self.user = User(id=1, username="testuser", confirmed = True)

    async def test_find_contacts(self):
        contacts = [Contact(id = 1, mail = "qwerty@i.ua", user = self.user), 
                    Contact(user= User(id=2)), 
                    Contact()]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await find_contacts("qwerty", self.session, self.user)
        self.assertEqual(result, contacts, msg=f"--------{result} != {contacts}")

    async def test_find_contacts_by_birthday_month_and_day(self):
        contact1 = Contact(id = 1, birthday = '2000-03-07', user = self.user)
        contact2 = Contact(id = 2, birthday = '2003-03-09', user = self.user)
        mocked_contact = MagicMock()
        mocked_contact.scalars.return_value.all.return_value = contact2
        self.session.execute.return_value = mocked_contact
        result = await find_contacts_by_birthday_month_and_day(self.session, month=3, day=9)
        self.assertEqual(result, contact2)
        self.assertNotEqual(result, contact1)

    async def test_find_contacts_delta_time(self):
        contacts = [Contact(id = 1, birthday = '2003-03-11'), 
                    Contact(id = 3, birthday = '2003-03-09')]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await find_contacts_delta_time(contact_find_days=7, db=self.session)
        self.assertEqual(result, contacts*7, msg = f"======{result}")
        self.assertNotEqual(result, contacts)

    async def test_get_all_contacts(self):
        limit = 10
        offset = 0
        contacts = [Contact(id = 1, mail = "qwerty@i.ua"), 
                    Contact(), 
                    Contact()]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_all_contacts(limit, offset,self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts(self):
        limit = 10
        offset = 0
        contacts = [Contact(id = 1, mail = "qwerty@i.ua", user = self.user), 
                    Contact(user= User(id=2)), 
                    Contact()]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts(limit, offset,self.session, self.user)
        self.assertEqual(result, contacts)

    async def test_get_contact(self):
        contact = Contact(id = 1, mail = "qwerty@i.ua", user = self.user)
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = contact
        self.session.execute.return_value = mocked_contact
        result = await get_contact(1, self.session, self.user)
        self.assertEqual(result, contact)

    async def test_create_contact(self):
        body = ContactModel(first_name="test_name", second_name="test_sec", mail = "qwerty@i.ua", birthday='2000-03-07', addition="qwerty")
        result = await create_contact(body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.second_name, body.second_name)
        self.assertEqual(result.mail, body.mail)

    async def test_update_contact(self):
        body = ContactUpdate(first_name="test_name", second_name="test_sec", mail = "qwerty@i.ua", birthday='2000-03-17', addition="qwerty", created_at="2024-03-07")
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value =Contact(id=1,)
        self.session.execute.return_value= mocked_contact
        result = await update_contact(contact_id=1, body=body, db=self.session, user=self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.second_name, body.second_name)
        self.assertEqual(result.mail, body.mail)

    async def test_remove_contact(self):
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value =Contact(id=1,)
        self.session.execute.return_value= mocked_contact
        result = await remove_contact(contact_id=1, db=self.session, user=self.user)
        self.assertIsInstance(result, Contact)
        self.session.delete.assert_called_once()
        self.assertEqual(result.id, 1)



if __name__ == '__main__':
    unittest.main()
