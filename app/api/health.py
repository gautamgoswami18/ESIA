from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def home():

    return {
        "application": "ESIA",
        "status": "Running"
    }


@router.get("/health")
def health():

    return {
        "status": "Healthy"
    }