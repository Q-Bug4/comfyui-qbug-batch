class CrossJoinSelector:
    # 使用全局字典存储所有实例的状态
    state_dict = {}
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "separator": ("STRING", {"default": ","}),
                "reset": ("BOOLEAN", {"default": False}),
                "input_1": ("STRING", {"forceInput": True}),
                "limit_1": ("INT", {"default": 0, "min": 0, "max": 999999}),
            },
            "optional": {
                "input_2": ("STRING", {"forceInput": True}),
                "limit_2": ("INT", {"default": 0, "min": 0, "max": 999999}),
                "input_3": ("STRING", {"forceInput": True}),
                "limit_3": ("INT", {"default": 0, "min": 0, "max": 999999}),
                "input_4": ("STRING", {"forceInput": True}),
                "limit_4": ("INT", {"default": 0, "min": 0, "max": 999999}),
                "input_5": ("STRING", {"forceInput": True}),
                "limit_5": ("INT", {"default": 0, "min": 0, "max": 999999}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("output_1", "output_2", "output_3", "output_4", "output_5")
    FUNCTION = "cross_join"
    CATEGORY = "selector"

    # 添加IS_CHANGED方法来禁用缓存
    @classmethod
    def IS_CHANGED(s, input_1, separator, reset, limit_1, input_2=None, limit_2=0, 
                   input_3=None, limit_3=0, input_4=None, limit_4=0, input_5=None, limit_5=0):
        import time
        return time.time()

    def _parse_inputs(self, input_1, separator, limit_1, input_2=None, limit_2=0, 
                     input_3=None, limit_3=0, input_4=None, limit_4=0, input_5=None, limit_5=0):
        """解析输入并返回有效的输入列表和限制"""
        inputs = []
        limits = []
        
        for inp, limit in [(input_1, limit_1), (input_2, limit_2), 
                          (input_3, limit_3), (input_4, limit_4), 
                          (input_5, limit_5)]:
            if not inp or not inp.strip():
                continue
                
            items = [item.strip() for item in inp.split(separator) if item.strip()]
            if not items:
                continue
                
            inputs.append(items)
            limits.append(limit)
            
        return inputs, limits

    def _get_current_outputs(self, inputs, indices, max_lengths):
        """根据当前索引生成输出"""
        outputs = [""] * 5
        for i, (input_list, idx) in enumerate(zip(inputs, indices)):
            outputs[i] = input_list[idx % max_lengths[i]]
        return outputs

    def _should_carry(self, level, indices, max_lengths, counts, limits):
        """判断是否需要进位
        
        Args:
            level: 当前层级
            indices: 各层级的当前索引
            max_lengths: 各层级的最大长度
            counts: 各层级的当前计数
            limits: 各层级的限制次数
            
        Returns:
            tuple: (need_carry, reset_current)
                - need_carry: 是否需要进位到上一层
                - reset_current: 是否需要重置当前层的索引
        """
        if level < 0:
            return False, False
            
        limit = limits[level]
        current_index = indices[level]
        current_count = counts[level]
        max_length = max_lengths[level]
        
        # 如果有限制
        if limit > 0:
            if current_count >= limit:
                # 达到限制次数，需要进位但不重置索引
                return True, False
        # 如果没有限制，检查是否超出长度
        elif current_index >= max_length:
            # 超出长度，需要进位且重置索引
            return True, True
            
        return False, False

    def _update_indices(self, inputs, limits, indices, counts):
        """更新索引和计数
        
        实现嵌套循环的进位逻辑：
        1. 内层到达限制或遍历完时进位到外层
        2. 根据情况重置内层的索引和计数
        3. 外层索引加1，计数加1
        
        Args:
            inputs: 输入列表的列表
            limits: 限制次数的列表
            indices: 当前索引的列表
            counts: 当前计数的列表
            
        Returns:
            tuple: (indices, counts) 更新后的索引和计数
        """
        if not indices:
            return indices, counts
            
        max_lengths = [len(input_list) for input_list in inputs]
        level = len(indices) - 1
        
        # 更新最内层的索引和计数
        indices[level] += 1
        counts[level] += 1
        
        # 从内到外处理进位
        while level >= 0:
            need_carry, reset_current = self._should_carry(
                level, indices, max_lengths, counts, limits
            )
            
            if need_carry:
                # 进位时总是重置计数，根据返回值决定是否重置索引
                counts[level] = 0
                if reset_current:
                    indices[level] = 0
                
                # 进位到上一层
                level -= 1
                if level >= 0:
                    indices[level] += 1
                    counts[level] += 1
            else:
                # 不需要进位，确保当前索引和计数在有效范围内
                indices[level] = indices[level] % max_lengths[level]
                if limits[level] > 0:
                    counts[level] = counts[level] % limits[level]
                break
                
        return indices, counts

    def _is_iteration_complete(self, indices, max_lengths, counts, limits):
        """检查是否所有层级都完成了遍历"""
        for i, (idx, max_len, count, limit) in enumerate(zip(indices, max_lengths, counts, limits)):
            if limit > 0:
                if count < limit:
                    return False
            else:
                if idx < max_len:
                    return False
        return True

    def cross_join(self, input_1, separator, reset=False, limit_1=0, 
                  input_2=None, limit_2=0, input_3=None, limit_3=0, 
                  input_4=None, limit_4=0, input_5=None, limit_5=0):
        # 解析输入
        inputs, limits = self._parse_inputs(input_1, separator, limit_1, input_2, limit_2, 
                                          input_3, limit_3, input_4, limit_4, input_5, limit_5)
        
        # 如果没有有效输入，返回空结果
        if not inputs:
            return ("", "", "", "", "")
            
        # 生成状态键并获取或初始化状态
        state_key = "|".join(f"{limit}:{','.join(input_list)}" for input_list, limit in zip(inputs, limits))
        
        if reset or state_key not in self.__class__.state_dict:
            self.__class__.state_dict[state_key] = {
                "indices": [0] * len(inputs),
                "counts": [0] * len(inputs)
            }
            
        # 获取当前状态
        state = self.__class__.state_dict[state_key]
        indices = state["indices"]
        counts = state["counts"]
        max_lengths = [len(input_list) for input_list in inputs]
        
        # 获取当前输出
        outputs = self._get_current_outputs(inputs, indices, max_lengths)
        
        # 更新状态
        indices, counts = self._update_indices(inputs, limits, indices, counts)
        
        # 检查是否需要重置
        if self._is_iteration_complete(indices, max_lengths, counts, limits):
            indices = [0] * len(inputs)
            counts = [0] * len(inputs)
            
        # 保存状态
        state["indices"] = indices
        state["counts"] = counts
        
        print(f"状态键: {state_key}, 当前索引: {indices}, 计数: {counts}, 输出: {outputs}")
        return tuple(outputs) 