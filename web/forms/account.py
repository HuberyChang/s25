from django import forms
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from utils.tencent.sms import send_sms_single, send_sms_mutil
import random
from utils import encrypt
from django_redis import get_redis_connection


class RegisterModelForm(forms.ModelForm):

    password = forms.CharField(
        label="密码",
        min_length=8,
        max_length=64,
        error_messages={
            "min_length": "密码长度不能小于8个字符",
            "max_length": "密码长度不能多于64个字符",
        },
        widget=forms.PasswordInput(attrs={"placeholder": "请输入密码"}),
    )

    confirm_password = forms.CharField(
        label="重复密码",
        min_length=8,
        max_length=64,
        error_messages={
            "min_length": "重复密码长度不能小于8个字符",
            "max_length": "重复密码长度不能多于64个字符",
        },
        widget=forms.PasswordInput(attrs={"placeholder": "请再次输入密码"}),
    )

    mobile_phone = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r"^(1[3|4|5|6|7|8|9])\d{9}$", "手机格式错误!!")],
    )

    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(attrs={"placeholder": "请输入验证码"}),
    )

    class Meta:
        model = models.UserInfo
        # fields = "__all__"
        fields = [
            "username",
            "email",
            "password",
            "confirm_password",
            "mobile_phone",
            "code",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = "请输入%s" % (field.label,)

    # 钩子函数，做数据校验
    def clean_username(self):
        username = self.cleaned_data["username"]

        exists = models.UserInfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError("用户名已存在")

        return username

    def clean_email(self):
        email = self.cleaned_data["email"]

        exists = models.UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError("邮箱已存在")

        return email

    def clean_password(self):
        pwd = self.cleaned_data["password"]

        # 加密&返回
        return encrypt.md5(pwd)

    def clean_confirm_password(self):
        # self.cleaned_data  已验证的所有字段里边的数据,
        # form里边 password在confirm_password前边验证，所以这个地方可以校验password
        # pwd = self.cleaned_data["password"]
        pwd = self.cleaned_data.get("password")
        confirm_pwd = encrypt.md5(self.cleaned_data["confirm_password"])

        if pwd != confirm_pwd:
            raise ValidationError("两次密码不一致")

        return confirm_pwd

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data["mobile_phone"]

        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError("手机号已经注册")

        return mobile_phone

    def clean_code(self):
        code = self.cleaned_data["code"]
        # mobile_phone = self.cleaned_data["mobile_phone"]
        # 需要先做判断，判断是否已经校验通过
        mobile_phone = self.cleaned_data.get("mobile_phone")
        if not mobile_phone:
            return code

        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)
        if not redis_code:
            raise ValidationError("验证码失效或者未发送，请重新发送")

        redis_str_code = redis_code.decode("utf-8")
        # 输入的验证码带空格也要通过
        if code.strip() != redis_str_code.strip():
            raise ValidationError("验证码错误，请重新输入")

        return code


class SendSmsForm(forms.Form):
    mobile_phone = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r"^(1[3|4|5|6|7|8|9])\d{9}$", "手机格式错误!")],
    )
    """
        在form或者modelform中想要使用视图函数中的一些参数或者一些值，可以重写__init__函数，把想要的参数或者值传进来
        比如这里的request参数
    """

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_mobile_phone(self):
        # 手机号校验钩子
        mobile_phone = self.cleaned_data["mobile_phone"]

        # 判断短信模板是否有问题
        tpl = self.request.GET.get("tpl")
        template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
        if not template_id:
            raise ValidationError("短信模板错误")

        # 校验数据库是否有这个手机号
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if tpl == "login":
            if not exists:
                raise ValidationError("手机号不存在")
        else:
            if exists:
                raise ValidationError("手机号已经存在")
        # 发短信 & 写入redis
        code = random.randrange(1000, 9999)

        # 发短信
        sms = send_sms_single(
            mobile_phone,
            template_id,
            [
                code,
            ],
        )
        if sms["result"] != 0:
            raise ValidationError("短信发送失败，{}".format(sms["errmsg"]))

        # 验证码写入redis
        conn = get_redis_connection()
        conn.set(mobile_phone, code, ex=60)

        return mobile_phone
