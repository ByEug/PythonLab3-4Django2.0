from typing import List, Optional
import pytest
from django.contrib.auth.models import User, Group
from Shop.models import Brand, WayToUse, ImageSneakers, Sneakers, SneakersInstance
from django.core.files.uploadedfile import SimpleUploadedFile
import uuid


@pytest.fixture
def test_group(db) -> Group:
    group = Group.objects.create(name="test_group")
    return group


@pytest.fixture
def factory_for_users_from_test_group(db, test_group: Group):
    def create_test_group_user(
        username: str,
        password: Optional[str] = None,
        first_name: Optional[str] = "eugene",
        last_name: Optional[str] = "bylkov",
        email: Optional[str] = "bylkovevgen00@gmail.com",
        is_staff: str = False,
        is_superuser: str = False,
        is_active: str = True,
        groups: List[Group] = [],
    ) -> User:
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
        )
        user.groups.add(test_group)
        user.groups.add(*groups)
        return user
    return create_test_group_user


@pytest.fixture
def user_a(db, factory_for_users_from_test_group) -> User:
    return factory_for_users_from_test_group("A")


@pytest.fixture
def user_b(db, factory_for_users_from_test_group) -> User:
    return factory_for_users_from_test_group("B")


def test_should_create_user_in_app_user_group(
        user_a: User,
        test_group: Group,
) -> None:
    assert user_a.groups.filter(pk=test_group.pk).exists()


def test_should_create_two_users(user_a: User, user_b: User) -> None:
    assert user_a.pk != user_b.pk


def test_users_should_not_be_verified(user_a: User, user_b: User) -> None:
    assert user_a.shopuser.verified is False and user_b.shopuser.verified is False


@pytest.fixture
def brand(db) -> Brand:
    brand = Brand.objects.create(name="puma")
    return brand


def test_brand_is_exist(brand: Brand) -> None:
    assert brand.name is "puma"


@pytest.fixture
def way_to_use(db) -> WayToUse:
    way_to_use = WayToUse.objects.create(way="scateboarding")
    return way_to_use


def test_way_to_use_is_exist(way_to_use: WayToUse) -> None:
    assert way_to_use.way is "scateboarding"


@pytest.fixture
def image_sneakers(db) -> ImageSneakers:
    image_sneakers = ImageSneakers.objects.create(name="sneakers_puma", image=SimpleUploadedFile(name='adidas-harden-vol-4.jpeg',
        content=open('/home/eugene/PycharmProjects/lab_3_4_django/media/images/adidas-harden-vol-4.jpeg', 'rb').read(), content_type='image/jpeg'))
    return image_sneakers


def test_image_sneakers_is_exist(image_sneakers: ImageSneakers) -> None:
    assert ImageSneakers.objects.filter(pk=image_sneakers.pk).exists()


@pytest.fixture
def sneakers(db, brand: Brand, way_to_use: WayToUse) -> Sneakers:
    sneakers_buff = Sneakers.objects.create(sneakers_name="puma_sneakers", brand=brand)
    sneakers_buff.way_to_use.add(way_to_use)
    return sneakers_buff


def test_sneakers_is_exist(sneakers: Sneakers) -> None:
    assert Sneakers.objects.filter(pk=sneakers.pk).exists()


@pytest.fixture
def sneakers_instance(db, sneakers: Sneakers, image_sneakers: ImageSneakers) -> SneakersInstance:
    sneakers_instance = SneakersInstance(image=image_sneakers, Sneakers_info=sneakers, color="Black", amount="3", size="44")
    return sneakers_instance




