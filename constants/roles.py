class UserRole:
    ADMIN = "administrator"
    CUSTOMER = "customer"
    STAFF = "staff"
    ENGINEER = "engineer"
    SUPERVISOR = "supervisor"

    ALL = [
        ADMIN,
        CUSTOMER,
        STAFF,
        ENGINEER,
        SUPERVISOR
    ]

    STAFF_ROLES = [
        STAFF,
        ENGINEER,
        SUPERVISOR
    ]

    @classmethod
    def is_valid(cls, role):
        return role in cls.ALL

    @classmethod
    def is_staff_role(cls, role):
        return role in cls.STAFF_ROLES