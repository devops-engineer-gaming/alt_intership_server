"""create todo table

Revision ID: 47de46f187a3
Revises: 
Create Date: 2022-08-22 11:17:52.676197

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = '47de46f187a3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text("""
      CREATE TABLE IF NOT EXISTS public.todos
(
    title character varying COLLATE pg_catalog."default",
    description character varying COLLATE pg_catalog."default",
    id serial primary key NOT NULL 
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.todos
    OWNER to todoer;""")
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text(
        """
        DROP TABLE public.todos
        """
    ))
