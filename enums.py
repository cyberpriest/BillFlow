from enum import Enum 


class Role(str,Enum):
    developer = 'dev'
    admin = 'admin'
    user = 'user'
    moderator = 'moderator'
    staff = 'staff'


class Plan(str,Enum):
    free = 'free'
    basic = 'basic'
    premium = 'premium'


class InvoiceStatus(str,Enum):
    draft  = 'draft'
    sent = 'sent'
    paid = 'paid'
    overdue = 'overdue'

