from .filesystem import ListFiles
from .selector import CrossJoinSelector
from .image import NoPreviewSaveImage

NODE_CLASS_MAPPINGS = {
    "ListFiles": ListFiles,
    "CrossJoinSelector": CrossJoinSelector,
    "NoPreviewSaveImage": NoPreviewSaveImage
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ListFiles": "List Files",
    "CrossJoinSelector": "Cross Join Selector",
    "NoPreviewSaveImage": "No Preview Save Image"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS'] 