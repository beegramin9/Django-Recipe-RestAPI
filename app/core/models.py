from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# settings.py에서 setting을 가져오는 recommmended way
from django.conf import settings
# Create your models here.
""" 쟝고의 default User 모델은 
아이디를 username으로 예상한다. 
그래서 여기 custom model을 만들고
(custom 모델 만든 후 settings.py에 내 custom 모델 추가해야 함
== 디펜던시 인젝션과 같이)
email로 customize를 해준 것 """

class UserManager(BaseUserManager):
    """ Manager 클래스는 helper functions(createUser, createSuperUser)들을 제공
    쟝고 ORM에서 사용될 수 있는 함수들을 customizing """
    def create_user(self, email, password=None, **extra_fields):
        # ES6와 같이, 다른 모든 것들을 extra_fields object(딕셔너리)에 넣는다.
        """ Creates and saves a new user  """
        if not email:
            raise ValueError('Users must have an email address.')

        # self.model = UserManager(따로 override안 했으니 사실은 BaseUserManager)의 model 객체. 
        # custom User Manager model overriding

        # the first part of an email is case sensitive, so normalizing an email will not change anything before the "@"
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # password encryption
        user.set_password(password)
        # db가 여러개 있을 때, db 선택하는 것
        user.save(using=self._db)

        return user

    # createSuperUser function: user가 CLI에서 만들어질 때 쟝고 CLI가 참고하는 함수
    # CLI에서 실제로 쓸 것이기 때문에 extra_fields 상관안해도 됨
    def create_superuser(self, email, password):
        """ Creates and saves a new super user """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        # user를 modify했으니 저장해야 함
        user.save(using=self._db)

        return user

# 내가 만든 custom User 모델 (속성만 가지고 있음. 메소드는 위 Manager 클래스가)
class User(AbstractBaseUser, PermissionsMixin):
    # AbstractBaseUser 은 쟝고의 기본 user 모델. 이제 override 할 것
    """ Custom user model that supports using email instead of username """
    # DB columns. 여기 models는 테이블이라고 생각하면 됨
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # 새로운 UserManager 객체 instantiation
    objects = UserManager()
    # username_field의 default값을 username을 email로 바꿈
    USERNAME_FIELD = 'email'

""" 새 모델 만들때마다 migration 커맨드 돌리고
admin.py에 model register 필요 """
class Tag(models.Model):
    """ Tag to be used for a recipe """
    name = models.CharField(max_length=255)
    # user foriegn key를 assign할건데
    # 바로 reference하지 않고 from django.conf import settings에서
    # settings.py의 auth user model을 refernce할 것

    user = models.ForeignKey(
        # foriegn key로 묶을 모델
        settings.AUTH_USER_MODEL,
        # foriegn key로 묶인 user를 지우면 어케할거?
        # CASCADE: Tag랑 같이 지워진다
        on_delete = models.CASCADE
    )

    # Optional
    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """ Ingredient to be used in a recipe """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """ Recipe object """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits = 5, decimal_places = 2)
    # best practice to set it Optional
    link = models.CharField(max_length=255, blank = True)

    # many to many
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title