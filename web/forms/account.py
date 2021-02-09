from django import forms
from web import models
from django.core.validators import RegexValidator


class RegisterModelForm(forms.ModelForm):
    mobile_phone = forms.CharField(
        label="手机号", validators=[RegexValidator(r"^(1|3|4|5|6|7|8|9)\d{9}$", "手机格式错误")]
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"placeholder": "请输入密码"}),
    )
    confirm = forms.CharField(
        label="重复密码",
        widget=forms.PasswordInput(attrs={"placeholder": "请再次输入密码"}),
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(attrs={"placeholder": "请输入验证码"}),
    )

    class Meta:
        model = models.UserInfo
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = "请输入%s" % (field.label)
