

class Base:
	SECRET_KEY = "JEKJKljkj3948kjd892d9j0co"
	SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
	BASE = "https://localhost"

	# If BASE is https these has to be specified
	SERVER_CERT = "certs/server.crt"
	SERVER_KEY = "certs/server.key"
	CA_BUNDLE = None
	OIDC_CLIENT_SECRETS = "client_secrets.json"
	OIDC_INTROSPECTION_AUTH_METHOD = "bearer"
	OIDC_SCOPES = ['openid', 'email', 'address']
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	VERIFY_SSL = False


class Production(Base):
	pass


class Testing(Base):
	pass


class Development(Base):
	pass
