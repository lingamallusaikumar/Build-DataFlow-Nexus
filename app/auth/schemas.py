class DummySchema:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def model_validate(cls, obj):
        return cls(**obj)

class UserRegistrationSchema(DummySchema):
    pass

class UserLoginSchema(DummySchema):
    pass

class MFASetupSchema(DummySchema):
    pass

class MFAVerifySchema(DummySchema):
    pass
