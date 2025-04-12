class CrossJoinSelector:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "list1": ("STRING", {"multiline": True}),
                "list2": ("STRING", {"multiline": True}),
                "separator": ("STRING", {"default": "\n"}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("combined_list",)
    FUNCTION = "cross_join"
    CATEGORY = "selector"

    def cross_join(self, list1, list2, separator):
        items1 = [item.strip() for item in list1.split(separator) if item.strip()]
        items2 = [item.strip() for item in list2.split(separator) if item.strip()]
        
        combined = []
        for item1 in items1:
            for item2 in items2:
                combined.append(f"{item1},{item2}")
        
        return (separator.join(combined),) 