# Residential Elevator Pricing Optimization

该项目聚焦老旧小区加装电梯场景中的定价与补偿问题，尝试在居民支付意愿、楼层差异、公平性与项目成本回收之间建立可计算的平衡机制。
<img width="1285" height="547" alt="image" src="https://github.com/user-attachments/assets/db75d635-e095-4ddd-94a6-1a8f622afdcf" />

## Project Goals

- 设计分楼层收费方案
- 量化噪音、采光、房价变化等因素对补偿的影响
- 评估不同收费机制下的回本能力
- 为加装电梯决策提供可视化和定量依据

## Methods

- 线性规划
- 权重归一化与多因素加权
- 支付意愿建模
- 成本回收分析
- 敏感性可视化

## Repository Structure

- `code/`
  定价模型、权重模型与可视化脚本
- `problem/`
  题目材料
- `docs/`
  说明文档与辅助资料

## Key Scripts

- `code/question1.py`
  楼层收费优化模型
- `code/question2.py`
  年费与按次收费方案比较
- `code/price_weight.py`
  价格权重分析
- `code/noise_weight.py`
  噪音补偿权重分析
- `code/使用频率.py`
  使用频率分布可视化
- `code/que1vision.py`
  问题一结果展示
- `code/cika_vison.py`
  方案对比图形展示

## Data And Outputs

项目输出主要为价格方案、权重曲线、线性规划结果和辅助可视化图。整体结构适合用于展示从因素建模到方案生成的完整过程。

## Running

大部分脚本可独立运行，适合按问题逐个执行并生成对应图表。

## Main Dependencies

- `numpy`
- `scipy`
- `matplotlib`
- `pandas`
- `plotly`
