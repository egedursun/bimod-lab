from celery import shared_task

MODEL_OBJECT_CATEGORIES = (
    ('pth', 'PyTorch Model'),
)

@shared_task
def upload_model_to_ml_model_base(file_bytes: bytes, full_path: str):

    file_format = full_path.split('.')[-1]
    if file_format not in [file_type[0] for file_type in MODEL_OBJECT_CATEGORIES]:
        print(f"Invalid file format: {file_format}, skipping file...")
        return False

    try:
        with open(str("./"+full_path), "wb+") as file:
            file.write(file_bytes)
    except Exception as e:
        print(f"Error uploading file to storage: {e}")
        return False
    return True
