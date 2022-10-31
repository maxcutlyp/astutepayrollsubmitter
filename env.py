USER_ID = 'max.cutlyp'
APPROVER_USER_ID = 'matt.bradbury'
MID = '43555'
UID = '43564'
DOMAIN = 'megt.astutepayroll.com'
LOGIN_PATH = '/megt/auth/login'
SUBMIT_PATH = '/megt/attendance/manage/'

TIMES = [
    # start, finish, break
    ('7:30am','4:00pm','60'), # Monday
    ('7:30am','4:00pm','60'), # Tuesday
    ('7:30am','4:00pm','60'), # Wednesday
    ('7:30am','4:00pm','60'), # Thursday
    ('7:30am','4:00pm','30'), # Friday
    (None,None,None),         # Saturday - not supported yet
    (None,None,None),         # Sunday - not supported yet
]
