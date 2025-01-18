from pathlib import Path
import shutil

def upload_profile_image(file, upload_dir: str = "public/user-profile") -> bool:
    try:
        # Ensure the directory exists
        upload_path = Path(upload_dir)
        upload_path.mkdir(parents=True, exist_ok=True)

        # Save the file with its original name
        file_path = upload_path / file.filename
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        return True
    except Exception as e:
        # print(f"Error during file upload: {e}")
        return False
