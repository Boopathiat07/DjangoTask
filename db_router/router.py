
class MasterSlaveRouter:
    def db_for_read(self, model, **hints):
        if model._meta.model_name == 'employee':
            return 'mongodb'
        return 'slave'

    def db_for_write(self, model, **hints):
        if model._meta.model_name == 'employee':
            return 'mongodb'
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        return False
       
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name == 'employee':
            return db == 'mongodb'
        return db == 'default'
