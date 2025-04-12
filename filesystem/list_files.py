import os
import folder_paths
from comfy.model_management import get_torch_device

class ListFiles:
    SORT_BY_OPTIONS = ["name", "size", "modified_time"]
    SORT_ORDER_OPTIONS = ["asc", "desc"]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "directory": ("STRING", {"default": ""}),
                "file_types": ("STRING", {"default": "*.png,*.jpg,*.jpeg,*.webp"}),
                "recursive": ("BOOLEAN", {"default": False}),
                "sort_by": (s.SORT_BY_OPTIONS, {"default": "name"}),
                "sort_order": (s.SORT_ORDER_OPTIONS, {"default": "asc"}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_list",)
    FUNCTION = "list_files"
    CATEGORY = "filesystem"

    def list_files(self, directory, file_types, recursive, sort_by, sort_order):
        if not directory:
            directory = folder_paths.get_input_directory()
        
        file_types = [ft.strip() for ft in file_types.split(",")]
        files = []
        
        if recursive:
            for root, _, filenames in os.walk(directory):
                for filename in filenames:
                    if any(filename.lower().endswith(ft.replace("*", "")) for ft in file_types):
                        full_path = os.path.join(root, filename)
                        files.append(full_path)
        else:
            for filename in os.listdir(directory):
                if any(filename.lower().endswith(ft.replace("*", "")) for ft in file_types):
                    full_path = os.path.join(directory, filename)
                    files.append(full_path)

        # Sort files based on user selection and sort order
        reverse = sort_order == "desc"
        if sort_by == "name":
            files.sort(key=lambda x: os.path.basename(x).lower(), reverse=reverse)
        elif sort_by == "size":
            files.sort(key=lambda x: os.path.getsize(x), reverse=reverse)
        elif sort_by == "modified_time":
            files.sort(key=lambda x: os.path.getmtime(x), reverse=reverse)
        
        return ("\n".join(files),) 