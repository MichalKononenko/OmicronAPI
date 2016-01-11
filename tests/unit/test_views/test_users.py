"""
Contains unit tests for :mod:`views`
"""
import json
import logging
import unittest
from base64 import b64encode
import mock
from sqlalchemy import create_engine
import views.users as users
from api_server import app
from database.schema import metadata
from database.models.users import User
from database.sessions import ContextManagedSession

__author__ = 'Michal Kononenko'

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

test_engine = create_engine('sqlite:///')
users.database_session = ContextManagedSession(bind=test_engine)


class TestView(unittest.TestCase):
    """
    Contains generic set-up for each view
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up the test client
        :return:
        """
        cls.client = app.test_client(use_cookies=True)
        cls.headers = {'content-type': 'application/json'}
        metadata.create_all(bind=test_engine)

    @classmethod
    def tearDownClass(cls):
        metadata.drop_all(bind=test_engine)


class TestRenderWelcomePage(TestView):
    def setUp(self):
        self.request_method = self.client.get

    def test_page(self):
        self.assertEqual(self.request_method('/').status_code, 200)


class TestUserContainer(TestView):
    @classmethod
    def setUpClass(cls):
        TestView.setUpClass()
        cls.username = 'scott'
        cls.password = 'tiger'
        cls.email = 'scott@tiger.com'


class TestParseSearchQueryParams(TestUserContainer):
    def setUp(self):
        self.url = '/api/v1/users'


class TestParseSearchQueryParamsContains(TestParseSearchQueryParams):
    def setUp(self):
        TestParseSearchQueryParams.setUp(self)
        self.contains_string = 'string'
        self.context = app.test_request_context(
            '%s?contains=%s' % (self.url, self.contains_string)
        )

    def test_contains_string_is_not_none(self):
        with self.context:
            search_string = users.UserContainer.parse_search_query_params(
                    users.request)

            self.assertEqual('%%%s%%' % self.contains_string, search_string)


class TestParseSearchQueryParamsStartsWith(TestParseSearchQueryParams):
    def setUp(self):
        TestParseSearchQueryParams.setUp(self)
        self.contains_string = 'string'
        self.context = app.test_request_context(
            '%s?starts_with=%s' % (self.url, self.contains_string)
        )

    def test_starts_with(self):
        with self.context:
            search_string = users.UserContainer.parse_search_query_params(
                users.request
            )
            self.assertEqual('%s%%' % self.contains_string, search_string)


class TestParseSearchQueryParamsEndsWith(TestParseSearchQueryParams):
    def setUp(self):
        TestParseSearchQueryParams.setUp(self)
        self.contains_string = 'string'
        self.context = app.test_request_context(
            '%s?ends_with=%s' % (self.url, self.contains_string)
        )

    def test_ends_with(self):
        with self.context:
            search_string = users.UserContainer.parse_search_query_params(
                users.request
            )
            self.assertEqual('%%%s' % self.contains_string, search_string)


class TestParseSearchQueryParamsNone(TestParseSearchQueryParams):
    def setUp(self):
        TestParseSearchQueryParams.setUp(self)
        self.context = app.test_request_context(self.url)

    def test_none(self):
        with self.context:
            self.assertEqual(
                '%%%%', users.UserContainer.parse_search_query_params(
                            users.request
                    )
            )


@mock.patch('sqlalchemy.orm.Query.all')
@mock.patch('sqlalchemy.orm.Query.count')
@mock.patch('sqlalchemy.orm.Query.first')
class TestUserContainerGet(TestUserContainer):
    def setUp(self):
        TestUserContainer.setUp(self)
        self.request_method = self.client.get
        self.url = 'api/v1/users'
        self.user = User(self.username, self.password, self.email)
        self.user.verify_password = mock.MagicMock(return_value=True)

    def test_get(self, mock_first, mock_count, mock_all):
        mock_first.return_value = self.user
        mock_all.return_value = [self.user]
        mock_count.return_value = 1

        r = self.request_method(self.url, headers=self.headers)
        self.assertEqual(r.status_code, 200)

        self.assertEqual(mock.call(), mock_all.call_args)
        self.assertEqual(mock.call(), mock_count.call_args)


@mock.patch('sqlalchemy.orm.Session.add')
class TestCreateUser(TestUserContainer):
    def setUp(self):
        self.request_method = self.client.post
        self.url = 'api/v1/users'

    def test_post(self, mock_add):
        data_to_post = {
            'username': self.username,
            'password': self.password,
            'email': self.email
        }

        r = self.request_method(self.url, data=json.dumps(data_to_post),
                                headers=self.headers)
        self.assertEqual(r.status_code, 201)

        self.assertTrue(mock_add.called)

    def test_post_bad_data(self, mock_add):
        data_to_post = {
            'user': self.username,
            'password': self.password,
            'email': self.email
        }
        r = self.request_method(self.url, data=json.dumps(data_to_post),
                                headers=self.headers)
        self.assertEqual(r.status_code, 400)
        self.assertFalse(mock_add.called)


class TestUserView(TestView):

    def setUp(self):
        self.username = 'scott'
        self.password = 'tiger'
        self.email = 'scott@tiger.com'
        self.user = User(self.username, self.password, self.email)
        self.user.verify_password = mock.MagicMock(return_value=True)


@mock.patch('sqlalchemy.orm.Query.all')
@mock.patch('sqlalchemy.orm.Query.count')
@mock.patch('sqlalchemy.orm.Query.first')
class TestGet(TestUserView):

    def setUp(self):
        TestUserView.setUp(self)
        self.request_method = self.client.get
        self.url = 'api/v1/users/%s' % self.username
        self.headers['Authorization'] = 'Basic %s' % \
            b64encode(('%s:%s' % (self.username, self.password)).
                      encode('ascii')).decode('ascii')

        self.bad_user = User('foo', 'bar', 'foo@bar.com')

    @mock.patch('views.users.g')
    def test_get_correct(self, mock_g, mock_first, mock_count, mock_all):
        mock_first.return_value = self.user
        mock_all.return_value = []
        mock_count.return_value = 0

        mock_g.user = self.user

        r = self.request_method(self.url, headers=self.headers)
        self.assertEqual(r.status_code, 200)

        self.assertTrue(mock_first.called)

    @mock.patch('views.users.g')
    def test_get_by_user_id(self, mock_g, mock_first, mock_count, mock_all):
        self.user.id = 1
        mock_first.return_value = self.user
        mock_all.return_value = []
        mock_count.return_value = 0
        mock_g.user = self.user

        url = 'api/v1/users/1'

        r = self.request_method(url, headers=self.headers)
        self.assertEqual(r.status_code, 200)

        self.assertTrue(mock_first.called)