import pytest


@pytest.fixture
def configurable_email(db):
    from mailmate.templates import ConfigurableEmail

    our_email = ConfigurableEmail(
        from_email='no-reply@face.net',
        to=['blah-a@gmail.com', 'blah-b@gmail.com'],
        subject='%s has a reply about this',
        template_name='body.txt',
        html_template_name='body.html',
    )

    return our_email


@pytest.fixture
def AwesomeMessage():
    from mailmate.templates import ConfigurableEmail

    class AwesomeMessage(ConfigurableEmail):
        from_email = 'no-reply@face.net'
        to = ['blah-a@gmail.com', 'blah-b@gmail.com']
        subject = '%s has a reply about this'
        template_name = 'body.txt'
        html_template_name = 'body.html'

    return AwesomeMessage


@pytest.fixture
def UserFriendlyMessage():
    from mailmate.templates import ConfigurableEmail

    class UserFriendlyMessage(ConfigurableEmail):
        from_email = 'no-reply@face.net'
        to = ['blah-a@gmail.com', 'blah-b@gmail.com']
        subject = '%s has a reply about this'
        template_name = 'body.txt'
        html_template_name = 'body.html'
        email_name = 'Super Awesome Message'

    return UserFriendlyMessage


@pytest.mark.django_db
def test_user_friendly_message(UserFriendlyMessage):
    UserFriendlyMessage()

    from mailmate.models import Email
    assert Email.objects.get(email_name='Super Awesome Message')

@pytest.fixture
def configureable_message(db, AwesomeMessage):
    return AwesomeMessage()


@pytest.mark.django_db
def test_message_customization(configureable_message, AwesomeMessage):

    assert configureable_message.subject == '%s has a reply about this'
    assert configureable_message.storage.receivers.count() == 2

    from mailmate.models import Email
    awesome_message = Email.objects.get(email_name='AwesomeMessage')
    awesome_message.subject = 'It cherged ermegerd'
    awesome_message.save()

    awesome_message.receivers.create(
        address='test@example.com'
    )

    message = AwesomeMessage()
    assert message.subject == 'It cherged ermegerd'
    assert message.storage.receivers.count() == 3
    assert message.to == [
        'blah-a@gmail.com',
        'blah-b@gmail.com',
        'test@example.com'
    ]


@pytest.mark.django_db
def test_passable_to_arguments(AwesomeMessage):
    message = AwesomeMessage(to=['something-else@gmail.com'])
    assert message.to == ['something-else@gmail.com']
    assert AwesomeMessage().to == ['blah-a@gmail.com', 'blah-b@gmail.com']


@pytest.mark.django_db
def test_passable_from_email_arguments(AwesomeMessage):
    message = AwesomeMessage(from_email='something-else@gmail.com')
    assert message.from_email == 'something-else@gmail.com'
    assert AwesomeMessage().from_email == 'no-reply@face.net'


@pytest.mark.django_db
def test_passable_subject_arguments(AwesomeMessage):
    message = AwesomeMessage(subject='Change of Subject')
    assert message.subject == 'Change of Subject'
    assert AwesomeMessage().subject == '%s has a reply about this'


def test_reusable_created(configurable_email):
    assert configurable_email.created


def test_email_to_saved(configurable_email):
    assert configurable_email.storage.receivers.count() == 2
    assert configurable_email.to == ['blah-a@gmail.com', 'blah-b@gmail.com']