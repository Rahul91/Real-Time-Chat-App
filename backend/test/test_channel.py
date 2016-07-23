from unittest import TestCase

from healthify.functionality import channel
from healthify.models.configure import session
from healthify.models.channel import Channel
from healthify.models.user import User

__author__ = 'rahul'


class TestChannel(TestCase):

    user_id = 'test-1001-0101-0100010'
    username = 'rahul@testuser.com'
    password = 'test1234'
    first_name = 'Rahul'
    last_name = 'Mishra'

    channel_id = 'test-channel-0101-0100010'
    channel_name = 'rahul@testuser.com'
    type = 'test1234'

    @classmethod
    def setUpClass(cls):
        super(TestChannel, cls).setUpClass()
        cls.user = User(
            id=cls.user_id,
            username=cls.username,
            password=cls.password,
            first_name=cls.first_name,
            last_name=cls.last_name,
        )

        session.add(cls.user)
        session.flush()

        cls.channel = Channel(
            id=cls.channel_id,
            name=cls.channel_name,
            type=cls.type,
            created_by=cls.user.id,
        )

        session.add(cls.channel)
        session.flush()

    # def test_get_channel_by_name_successful(self):
    #     self.assertIsNotNone(channel.get_channel_by_name(channel_name=self.channel_name))

    def test_get_channel_by_id_no_params(self):
        self.assertRaises(KeyError, channel.get_channel_by_id)

    # def test_get_user_by_id_successful(self):
    #     self.assertIsNotNone(channel.get_channel_by_id(channel_id=self.channel_id))

    def test_get_channel_by_id_is_null(self):
        self.assertRaises(KeyError, channel.get_channel_by_id, user_id=None)

    def test_get_channel_by_id_for_value_error(self):
        with self.assertRaises(ValueError) as err_wrong_param:
            channel.get_channel_by_id(channel_id='wrong-id')
        self.channel.deleted_on = '2016-04-04'
        session.flush()
        with self.assertRaises(ValueError) as err_deleted_param:
            channel.get_channel_by_id(channel_id=self.channel_id)
        with self.assertRaises(ValueError) as err_empty_string_param:
            channel.get_channel_by_id(channel_id='')

        self.assertEqual('INVALID-CHANNEL-ID', err_wrong_param.exception.message)
        self.assertEqual('INVALID-CHANNEL-ID', err_deleted_param.exception.message)
        self.assertEqual('REQ-CHANNEL-ID', err_empty_string_param.exception.message)

    def test_get_user_by_id_user_for_key_error(self):
        with self.assertRaises(KeyError) as err_empty_param:
           channel.get_channel_by_id(channel_wrong_id=self.channel_id)

        self.assertEqual('REQ-CHANNEL-ID', err_empty_param.exception.message)

    def test_get_channel_by_name_no_params(self):
        self.assertRaises(KeyError, channel.get_channel_by_name)

    def test_get_channel_by_name_is_null(self):
        self.assertRaises(ValueError, channel.get_channel_by_name, channel_name=None)

    def test_get_channel_by_name_for_value_error(self):
        # with self.assertRaises(ValueError) as err_wrong_param:
        #     channel.get_channel_by_name(channel_name='wrong-id')
        # self.channel.deleted_on = '2016-04-04'
        # session.flush()
        # with self.assertRaises(ValueError) as err_deleted_param:
        #     channel.get_channel_by_name(channel_name=self.channel_id)
        with self.assertRaises(ValueError) as err_empty_string_param:
            channel.get_channel_by_name(channel_name='')
        #
        # self.assertEqual('INVALID-CHANNEL-NAME', err_wrong_param.exception.message)
        # self.assertEqual('INVALID-CHANNEL-NAME', err_deleted_param.exception.message)
        self.assertEqual('REQ-CHANNEL-NAME', err_empty_string_param.exception.message)

    def test_get_channel_by_name_for_key_error(self):
        with self.assertRaises(KeyError) as err_empty_param:
           channel.get_channel_by_name(channel_name_wrong=self.channel_id)

        self.assertEqual('REQ-CHANNEL-NAME', err_empty_param.exception.message)

    # TODO: Have to write remaining testcases
    
    @classmethod
    def tearDownClass(cls):
        super(TestChannel, cls).tearDownClass()
        session.rollback()