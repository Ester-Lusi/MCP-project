import os
import zipfile
from typing import List


class FileService:
    def __init__(self, settings=None):
        self.settings = settings

    def scan_directory(self, directory: str, timeout_sec: int) -> dict:
        # סריקת התיקייה והחזרת נתונים על הקבצים
        file_metadata = []
        try:
            with os.scandir(directory) as it:
                for entry in it:
                    if entry.is_file():
                        file_metadata.append({
                            "filename": entry.name,
                            "size": entry.stat().st_size,
                            "last_modified": entry.stat().st_mtime
                        })
            return {"ok": True, "data": file_metadata}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def rename_files(self, directory: str, naming_scheme: str, timeout_sec: int) -> dict:
        # שינוי שם קבצים בתיקייה
        try:
            for entry in os.scandir(directory):
                if entry.is_file():
                    new_name = self.apply_naming_scheme(entry.name, naming_scheme)
                    os.rename(entry.path, os.path.join(directory, new_name))
            return {"ok": True, "message": "Files renamed successfully"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def apply_naming_scheme(self, filename: str, naming_scheme: str) -> str:
        # פיתוח לוגיקה ליצירת שם חדש
        return f"{naming_scheme}_{filename}"

    def move_files(self, source_directory: str, target_directory: str, timeout_sec: int) -> dict:
        # העברת קבצים לתיקייה אחרת
        try:
            if not os.path.exists(target_directory):
                os.makedirs(target_directory)

            for entry in os.scandir(source_directory):
                if entry.is_file():
                    os.rename(entry.path, os.path.join(target_directory, entry.name))
            return {"ok": True, "message": "Files moved successfully"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def create_archive(self, directory: str, archive_name: str, timeout_sec: int) -> dict:
        # יצירת ארכיב ZIP
        try:
            with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as archive:
                for entry in os.scandir(directory):
                    if entry.is_file():
                        archive.write(entry.path, arcname=entry.name)
            return {"ok": True, "message": f"Archive {archive_name} created successfully"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
