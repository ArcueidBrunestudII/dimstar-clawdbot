"""
数学建模示例：城市交通流量优化问题（简化版）
目标：优化信号灯配时，最小化车辆等待时间
方法：统计分析 + 简单优化 + 可视化
"""

import random
import math
import statistics
from datetime import datetime

class SimpleTrafficOptimization:
    def __init__(self):
        self.generate_data()
        self.setup_optimization()
    
    def generate_data(self):
        """生成模拟的交通流量数据"""
        random.seed(42)
        
        # 生成24小时交通流量数据
        hours = list(range(24))
        # 模拟早晚高峰
        self.traffic_flow = []
        for hour in hours:
            # 基础流量 + 高峰调整 + 随机噪声
            base = 50 + 30 * math.sin(2 * math.pi * (hour - 6) / 24)
            noise = random.gauss(0, 10)
            flow = max(base + noise, 10)  # 确保不为负数
            self.traffic_flow.append(flow)
        
        # 生成路口数据
        self.intersections = ['A', 'B', 'C', 'D', 'E']
        self.intersection_data = {}
        
        for intersection in self.intersections:
            north_south = random.randint(100, 500)
            east_west = random.randint(80, 400)
            capacity = random.randint(800, 1500)
            current_cycle = random.randint(60, 120)
            
            self.intersection_data[intersection] = {
                'north_south': north_south,
                'east_west': east_west,
                'capacity': capacity,
                'current_cycle': current_cycle
            }
        
        print("=== 数据生成完成 ===")
        print(f"交通流量范围: {min(self.traffic_flow):.1f} - {max(self.traffic_flow):.1f} 辆/小时")
        print("路口数据:")
        for intersection, data in self.intersection_data.items():
            print(f"  {intersection}: NS={data['north_south']}, EW={data['east_west']}, "
                  f"周期={data['current_cycle']}秒")
    
    def setup_optimization(self):
        """设置优化问题"""
        print("\n=== 优化模型设置 ===")
        
        # 目标函数系数（等待时间系数）
        self.c = []
        for intersection in self.intersections:
            data = self.intersection_data[intersection]
            coefficient = data['north_south'] + data['east_west']
            self.c.append(coefficient)
        
        print(f"目标函数系数: {self.c}")
    
    def simple_optimization(self):
        """简单优化算法"""
        print("\n=== 开始求解优化问题 ===")
        
        n_intersections = len(self.intersections)
        optimal_cycles = []
        
        for i, intersection in enumerate(self.intersections):
            data = self.intersection_data[intersection]
            current_cycle = data['current_cycle']
            
            # 简单优化：基于流量比例调整周期
            traffic_factor = (data['north_south'] + data['east_west']) / 1000
            # 约束在60-180秒之间
            new_cycle = max(60, min(180, current_cycle * (1 + traffic_factor)))
            optimal_cycles.append(new_cycle)
        
        # 计算等待时间
        current_waiting = []
        optimal_waiting = []
        
        for i, intersection in enumerate(self.intersections):
            data = self.intersection_data[intersection]
            current_w = data['north_south'] + data['east_west']
            optimal_w = current_w * (optimal_cycles[i] / data['current_cycle'])
            
            current_waiting.append(current_w)
            optimal_waiting.append(optimal_w)
        
        total_current = sum(current_waiting)
        total_optimal = sum(optimal_waiting)
        improvement = total_current - total_optimal
        improvement_rate = improvement / total_current * 100
        
        print(f"✅ 优化完成!")
        print(f"最小总等待时间: {total_optimal:.2f}")
        print(f"优化前后对比:")
        print(f"  当前总等待时间: {total_current:.2f}")
        print(f"  优化后总等待时间: {total_optimal:.2f}")
        print(f"  总体改进: {improvement_rate:.2f}%")
        print(f"  节省等待时间: {improvement:.2f}")
        
        print("\n各路口最优信号灯周期:")
        for i, intersection in enumerate(self.intersections):
            print(f"  {intersection}: {optimal_cycles[i]:.1f}秒 (原: {self.intersection_data[intersection]['current_cycle']}秒)")
        
        # 更新数据
        for i, intersection in enumerate(self.intersections):
            self.intersection_data[intersection]['optimal_cycle'] = optimal_cycles[i]
            self.intersection_data[intersection]['current_waiting'] = current_waiting[i]
            self.intersection_data[intersection]['optimal_waiting'] = optimal_waiting[i]
        
        return {
            'optimal_cycles': optimal_cycles,
            'current_waiting': current_waiting,
            'optimal_waiting': optimal_waiting,
            'improvement_rate': improvement_rate
        }
    
    def analyze_traffic_patterns(self):
        """分析交通模式"""
        print("\n=== 交通模式分析 ===")
        
        # 统计分析
        mean_flow = statistics.mean(self.traffic_flow)
        std_flow = statistics.stdev(self.traffic_flow)
        
        # 找出高峰时段
        peak_hours = []
        for i, flow in enumerate(self.traffic_flow):
            if flow > mean_flow + std_flow:
                peak_hours.append(i)
        
        print(f"平均流量: {mean_flow:.1f} 辆/小时")
        print(f"流量标准差: {std_flow:.1f} 辆/小时")
        print(f"高峰时段: {peak_hours} 时")
        
        # 创建时间序列数据
        self.traffic_df = []
        for i, hour in enumerate(range(24)):
            self.traffic_df.append({
                'hour': hour,
                'traffic_flow': self.traffic_flow[i],
                'is_peak': hour in peak_hours
            })
        
        return self.traffic_df
    
    def create_text_visualization(self):
        """创建文本可视化"""
        print("\n=== 文本可视化结果 ===")
        
        # 1. 交通流量时间序列图（文本版）
        print("\n1. 24小时交通流量变化:")
        print("时间  流量  状态")
        print("-" * 20)
        
        for data in self.traffic_df:
            hour = data['hour']
            flow = data['traffic_flow']
            status = "高峰" if data['is_peak'] else "正常"
            print(f"{hour:2d}时  {flow:5.1f}  {status}")
        
        # 2. 路口优化对比表
        print("\n2. 路口等待时间优化对比:")
        print("路口  当前等待  优化后  改进率")
        print("-" * 30)
        
        total_current = 0
        total_optimal = 0
        
        for intersection in self.intersections:
            data = self.intersection_data[intersection]
            current = data['current_waiting']
            optimal = data['optimal_waiting']
            improvement_rate = (current - optimal) / current * 100
            
            total_current += current
            total_optimal += optimal
            
            print(f"{intersection}    {current:6.1f}    {optimal:6.1f}    {improvement_rate:5.1f}%")
        
        # 3. 总体改进效果
        total_improvement = total_current - total_optimal
        total_improvement_rate = total_improvement / total_current * 100
        
        print(f"\n3. 总体改进效果:")
        print(f"   当前总等待时间: {total_current:.1f}")
        print(f"   优化后总等待时间: {total_optimal:.1f}")
        print(f"   总体改进: {total_improvement_rate:.2f}%")
        print(f"   节省等待时间: {total_improvement:.1f}")
        
        # 4. 信号灯周期优化
        print("\n4. 信号灯周期优化:")
        print("路口  当前周期  优化周期  调整幅度")
        print("-" * 30)
        
        for intersection in self.intersections:
            data = self.intersection_data[intersection]
            current = data['current_cycle']
            optimal = data['optimal_cycle']
            change = optimal - current
            
            print(f"{intersection}    {current:6d}    {optimal:6.1f}    {change:+6.1f}")
    
    def create_analysis_report(self):
        """创建分析报告"""
        total_current = sum(self.intersection_data[i]['current_waiting'] for i in self.intersections)
        total_optimal = sum(self.intersection_data[i]['optimal_waiting'] for i in self.intersections)
        improvement = total_current - total_optimal
        improvement_rate = improvement / total_current * 100
        
        mean_flow = statistics.mean(self.traffic_flow)
        std_flow = statistics.stdev(self.traffic_flow)
        peak_hours = [i for i, flow in enumerate(self.traffic_flow) 
                     if flow > mean_flow + std_flow]
        
        report = f"""
=== 交通信号灯优化分析报告 ===

1. 问题描述:
   - 目标：优化城市5个主要路口的信号灯配时
   - 方法：基于流量比例的简单优化算法

2. 数据概况:
   - 监测时段：24小时
   - 路口数量：5个
   - 交通流量范围：{min(self.traffic_flow):.1f} - {max(self.traffic_flow):.1f} 辆/小时

3. 优化结果:
   - 当前总等待时间：{total_current:.1f}
   - 优化后总等待时间：{total_optimal:.1f}
   - 总体改进：{improvement_rate:.2f}%
   - 节省等待时间：{improvement:.1f}

4. 各路口优化详情：
"""
        
        for intersection in self.intersections:
            data = self.intersection_data[intersection]
            current = data['current_waiting']
            optimal = data['optimal_waiting']
            improvement_rate_i = (current - optimal) / current * 100
            optimal_cycle = data['optimal_cycle']
            
            report += f"""
   {intersection}路口:
     - 当前等待时间：{current:.1f}
     - 优化后等待时间：{optimal:.1f}
     - 改进比例：{improvement_rate_i:.2f}%
     - 最优信号灯周期：{optimal_cycle:.1f}秒
"""
        
        report += f"""
5. 高峰时段分析:
   - 平均流量：{mean_flow:.1f} 辆/小时
   - 流量标准差：{std_flow:.1f} 辆/小时
   - 高峰时段：{peak_hours} 时

6. 建议：
   - 在高峰时段（{peak_hours}时）适当调整信号灯周期
   - 重点优化{self.intersections[max(range(len(self.intersections)), 
                key=lambda i: self.intersection_data[self.intersections[i]]['current_waiting'])]}路口
   - 建议实施动态信号灯控制系统

报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open('/root/clawd/optimization_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("\n✅ 分析报告已保存为: optimization_report.txt")
        print(report)

def main():
    """主函数"""
    print("🚦 开始交通流量优化建模...")
    
    # 创建优化实例
    optimizer = SimpleTrafficOptimization()
    
    # 分析交通模式
    traffic_analysis = optimizer.analyze_traffic_patterns()
    
    # 求解优化问题
    optimization_result = optimizer.simple_optimization()
    
    # 创建文本可视化
    optimizer.create_text_visualization()
    
    # 创建分析报告
    optimizer.create_analysis_report()
    
    print("\n🎉 建模完成！")
    print("📁 生成的文件：")
    print("   - optimization_report.txt (详细分析报告)")

if __name__ == "__main__":
    main()