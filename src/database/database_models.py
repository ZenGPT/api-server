import json
import os
from typing import Optional, Dict, Any
from datetime import timezone
from pynamodb.constants import NUMBER
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, NumberAttribute, Attribute, JSONAttribute, \
    VersionAttribute
from pynamodb.expressions.condition import Condition
from pynamodb.models import Model
from pynamodb.settings import OperationSettings
import datetime


class FloatAttribute(Attribute[float]):
    """
    Unlike NumberAttribute, this attribute has its type hinted as 'float'.
    """
    attr_type = NumberAttribute.attr_type
    serialize = NumberAttribute.serialize  # type: ignore
    deserialize = NumberAttribute.deserialize  # type: ignore


class IntAttribute(Attribute[int]):
    """
    A number attribute
    """
    attr_type = NUMBER

    def serialize(self, value):
        """
        Encode numbers as JSON
        """
        return json.dumps(value)

    def deserialize(self, value):
        """
        Decode numbers from JSON
        """
        return json.loads(value)


class GPTDockBaseModel(Model):
    class Meta:
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region = os.getenv("AWS_REGION")
        if os.getenv("DYNAMODB_HOST"):
            host = os.getenv("DYNAMODB_HOST")


class GPTDockClientData(GPTDockBaseModel):
    class Meta:
        table_name = "gpt_dock_client_data"

    client_id = UnicodeAttribute(hash_key=True)
    _updated_at = UTCDateTimeAttribute()
    token_quota = IntAttribute(default=0)
    max_quota = IntAttribute(default=0)
    config = JSONAttribute(null=True)
    version = VersionAttribute()

    def save(self,
             condition: Optional[Condition] = None,
             settings: OperationSettings = OperationSettings.default) -> Dict[str, Any]:
        self._updated_at = datetime.datetime.now(timezone.utc)
        return super().save(condition, settings)

    def __repr__(self):
        return f"GPTDockClientData(client_id='{self.client_id}', token_quota={self.token_quota})"

    def __str__(self):
        return self.__repr__()


class GPTDockUserData(GPTDockBaseModel):
    class Meta:
        table_name = "gpt_dock_user_data"

    user_id = UnicodeAttribute(hash_key=True)
    client_id = UnicodeAttribute(range_key=True)
    _updated_at = UTCDateTimeAttribute()
    token_used = IntAttribute(default=0)
    config = JSONAttribute(null=True)
    version = VersionAttribute()

    def save(self,
             condition: Optional[Condition] = None,
             settings: OperationSettings = OperationSettings.default) -> Dict[str, Any]:
        self._updated_at = datetime.datetime.now(timezone.utc)
        return super().save(condition, settings)

    def __repr__(self):
        return f"GPTDockUserData(user_id='{self.user_id}', client_id='{self.client_id}', token_quota={self.token_quota})"

    def __str__(self):
        return self.__repr__()
