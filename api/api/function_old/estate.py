from EstateModel.models import Estate,Estate_Type
from DepositoryModel.models import Depository
from CityModel.models import County,Suburb

#创建不动产
def create_estate(estate_type_id,uid,):
    #尝试获得
    type_of = Estate_Type.objects.get(pk=estate_type_id)