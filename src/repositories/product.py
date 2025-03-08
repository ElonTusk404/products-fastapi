from src.models import ProductModel
from src.utils.repository import SqlAlchemyRepository


class ProductRepository(SqlAlchemyRepository):
    model = ProductModel


    