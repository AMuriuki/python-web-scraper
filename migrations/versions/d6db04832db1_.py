"""empty message

Revision ID: d6db04832db1
Revises: 
Create Date: 2020-11-10 07:30:49.929703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6db04832db1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vehicle3rdlevelsubsystem', schema=None) as batch_op:
        batch_op.create_foreign_key(batch_op.f('fk_vehicle3rdlevelsubsystem_specification_id_vehiclespecification'), 'vehiclespecification', ['specification_id'], ['id'])

    with op.batch_alter_table('vehiclepart', schema=None) as batch_op:
        batch_op.add_column(sa.Column('specification_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_vehiclepart_specification_id_vehiclespecification'), 'vehiclespecification', ['specification_id'], ['id'])

    with op.batch_alter_table('vehiclesecondlevelsubsystem', schema=None) as batch_op:
        batch_op.add_column(sa.Column('specification_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_vehiclesecondlevelsubsystem_specification_id_vehiclespecification'), 'vehiclespecification', ['specification_id'], ['id'])

    with op.batch_alter_table('vehiclesubsystem', schema=None) as batch_op:
        batch_op.add_column(sa.Column('specification_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_vehiclesubsystem_specification_id_vehiclespecification'), 'vehiclespecification', ['specification_id'], ['id'])

    with op.batch_alter_table('vehiclesystem', schema=None) as batch_op:
        batch_op.add_column(sa.Column('specification_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_vehiclesystem_specification_id_vehiclespecification'), 'vehiclespecification', ['specification_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vehiclesystem', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_vehiclesystem_specification_id_vehiclespecification'), type_='foreignkey')
        batch_op.drop_column('specification_id')

    with op.batch_alter_table('vehiclesubsystem', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_vehiclesubsystem_specification_id_vehiclespecification'), type_='foreignkey')
        batch_op.drop_column('specification_id')

    with op.batch_alter_table('vehiclesecondlevelsubsystem', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_vehiclesecondlevelsubsystem_specification_id_vehiclespecification'), type_='foreignkey')
        batch_op.drop_column('specification_id')

    with op.batch_alter_table('vehiclepart', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_vehiclepart_specification_id_vehiclespecification'), type_='foreignkey')
        batch_op.drop_column('specification_id')

    with op.batch_alter_table('vehicle3rdlevelsubsystem', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_vehicle3rdlevelsubsystem_specification_id_vehiclespecification'), type_='foreignkey')

    # ### end Alembic commands ###