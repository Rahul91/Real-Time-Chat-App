from unittest import TestCase

from healthify.functionality import auth
from healthify.models.configure import session
from healthify.models.user import User


__author__ = 'rahul'


class TestUser(TestCase):

    user_id = 'test-1001-0101-0100010'
    username = 'rahul@testuser.com'
    password = 'test1234'
    first_name = 'Rahul'
    last_name = 'Mishra'

    @classmethod
    def setUpClass(cls):
        super(TestUser, cls).setUpClass()
        cls.user = User(
            id=cls.user_id,
            username=cls.username,
            password=cls.password,
            first_name=cls.first_name,
            last_name=cls.last_name,
        )

        session.add(cls.user)
        session.flush()

    def test_authenticate_fail_because_credentials_are_empty(self):
        self.assertEqual(auth.authenticate(None, None), False)

    def test_authenticate_fail_because_user_not_present(self):
        self.assertEqual(auth.authenticate('notpresent', 'doesntmatter'), False)

    def test_authenticate_fail_because_password_is_wrong(self):
        self.assertEqual(auth.authenticate(self.username, 'wrongpass'), False)

    def test_authenticate_successful(self):
        self.assertIsNot(auth.authenticate(self.username, self.password), False)

    def test_authenticate_fail_because_user_deleted(self):
        self.user.deleted_on = '2016-04-04'
        session.flush()
        self.assertEqual(auth.authenticate(self.username, self.password), False)
        self.user.deleted_on = None
        session.flush()

    def test_identity_fail_because_none_payload(self):
        self.assertRaises(TypeError, auth.identity, None)

    def test_identity_fail_because_invalid_payload(self):
        self.assertRaises(TypeError, auth.identity, 2929)

    def test_identity_successful(self):
        self.assertIsNotNone(auth.identity(dict(identity=self.user_id)))

    def test_get_user_by_id_no_params(self):
        self.assertRaises(KeyError, auth.get_user_by_id)

    def test_get_user_by_id_is_null(self):
        self.assertRaises(ValueError, auth.get_user_by_id, user_id=None)

    def test_get_user_by_id_user_for_value_error(self):
        with self.assertRaises(ValueError) as err_wrong_param:
            auth.get_user_by_id(user_id='wrong-id')
        with self.assertRaises(ValueError) as err_empty_string_param:
            auth.get_user_by_id(user_id='')
        self.user.deleted_on = '2016-04-04'
        session.flush()
        with self.assertRaises(ValueError) as err_deleted_param:
            auth.get_user_by_id(user_id=self.user_id)

        self.assertEqual('BAD-USER-ID', err_wrong_param.exception.message)
        self.assertEqual('REQ-USER-ID', err_empty_string_param.exception.message)
        self.assertEqual('BAD-USER-ID', err_deleted_param.exception.message)

    def test_get_user_by_id_user_for_key_error(self):
        with self.assertRaises(KeyError) as err_empty_param:
           auth.get_user_by_id()
        with self.assertRaises(KeyError) as err_empty_string_param:
            auth.get_user_by_id(user_key_id='')

        self.assertEqual('REQ-USER-ID', err_empty_param.exception.message)
        self.assertEqual('REQ-USER-ID', err_empty_string_param.exception.message)

    def test_get_user_by_id_successful(self):
        self.assertIsNotNone(auth.get_user_by_id(user_id=self.user_id))

    def test_get_user_by_username_is_null(self):
        self.assertRaises(KeyError, auth.get_user_by_username)

    def test_get_user_by_username_invalid(self):
        self.assertRaises(ValueError, auth.get_user_by_username, None, username=[])

    def test_get_user_by_username_user_not_present(self):
        self.assertIsNone(auth.get_user_by_username(username='wrongusername'))

    def test_get_user_by_username_user_deleted(self):
        self.user.deleted_on = '2016-04-04'
        session.flush()
        self.assertIsNone(auth.get_user_by_username(username=self.username))
        self.user.deleted_on = None
        session.flush()

    def test_signup_key_error(self):
        param = dict(
            username='',
            password='somepassword',
            first_name='testt',
            last_name='last'
        )
        with self.assertRaises(ValueError) as err_empty_username:
            auth.signup(**param)
        param = dict(
            username='rahul@rahul.rahul',
            password='',
            first_name='test',
            last_name='last'
        )
        with self.assertRaises(ValueError) as err_empty_password:
            auth.signup(**param)
        param = dict(
            username='rahul@rahul.rahul',
            password='password',
            first_name='',
            last_name='last'
        )
        with self.assertRaises(ValueError) as err_empty_first_name:
            auth.signup(**param)

        self.assertEqual('SIGNUP-BAD-USERNAME', err_empty_username.exception.message)
        self.assertEqual('SIGNUP-REQ-PASSWORD', err_empty_password.exception.message)
        self.assertEqual('SIGNUP-REQ-FIRSTNAME', err_empty_first_name.exception.message)

    @classmethod
    def tearDownClass(cls):
        super(TestUser, cls).tearDownClass()
        session.rollback()


