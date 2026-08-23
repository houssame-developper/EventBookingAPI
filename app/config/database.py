from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from config.settings import DATABASE_URL
from typing import AsyncGenerator


# Configuration corrigée et optimisée
engine = create_async_engine(
    DATABASE_URL,
    echo=True,           # Active le log de toutes les requêtes SQL générées
    pool_size=5,         # Nombre maximal de connexions persistantes à maintenir (par défaut: 5)
    max_overflow=10,     # Nombre de connexions temporaires autorisées au-delà de pool_size
    pool_pre_ping=True   # Teste la santé de la connexion avant chaque exécution (évite les déconnexions)
)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,  # Optionnel car activé par défaut avec async_sessionmaker
    expire_on_commit=False  # Recommandé en async pour éviter des requêtes implicites bloquantes
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session

        except Exception:
            await session.rollback()  
            raise
        finally:
            await session.close()