class CrossJoinSelector:
    # 使用全局字典存储所有实例的状态
    state_dict = {}
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_1": ("STRING", {"multiline": True}),
                "separator": ("STRING", {"default": "\n"}),
                "reset": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "input_2": ("STRING", {"multiline": True}),
                "input_3": ("STRING", {"multiline": True}),
                "input_4": ("STRING", {"multiline": True}),
                "input_5": ("STRING", {"multiline": True}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("output_1", "output_2", "output_3", "output_4", "output_5", "next_input")
    FUNCTION = "cross_join"
    CATEGORY = "selector"

    # 添加IS_CHANGED方法来禁用缓存
    @classmethod
    def IS_CHANGED(s, input_1, separator, reset, input_2=None, input_3=None, input_4=None, input_5=None):
        # 总是返回不同的值，强制ComfyUI重新计算节点
        import time
        return time.time()

    @staticmethod
    def get_state_key(inputs):
        """基于输入生成唯一的状态键"""
        key = ""
        for input_list in inputs:
            key += "||".join(input_list) + "|$|"
        return key

    def cross_join(self, input_1, separator, reset=False, input_2=None, input_3=None, input_4=None, input_5=None):
        # 收集所有非空输入
        inputs = []
        for inp in [input_1, input_2, input_3, input_4, input_5]:
            if inp is not None and inp.strip():
                items = [item.strip() for item in inp.split(separator) if item.strip()]
                if items:
                    inputs.append(items)
        
        # 如果没有输入，返回空结果
        if not inputs:
            return "", "", "", "", "", None
            
        # 为当前输入组合生成唯一的键
        state_key = self.get_state_key(inputs)
        
        # 如果需要重置或首次使用该组合，初始化状态
        if reset or state_key not in self.__class__.state_dict:
            self.__class__.state_dict[state_key] = {
                "indices": [0] * len(inputs),
                "max_lengths": [len(items) for items in inputs]
            }
        
        # 获取当前状态
        state = self.__class__.state_dict[state_key]
        indices = state["indices"]
        max_lengths = state["max_lengths"]
        
        # 准备输出
        outputs = [""] * 5
        
        # 获取当前索引对应的值
        for i in range(len(indices)):
            if i < len(inputs):
                idx = indices[i]
                if idx < len(inputs[i]):
                    outputs[i] = inputs[i][idx]
        
        # 更新索引（模拟嵌套循环）
        if indices:
            # 从最后一层开始尝试进位
            level = len(indices) - 1
            indices[level] += 1
            
            # 如果当前层级溢出，向上进位
            while level >= 0 and indices[level] >= max_lengths[level]:
                indices[level] = 0  # 当前层级归零
                level -= 1  # 移动到上一层级
                if level >= 0:
                    indices[level] += 1  # 上一层级加1
        
        # 保存更新后的状态
        state["indices"] = indices
        
        # 检查是否需要添加新的输入
        # 当所有索引都为0时，说明完成了一轮完整的循环
        next_input = ""
        if all(idx == 0 for idx in indices) and len(inputs) < 5:
            next_input = None
        
        print(f"状态键: {state_key}, 当前索引: {indices}, 输出: {outputs}, 下一个输入: {next_input}")
        return tuple(outputs + [next_input]) 