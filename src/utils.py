from templates.templates import ItemSearch, VehicleSearch
from .uconomy import Shop, Uconomy
from .user import User
from decimal import Decimal
from config.bot_config import register_reward, register_command, search_item_command, search_vehicle_command
from .exception import IllegalSteamIdError,BalanceNotEnoughError,IllegalCommandFormatError,ValueIsNegativeError
from graia.application.message.elements.internal import At,Plain
from graia.application.message.chain import MessageChain
from PIL import Image,ImageFont,ImageDraw
import os
from PIL import Image,ImageFont,ImageDraw

uconomy = Uconomy()
user = User()
shop = Shop()
ItemSearch = ItemSearch()
VehicleSearch = VehicleSearch()

def register(text: str,qid: str):
    steamid = text.replace(register_command,'').replace(' ','')
    if steamid.isdigit() and len(steamid) == 17:
        user.userInit(qid=qid,steamid=steamid)
        user_balance = uconomy.getUserBalance(steamid)
        uconomy.setUserBalance(steamid,user_balance + Decimal(register_reward))
    else:
        raise IllegalSteamIdError

def transfer(msgchain: MessageChain,qid: str):
    try:
        other_side_steamid = user.getSteamId(msgchain.get(At)[0].target)
        main_side_steamid = user.getSteamId(qid)
        transfer_balance = Decimal(int(msgchain.get(Plain)[1].text))
        if transfer_balance <= Decimal(0):
            raise ValueIsNegativeError
        else:
            if uconomy.getUserBalance(main_side_steamid) >= transfer_balance:
                uconomy.setUserBalance(main_side_steamid,uconomy.getUserBalance(main_side_steamid)-transfer_balance)
                uconomy.setUserBalance(other_side_steamid,uconomy.getUserBalance(other_side_steamid)+transfer_balance)
            else:
                raise BalanceNotEnoughError
    except IndexError:
        raise IllegalCommandFormatError

def item_search(text: str):
    itemname = text.replace(search_item_command,'').replace(' ','')
    return ItemSearch.templatesBuild(shop.searchShopItem(itemname))

def vehicle_search(text: str):
    vehiclename = text.replace(search_vehicle_command, '').replace(' ', '')
    return VehicleSearch.templatesBuild(shop.searchShopVehicle(vehiclename))
