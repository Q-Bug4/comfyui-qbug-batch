# QBug-Batch: ComfyUI 自定义节点

一个用于 ComfyUI 的实用节点集合，用于批量处理和工作流自动化。

[English Documentation](README.md)

## 项目愿景

QBug-Batch 旨在解决 ComfyUI 工作流中的批量处理挑战。我们的愿景是帮助用户：

- 通过组合不同的场景、人物和参数，高效地生成多个输出
- 减少在为每个变体手动调整工作流上花费的时间
- 自动化原本需要多次手动干预的重复任务
- 通过允许系统性地探索参数组合来提高生产力

通过提供专门用于批处理操作的节点，我们帮助 ComfyUI 用户节省时间，并专注于创意方面而非技术调整。

## 快速开始
请将下列示例工作流导入到Comfyui中进行使用
- [crossjoin-example](example/crossjoin-example.json)

## 节点

### ListFiles（列出文件）

一个从目录中列出文件的节点，具有可选的排序和过滤功能。该节点输出逗号分隔的文件列表，可供其他节点使用。

**功能特点：**
- 列出指定目录中的所有文件
- 支持文件扩展名过滤
- 支持按字母顺序和日期排序
- 将文件作为逗号分隔的字符串输出

### CrossJoinSelector（交叉连接选择器）

一个强大的选择器节点，实现了嵌套循环行为，用于遍历多个输入。

**功能特点：**
- 支持最多5个输入列表
- 模拟嵌套循环行为
- 每个输入都有一个可选的限制参数来控制迭代次数
- 在执行之间维持状态
- 非常适合处理参数组合的批量处理

**使用示例：**
```
input_1: "pic1,pic2,pic3"
limit_1: 0（无限制）
input_2: "1,2,3,4,5,6,7,8,9,10"
limit_2: 3
```

此配置将迭代 input_1 中的所有项目，对于每个项目，将遍历 input_2 中的3个项目，然后再移动到 input_1 的下一个项目。

### NoPreviewSaveImage（无预览保存图像）

一个保存图像而不显示预览的节点，适用于批量处理。

## 安装
### Custom Nodes Manager
在Custom Nodes Manager中搜索qbug-batch进行安装

### 仓库克隆
1. 将此仓库克隆到您的 ComfyUI custom_nodes 目录中：
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/your-username/qbug-batch.git
```
## 节点参数详细说明

### ListFiles（列出文件）

**输入参数：**
- `directory`：要列出文件的目录路径。如果为空，则使用ComfyUI的默认输入目录。
- `file_types`：要筛选的文件类型，以逗号分隔（例如：`*.png,*.jpg,*.jpeg,*.webp`）。
- `recursive`：是否递归搜索子目录（布尔值）。
- `sort_by`：文件排序方式，可选值：
  - `name`：按文件名排序
  - `size`：按文件大小排序
  - `modified_time`：按修改时间排序
- `sort_order`：排序顺序，可选值：
  - `asc`：升序
  - `desc`：降序
- `separator`：输出文件列表中的分隔符，默认为逗号。

**输出：**
- `file_list`：以指定分隔符连接的文件全路径字符串。

### CrossJoinSelector（交叉连接选择器）

**输入参数：**
- `separator`：输入列表中的分隔符，用于拆分字符串为项目列表。
- `reset`：是否重置迭代状态（布尔值）。
- `input_n`：第n个输入列表（必需）。
- `limit_n`：第n个输入的迭代限制（0表示无限制）。

**输出：**
- `output_n`：当前迭代中第n个输入的选中项。

### NoPreviewSaveImage（无预览保存图像）

**输入参数：**
- `images`：要保存的图像。
- `filename_prefix`：保存文件的前缀名称，默认为"ComfyUI"。
- `save_metadata`：是否保存元数据到PNG文件（布尔值）。

**输出：**
- 无返回值，但会将图像保存到ComfyUI的输出目录中。
- 保存的文件将使用格式：`{filename_prefix}_{counter:05}_.png`。


## 使用场景

- **人物生成**：组合不同的人物与各种背景、姿势或风格
- **风格探索**：在多种艺术风格或参数中测试单个图像
- **模型评估**：在不同模型上运行相同的提示词以比较结果
- **参数调优**：系统地探索不同的参数组合以找到最佳设置

## 许可证

MIT 许可证 