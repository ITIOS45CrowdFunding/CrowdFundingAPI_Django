# generate token for user activation
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivationToken(PasswordResetTokenGenerator):
    def _generate_token(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"
    
activation_token=AccountActivationToken()
