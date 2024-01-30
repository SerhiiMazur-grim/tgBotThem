from . import Base

from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    Boolean,
    ARRAY,
)


class SendPost(Base):
    __tablename__ = 'mailing'

    id = Column(Integer, primary_key=True, autoincrement=True)
    send_post = Column(Boolean, default=False)
    user_count = Column(Integer, default=0)
    user_list = Column(ARRAY(item_type=BigInteger, zero_indexes=True), default=[])
