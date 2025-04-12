import os
import folder_paths
from comfy.model_management import get_torch_device

class ListFiles:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "directory": ("STRING", {"default": ""}),
                "file_types": ("STRING", {"default": "*.png,*.jpg,*.jpeg,*.webp"}),
                "recursive": ("BOOLEAN", {"default": False}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_list",)
    FUNCTION = "list_files"
    CATEGORY = "filesystem"

    def list_files(self, directory, file_types, recursive):
        if not directory:
            directory = folder_paths.get_input_directory()
        
        file_types = [ft.strip() for ft in file_types.split(",")]
        files = []
        
        if recursive:
            for root, _, filenames in os.walk(directory):
                for filename in filenames:
                    if any(filename.lower().endswith(ft.replace("*", "")) for ft in file_types):
                        files.append(os.path.join(root, filename))
        else:
            for filename in os.listdir(directory):
                if any(filename.lower().endswith(ft.replace("*", "")) for ft in file_types):
                    files.append(os.path.join(directory, filename))
        
        return ("\n".join(files),) 