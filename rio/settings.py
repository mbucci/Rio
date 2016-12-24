class Common(object):
	DEBUG = True
	JSON_AS_ASCII = False
	SQLALCHEMY_DATABASE_URI = 'mysql://root:Hugediablo!6@localhost:3306/rio?charset=utf8mb4'


class Local(Common):
	pass


class Development(Common):
	SQLALCHEMY_DATABASE_URI = 'mysql://mbucci:Hugediablo!6@rio-db.c8wwstsgstz6.us-east-1.rds.amazonaws.com:3306/rio_db?charset=utf8mb4'