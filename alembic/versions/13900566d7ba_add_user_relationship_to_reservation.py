"""Add user relationship to Reservation

Revision ID: 13900566d7ba Revises: 87db95ee7123 Create Date: 2024-01-28
20:39:31.652056

1. Создаётся пустая таблица под другим именем. Структура таблицы повторяет
исходную, но с добавлением нового поля.
2. В новую таблицу копируются данные из исходной таблицы.
3. Исходная таблица удаляется.
4. Новой таблице присваивается имя исходной таблицы.

Всё это можно сделать при помощи batch-операций (групповых операций).

fk — обозначение внешнего ключа - Foreign Key;
reservation — таблица, для которой создается внешний ключ;
user_id — столбец, который содержит внешний ключ;
user — таблица, на которую ссылается внешний ключ."""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13900566d7ba'
down_revision: Union[str, None] = '87db95ee7123'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_reservation_user_id_user', 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.drop_constraint('fk_reservation_user_id_user', type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###