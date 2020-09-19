
from .product import ProductConfig
from .develop import DevelopConfig

mod = 1

if mod == 1:
    config = DevelopConfig
else:
    config = ProductConfig
