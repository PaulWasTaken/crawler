import sqlalchemy as sa

from re import sub
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from sqlalchemy.util.langhelpers import public_factory


class Replace(expression.Insert):
    pass


sa.replace = public_factory(Replace, ".expression.replace")


@compiles(Replace, 'sqlite')
def compile_replace(replace, compiler, **kw):
    stmt = compiler.sql_compiler.visit_insert(replace)
    return sub(r'^INSERT', 'INSERT OR REPLACE', stmt)
