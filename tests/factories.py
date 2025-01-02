from datetime import datetime, timedelta
import random

from polyfactory import PostGenerated
from polyfactory.factories.pydantic_factory import ModelFactory

from app.application.posts.schemas import PostCreateSchema

AUTH_PASSWORD = 'test_password'


def _generate_numeric_string(*args, **kwargs) -> str:
    return str(random.randint(1, 1000))


def _generate_float_string(*args, **kwargs) -> str:
    random_float = random.uniform(1.0, 50.0)
    return f'{random_float:.2f}'


def _generate_iat(*args, **kwargs):
    return datetime.now().timestamp()


def _generate_exp(*args, **kwargs):
    delta_seconds = random.randint(1, 10000)
    new_exp = datetime.now() + timedelta(days=1) + timedelta(seconds=delta_seconds)
    return new_exp.timestamp()


class _MockDecodedTokenExample:
    iat: float = PostGenerated(_generate_iat)
    exp: float = PostGenerated(_generate_exp)


class PostCreationFactory(ModelFactory[PostCreateSchema]):
    __model__ = PostCreateSchema
