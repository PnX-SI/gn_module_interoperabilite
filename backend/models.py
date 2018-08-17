from flask import request
from sqlalchemy.sql import func
from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import serializable
from geonature.core.users.models import TRoles


@serializable
class Export(DB.Model):
    __tablename__ = 't_exports'
    __table_args__ = {'schema': 'gn_exports'}
    id = DB.Column(DB.Integer, primary_key=True, nullable=False)
    id_creator = DB.Column(DB.Integer, DB.ForeignKey(TRoles.id_role))
    role = DB.relationship('TRoles', foreign_keys=[id_creator], lazy='select')
    label = DB.Column(DB.Text, nullable=False, unique=True)
    schema_name = DB.Column(DB.Text, nullable=False)
    view_name = DB.Column(DB.Text, nullable=False)
    desc = DB.Column(DB.Text)
    created = DB.Column(DB.DateTime, default=func.now())
    updated = DB.Column(DB.DateTime, onupdate=func.now())
    deleted = DB.Column(DB.DateTime)

    def __init__(self, id_creator, label, schema_name, view_name, desc=None):
        self.id_creator = id_creator
        self.label = label
        self.schema_name = schema_name
        self.view_name = view_name
        self.desc = desc

    def __str__(self):
        return "<Export(id='{}', label='{}')>".format(self.id, self.label)

    __repr__ = __str__


# DONE: clearing policy ... 6 months as per cnil preconization
# https://www.cnil.fr/cnil-direct/attachement/501/517 fiche n°4
# TODO: Encrypt sensitive data
# https://www.cnil.fr/cnil-direct/attachement/501/517 fiche n°17
@serializable
class ExportLog(DB.Model):
    __tablename__ = 't_exports_logs'
    __table_args__ = {'schema': 'gn_exports'}
    id = DB.Column(DB.Integer, primary_key=True, nullable=False)
    id_export = DB.Column(DB.Integer(),
                          DB.ForeignKey('gn_exports.t_exports.id'))
    export = DB.relationship('Export', lazy='joined')
    format = DB.Column(DB.String(4), nullable=False)
    date = DB.Column(DB.DateTime, default=func.now())
    ip_addr_port = DB.Column(DB.String(51), nullable=False)  # ipv4 -> ipv6
    id_user = DB.Column(DB.Integer, DB.ForeignKey(TRoles.id_role))
    user = DB.relationship('TRoles', foreign_keys=[id_user], lazy='joined')

    @staticmethod
    def log(**kwargs):
        if 'X-Forwarded-For' in request.headers:
            remote_addr = request.headers.getlist('X-Forwarded-For')[0]\
                                         .rpartition(' ')[-1]
        elif request.environ.get('HTTP_X_REAL_IP', None):
            remote_addr = request.environ.get('HTTP_X_REAL_IP')
        else:
            remote_addr = request.remote_addr

        remote_addr_port = ':'.join(
            [remote_addr, str(request.environ.get('REMOTE_PORT'))])
        kwargs['ip_addr_port'] = remote_addr_port
        try:
            x = ExportLog(**kwargs)
            DB.session.add(x)
            DB.session.flush()
        except Exception as e:
            DB.session.rollback()
            raise e('Echec de journalisation.')
