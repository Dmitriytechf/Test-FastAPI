from fastapi import APIRouter


router = APIRouter()

result_counter = 0

@router.get("/count", summary="Счетчик")
def get_count():
    global result_counter
    result_counter += 1
    return {'main_count': result_counter}