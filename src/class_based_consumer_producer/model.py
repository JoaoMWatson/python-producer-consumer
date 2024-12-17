from enum import Enum


class ServiceTree(object):
    """Classe modelo para schema service-tree"""

    def __init__(
        self,
        system: str,
        businessKey: str,
        description: str,
        portalList: list[str],
        serviceTypeList: list[enumerate],
        academicLevelList: list[enumerate],
        createdAt: int,
        overdueStudentAccepted: bool,
    ):
        """
        Inicializa a classe ServiceTree com atributos:
        Args:
            system (str): sistema que produziu a mensagem
            businessKey (str): chave de negócio
            description (str): descrição do serviço
            portalList (list[str]): lista de portais
            serviceTypeList (list[enumerate]): lista de enum de serviço
            academicLevelList (list[enumerate]): lista de enum de nível acadêmico
            createdAt (int): data de criação
            overdueStudentAccepted (bool): aceita alunos inadimplentes
        """
        self.system: str = system
        self.businessKey: str = businessKey
        self.description: str = description
        self.portalList: list[str] = portalList
        self.serviceTypeList: list[enumerate] = serviceTypeList
        self.academicLevelList: list[enumerate] = academicLevelList
        self.createdAt: int = createdAt
        self.overdueStudentAccepted: bool = overdueStudentAccepted

    def to_dict(self):
        """Converte a classe para um dicionário"""
        return dict(
            system=self.system,
            businessKey=self.businessKey,
            description=self.description,
            portalList=self.portalList,
            serviceTypeList=self.serviceTypeList,
            academicLevelList=self.academicLevelList,
            createdAt=self.createdAt,
            overdueStudentAccepted=self.overdueStudentAccepted,
        )
