from src.models import ReserveModel
from src.utils.repository import SqlAlchemyRepository


class ReserveRepository(SqlAlchemyRepository):
    model = ReserveModel


    