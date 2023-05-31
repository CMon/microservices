from enum import Enum

class JWTAlgorithm(Enum):
    HS256 = "HS256"
    HS384 = "HS384"
    HS512 = "HS512"
    RS256 = "RS256"
    RS384 = "RS384"
    RS512 = "RS512"
    ES256 = "ES256"
    ES384 = "ES384"
    ES512 = "ES512"
    PS256 = "PS256"
    PS384 = "PS384"
    PS512 = "PS512"

class JwtEncryptionData(object):
    def __init__(self, algorithm: JWTAlgorithm, jwtPrivateOrSecret, jwtPublic = None):
        self.__algorithm = algorithm
        self.__privateOrSecret = jwtPrivateOrSecret

        if jwtPublic is not None:
            if algorithm == JWTAlgorithm.HS256 or algorithm == JWTAlgorithm.HS384 or algorithm == JWTAlgorithm.HS512:
                raise RuntimeError(f"You provided a public part but the given algorithm ({algorithm.value}) does not use it")
        else:
            if not (algorithm == JWTAlgorithm.HS256 or algorithm == JWTAlgorithm.HS384 or algorithm == JWTAlgorithm.HS512):
                raise RuntimeError(f"You selected an algorithm ({algorithm.value}) that needs a public part please provide one")
        self.__public = jwtPublic

    @property
    def algorithm(self):
        return self.__algorithm

    @algorithm.setter
    def algorithm(self, value):
        self.__algorithm = value

    @algorithm.deleter
    def algorithm(self):
        del self.__algorithm

    @property
    def privateOrSecret(self):
        return self.__privateOrSecret

    @privateOrSecret.setter
    def privateOrSecret(self, value):
        self.__privateOrSecret = value

    @privateOrSecret.deleter
    def privateOrSecret(self):
        del self.__privateOrSecret

    @property
    def public(self):
        return self.__public

    @public.setter
    def public(self, value):
        self.__public = value

    @public.deleter
    def public(self):
        del self.__public

    def __str__ (self):
        return f'JwtEncryptionData(algorithm={self.algorithm.value} ,privateOrSecret={self.privateOrSecret} ,public={self.public})'