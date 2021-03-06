from config.bot_config import mysql_uconomy_table, admin_qq
from .database import Database
from .exception import UserAlreadyHaveError, UserNotLoginError, UserNotFoundError


class User(Database):
    def checkUser(self, qid: str) -> bool:
        if self.executeWithCount(f"SELECT * FROM userinfo WHERE qid = '{qid}';") != 0:
            return True
        else:
            return False

    def userDatabaseInit(self):
        self.executeWithCommit(
            "CREATE TABLE IF NOT EXISTS `userinfo` (`qid` CHAR(12) NOT NULL,`steamId` CHAR(17) NOT NULL,`permission` TINYINT NOT NULL ) ENGINE=InnoDB DEFAULT CHARSET=utf8;")

    def checkUserLogin(self, steamid: str) -> bool:
        if self.executeWithCount(f"SELECT * FROM {mysql_uconomy_table} WHERE steamId = '{steamid}';") != 0:
            return True
        else:
            return False

    def userInit(self, qid: str, steamid: str):
        if not self.checkUser(qid):
            if self.checkUserLogin(steamid):
                self.executeWithCommit(
                    f"INSERT INTO userinfo (qid,steamId,permission) VALUE ('{qid}', '{steamid}', 0);")
                if int(qid) == admin_qq:
                    self.setUserPermission(qid, 2)
            else:
                raise UserNotLoginError
        else:
            raise UserAlreadyHaveError

    def getSteamId(self, qid: str) -> str:
        if self.checkUser(qid):
            return self.executeWithReturn(f"SELECT steamId FROM userinfo WHERE qid = '{qid}'")[0]['steamId']
        else:
            raise UserNotFoundError

    def checkUserPermission(self, qid: str, permission: int):
        if self.checkUser(qid):
            if int(self.executeWithReturn(f"SELECT permission FROM userinfo WHERE qid = '{qid}'")[0][
                       'permission']) >= permission:
                return True
            else:
                return False
        else:
            raise UserNotFoundError

    def setUserPermission(self, qid: str, permission: int):
        if self.checkUser(qid):
            self.executeWithCommit(f"UPDATE userinfo set permission = {str(permission)} WHERE qid = '{qid}'")
        else:
            raise UserNotFoundError
