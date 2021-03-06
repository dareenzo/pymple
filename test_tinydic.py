# coding: utf-8

import unittest
from tinydic import Container


class Service:

    def __init__(self, setting):
        self.setting = setting

    def do_work(self):
        pass


class Client:

    def __init__(self, service):
        self.service = service

    def do_something(self, a, b):
        self.service.do_work(a, b)


def email_formatter_service(container):
    def functor(name):
        return '{name}@{c.domain}'.format(name=name, c=container)
    return functor


class ContainerTest(unittest.TestCase):

    def setUp(self):
        self.container = Container()

    def test_registers_constants(self):
        self.container.name = 'spam'
        self.container.lastname = 'eggs'

        self.assertEqual(self.container.name, 'spam')
        self.assertEqual(self.container.lastname, 'eggs')

    def test_raises_error_when_getting_unregistered_values(self):
        with self.assertRaises(AttributeError):
            idontexist = self.container.idontexist

    def test_registers_variables(self):
        container = self.container
        container.setting = 'MyConfigSetting'
        container.service = lambda c: Service(c.setting)
        container.client = lambda c: Client(c.service)

        self.assertTrue(isinstance(container.service, Service))

        self.assertTrue(isinstance(container.client, Client))

        container.domain = 'example.com'
        container.email_formatter_service = email_formatter_service

        self.assertEqual('spam@example.com', container.email_formatter_service('spam'))


    def test_returns_different_instances_for_services_registed_as_non_constants(self):
        container = self.container
        container.service = lambda c: Service('dih')
        self.assertNotEqual(container.service, container.service)


    def test_returns_same_instance_for_services_registered_as_constants(self):
        container = self.container

        container.register('const1', 'c1', True)
        container.const2 = 'c2'
        self.assertEqual(container.const1, 'c1')
        self.assertEqual(container.const2, 'c2')


if __name__ == '__main__':
    unittest.main()
