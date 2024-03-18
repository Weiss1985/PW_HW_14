
import unittest
from unittest import mock
from unittest.mock import MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact, User
from src.schemas.auth import UserModel,UserResponse,UsertUpdate
from src.repository.users import (
    create_user,
    get_user_by_mail,
    update_token,
    update_avatar_url,
    confirmed_email,
)


class TestAsyncContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)
        self.user = User(id=1, username="testuser",mail = "qwerty@i.ua", confirmed = True)

    async def test_create_user(self):
        body = UserModel(username="test_name", password="pass", mail = "qwerty@i.ua", birthday='2000-03-07', addition="qwerty")
        result = await create_user(body, self.session)
        self.assertIsInstance(result, User)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.password, body.password)
        self.assertEqual(result.mail, body.mail)

    async def test_get_user_by_mail(self):
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = self.user
        self.session.execute.return_value = mocked_user
        result = await get_user_by_mail("qwerty@i.ua", self.session)
        self.assertEqual(result, self.user)












    # async def test_find_contacts(self):
    #     contacts = [Contact(id = 1, mail = "qwerty@i.ua", user = self.user), 
    #                 Contact(user= User(id=2)), 
    #                 Contact()]
    #     mocked_contacts = MagicMock()
    #     mocked_contacts.scalars.return_value.all.return_value = contacts
    #     self.session.execute.return_value = mocked_contacts
    #     result = await find_contacts("qwerty", self.session, self.user)
    #     self.assertEqual(result, contacts, msg=f"--------{result} != {contacts}")

    # async def test_find_contacts_by_birthday_month_and_day(self):
    #     contact1 = Contact(id = 1, birthday = '2000-03-07', user = self.user)
    #     contact2 = Contact(id = 2, birthday = '2003-03-09', user = self.user)
    #     mocked_contact = MagicMock()
    #     mocked_contact.scalars.return_value.all.return_value = contact2
    #     self.session.execute.return_value = mocked_contact
    #     result = await find_contacts_by_birthday_month_and_day(self.session, month=3, day=9)
    #     self.assertEqual(result, contact2)
    #     self.assertNotEqual(result, contact1)

    # async def test_find_contacts_delta_time(self):
    #     contacts = [Contact(id = 1, birthday = '2003-03-11'), 
    #                 Contact(id = 3, birthday = '2003-03-09')]
    #     mocked_contacts = MagicMock()
    #     mocked_contacts.scalars.return_value.all.return_value = contacts
    #     self.session.execute.return_value = mocked_contacts
    #     result = await find_contacts_delta_time(contact_find_days=7, db=self.session)
    #     self.assertEqual(result, contacts*7, msg = f"======{result}")
    #     self.assertNotEqual(result, contacts)

    # async def test_get_all_contacts(self):
    #     limit = 10
    #     offset = 0
    #     contacts = [Contact(id = 1, mail = "qwerty@i.ua"), 
    #                 Contact(), 
    #                 Contact()]
    #     mocked_contacts = MagicMock()
    #     mocked_contacts.scalars.return_value.all.return_value = contacts
    #     self.session.execute.return_value = mocked_contacts
    #     result = await get_all_contacts(limit, offset,self.session)
    #     self.assertEqual(result, contacts)

    # async def test_get_contacts(self):
    #     limit = 10
    #     offset = 0
    #     contacts = [Contact(id = 1, mail = "qwerty@i.ua", user = self.user), 
    #                 Contact(user= User(id=2)), 
    #                 Contact()]
    #     mocked_contacts = MagicMock()
    #     mocked_contacts.scalars.return_value.all.return_value = contacts
    #     self.session.execute.return_value = mocked_contacts
    #     result = await get_contacts(limit, offset,self.session, self.user)
    #     self.assertEqual(result, contacts)




if __name__ == '__main__':
    unittest.main()



