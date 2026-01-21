from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Менеджер жизненного цикла приложения.
    Выполняется при старте и остановке сервера.
    """
    from te_fast.core.database import init_db, close_db
  
    # Startup - выполняется при запуске сервера
    print("Starting FastAPI application...")

    try:
        await init_db()
        print("Database initialized successfully")
        
        app.state.db_initialized = True
        app.state.startup_time = asyncio.get_event_loop().time()
        
    except Exception as e:
        print(f"Error during startup: {e}")
        raise
    
    # Здесь приложение работает и обрабатывает запросы
    yield
    # Shutdown - выполняется ПРИ ОСТАНОВКЕ сервера
    print("Stopping FastAPI application...")
    
    try:
        # Закрываем соединения с БД
        await close_db()
        
        print("Application stopped gracefully")
        
    except Exception as e:
        print(f"Error during shutdown: {e}")
