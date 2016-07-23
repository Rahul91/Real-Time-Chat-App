from unittest import TestCase

from healthify.functionality import channel, chat
from healthify.models.configure import session
from healthify.models.channel import Channel
from healthify.models.chat import ChatHistory
from healthify.models.common import UserChannelMapping
from healthify.models.user import User

__author__ = 'rahul'


class TestChat(TestCase):

    user_id = 'test-1001-0101-0100010'
    username = 'rahul@testuser.com'
    password = 'test1234'
    first_name = 'Rahul'
    last_name = 'Mishra'

    channel_id = 'test-channel-0101-0100010'
    channel_name = 'rahul@testuser.com'
    type = 'test1234'

    message = 'this is a test message'
    message_id = 'test-message-101001-1101'

    @classmethod
    def setUpClass(cls):
        super(TestChat, cls).setUpClass()
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

        cls.chat = ChatHistory(
            id=cls.message_id,
            published_by=cls.user_id,
            message=cls.message,
            channel=cls.channel_id,
        )
        session.add(cls.chat)
        session.flush()

    def test_publish_message_no_params(self):
        self.assertRaises(KeyError, chat.publish_message)

    def test_publish_message_is_null(self):
        self.assertRaises(KeyError, chat.publish_message, channel_name=None, message=None)

    def test_publish_message_for_value_error(self):
        with self.assertRaises(ValueError) as err_wrong_param:
            chat.publish_message(channel_name=None, message=None, user_id=self.user_id)
        with self.assertRaises(ValueError) as err_incomplete_param:
            chat.publish_message(channel_name=None, message='some message', user_id=self.user_id)
        self.chat.deleted_on = '2016-04-04'
        session.flush()
        with self.assertRaises(ValueError) as err_deleted_param:
            chat.publish_message(channel_name=self.channel_name, message='some message', user_id=None)
        with self.assertRaises(ValueError) as err_empty_string_param:
            chat.publish_message(channel_name=None, message='some message', user_id=self.user_id)

        self.assertEqual('PUB-REQ-MESSAGE-PAYLOAD', err_wrong_param.exception.message)
        self.assertEqual('PUB-REQ-CHANNEL', err_incomplete_param.exception.message)
        self.assertEqual('REQ-USER-ID', err_deleted_param.exception.message)
        self.assertEqual('PUB-REQ-CHANNEL', err_empty_string_param.exception.message)

    # TODO: Have to write remaining testcases

    @classmethod
    def tearDownClass(cls):
        super(TestChat, cls).tearDownClass()
        session.rollback()
