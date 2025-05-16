import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache

def generate_verification_code(length=6):
    """生成指定长度的数字验证码"""
    return ''.join(random.choices(string.digits, k=length))

def send_verification_email(email, code):
    """发送验证码邮件"""
    subject = '博客注册验证码'
    message = f'您的验证码是：{code}，有效期为10分钟，请勿将验证码泄露给他人。'
    html_message = f'''
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 5px; background-color: #f9f9f9;">
        <h2 style="color: #333; border-bottom: 1px solid #ddd; padding-bottom: 10px;">博客注册验证码</h2>
        <p style="color: #555; line-height: 1.6;">尊敬的用户：</p>
        <p style="color: #555; line-height: 1.6;">您好！感谢您注册我们的博客系统。</p>
        <p style="color: #555; line-height: 1.6;">您的验证码是：</p>
        <div style="background-color: #fff; border: 1px dashed #ccc; padding: 15px; text-align: center; margin: 15px 0; border-radius: 4px;">
            <span style="font-size: 24px; font-weight: bold; letter-spacing: 5px; color: #3498db;">{code}</span>
        </div>
        <p style="color: #555; line-height: 1.6;">此验证码有效期为<strong>10分钟</strong>，请及时完成注册。</p>
        <p style="color: #555; line-height: 1.6;">请勿将验证码泄露给他人，如非本人操作，请忽略此邮件。</p>
        <div style="margin-top: 30px; padding-top: 15px; border-top: 1px solid #ddd; text-align: center; color: #777; font-size: 12px;">
            <p>&copy; 个人博客系统 - 这是一封自动发送的邮件，请勿回复。</p>
        </div>
    </div>
    '''
    
    # 发送邮件
    return send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        html_message=html_message,
        fail_silently=False,
    )

def save_verification_code(email, code, timeout=600):
    """保存验证码到缓存中，默认10分钟有效期"""
    cache_key = f'email_verification_{email}'
    cache.set(cache_key, code, timeout)

def verify_code(email, code):
    """验证用户输入的验证码是否正确"""
    cache_key = f'email_verification_{email}'
    stored_code = cache.get(cache_key)
    
    if not stored_code:
        return False  # 验证码已过期或不存在
    
    # 验证通过后删除验证码
    if stored_code == code:
        cache.delete(cache_key)
        return True
    
    return False 