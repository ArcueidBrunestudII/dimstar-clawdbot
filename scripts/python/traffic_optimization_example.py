"""
数学建模示例：城市交通流量优化问题
目标：优化信号灯配时，最小化车辆等待时间
方法：线性规划 + 数据可视化
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import linprog
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class TrafficOptimization:
    def __init__(self):
        self.generate_data()
        self.setup_optimization()
    
    def generate_data(self):
        """生成模拟的交通流量数据"""
        np.random.seed(42)
        
        # 生成24小时交通流量数据
        hours = np.arange(24)
        # 模拟早晚高峰
        base_flow = 50 + 30 * np.sin(2 * np.pi * (hours - 6) / 24)
        noise = np.random.normal(0, 10, 24)
        self.traffic_flow = np.maximum(base_flow + noise, 10)
        
        # 生成路口数据
        self.intersections = ['A', 'B', 'C', 'D', 'E']
        self.intersection_data = pd.DataFrame({
            'intersection': self.intersections,
            'north_south': np.random.randint(100, 500, 5),
            'east_west': np.random.randint(80, 400, 5),
            'capacity': np.random.randint(800, 1500, 5),
            'current_cycle': np.random.randint(60, 120, 5)
        })
        
        print("=== 数据生成完成 ===")
        print(f"交通流量范围: {self.traffic_flow.min():.1f} - {self.traffic_flow.max():.1f} 辆/小时")
        print(f"路口数据:\n{self.intersection_data}")
    
    def setup_optimization(self):
        """设置优化问题"""
        # 目标函数：最小化总等待时间
        # 决策变量：每个路口的信号灯周期时间
        n_intersections = len(self.intersections)
        
        # 目标函数系数（等待时间系数）
        c = self.intersection_data['north_south'] + self.intersection_data['east_west']
        
        # 约束条件
        # 1. 周期时间限制：60 <= cycle <= 180秒
        A_ub = np.array([
            [-1, -1, -1, -1, -1],  # -cycle_i <= -60
            [1, 1, 1, 1, 1]        # cycle_i <= 180
        ])
        b_ub = np.array([-60 * n_intersections, 180 * n_intersections])
        
        # 2. 总时间约束：所有路口周期时间总和 <= 600秒
        A_total = np.ones(1, n_intersections)
        b_total = [600]
        
        # 合并约束
        A_ub = np.vstack([A_ub, A_total])
        b_ub = np.append(b_ub, b_total)
        
        # 边界约束
        bounds = [(60, 180) for _ in range(n_intersections)]
        
        self.c = c
        self.A_ub = A_ub
        self.b_ub = b_ub
        self.bounds = bounds
        
        print("=== 优化模型设置完成 ===")
        print(f"目标函数系数: {c}")
        print(f"约束矩阵形状: {A_ub.shape}")
    
    def solve_optimization(self):
        """求解优化问题"""
        print("=== 开始求解优化问题 ===")
        
        # 求解线性规划
        result = linprog(
            c=self.c,
            A_ub=self.A_ub,
            b_ub=self.b_ub,
            bounds=self.bounds,
            method='highs'
        )
        
        if result.success:
            optimal_cycles = result.x
            min_waiting_time = result.fun
            
            print(f"✅ 优化成功!")
            print(f"最小总等待时间: {min_waiting_time:.2f}")
            print(f"最优信号灯周期:")
            
            for i, intersection in enumerate(self.intersections):
                print(f"  {intersection}: {optimal_cycles[i]:.1f}秒")
            
            # 更新数据
            self.intersection_data['optimal_cycle'] = optimal_cycles
            self.intersection_data['current_waiting'] = self.intersection_data['north_south'] + self.intersection_data['east_west']
            self.intersection_data['optimal_waiting'] = (self.intersection_data['north_south'] + 
                                                        self.intersection_data['east_west'] * 
                                                        (optimal_cycles / self.intersection_data['current_cycle']))
            
            return result
        else:
            print(f"❌ 优化失败: {result.message}")
            return None
    
    def analyze_traffic_patterns(self):
        """分析交通模式"""
        print("\n=== 交通模式分析 ===")
        
        # 统计分析
        mean_flow = np.mean(self.traffic_flow)
        std_flow = np.std(self.traffic_flow)
        peak_hours = np.where(self.traffic_flow > mean_flow + std_flow)[0]
        
        print(f"平均流量: {mean_flow:.1f} 辆/小时")
        print(f"流量标准差: {std_flow:.1f} 辆/小时")
        print(f"高峰时段: {peak_hours} 时")
        
        # 时间序列分析
        self.traffic_df = pd.DataFrame({
            'hour': np.arange(24),
            'traffic_flow': self.traffic_flow,
            'is_peak': self.traffic_flow > mean_flow + std_flow
        })
        
        return self.traffic_df
    
    def create_visualizations(self):
        """创建可视化图表"""
        print("=== 生成可视化图表 ===")
        
        # 1. 交通流量时间序列图
        plt.figure(figsize=(12, 8))
        
        plt.subplot(2, 2, 1)
        plt.plot(self.traffic_df['hour'], self.traffic_df['traffic_flow'], 
                'b-', linewidth=2, label='交通流量')
        plt.axhline(y=np.mean(self.traffic_flow), color='r', linestyle='--', 
                   label='平均流量')
        plt.fill_between(self.traffic_df['hour'], self.traffic_df['traffic_flow'], 
                        alpha=0.3, where=self.traffic_df['is_peak'], 
                        color='red', label='高峰时段')
        plt.xlabel('时间 (小时)')
        plt.ylabel('交通流量 (辆/小时)')
        plt.title('24小时交通流量变化')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 2. 路口优化对比图
        plt.subplot(2, 2, 2)
        x = np.arange(len(self.intersections))
        width = 0.35
        
        current_waiting = self.intersection_data['current_waiting']
        optimal_waiting = self.intersection_data['optimal_waiting']
        
        plt.bar(x - width/2, current_waiting, width, label='当前等待时间', alpha=0.8)
        plt.bar(x + width/2, optimal_waiting, width, label='优化后等待时间', alpha=0.8)
        
        plt.xlabel('路口')
        plt.ylabel('等待时间')
        plt.title('路口等待时间优化对比')
        plt.xticks(x, self.intersections)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 3. 信号灯周期优化图
        plt.subplot(2, 2, 3)
        current_cycles = self.intersection_data['current_cycle']
        optimal_cycles = self.intersection_data['optimal_cycle']
        
        plt.plot(self.intersections, current_cycles, 'ro-', linewidth=2, 
                markersize=8, label='当前周期')
        plt.plot(self.intersections, optimal_cycles, 'go-', linewidth=2, 
                markersize=8, label='优化周期')
        
        plt.xlabel('路口')
        plt.ylabel('信号灯周期 (秒)')
        plt.title('信号灯周期优化')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 4. 改进效果饼图
        plt.subplot(2, 2, 4)
        total_current = current_waiting.sum()
        total_optimal = optimal_waiting.sum()
        improvement = total_current - total_optimal
        improvement_rate = improvement / total_current * 100
        
        sizes = [total_optimal, improvement]
        labels = [f'优化后等待时间\n{total_optimal:.1f}', 
                 f'减少的等待时间\n{improvement:.1f}\n({improvement_rate:.1f}%)']
        colors = ['#66b3ff', '#99ff99']
        
        plt.pie(sizes, labels=labels, colors=colors, autopct='', startangle=90)
        plt.title(f'总体改进效果\n总等待时间减少: {improvement_rate:.1f}%')
        
        plt.tight_layout()
        plt.savefig('/root/clawd/traffic_optimization_results.png', dpi=300, bbox_inches='tight')
        print("✅ 可视化图表已保存为: traffic_optimization_results.png")
        
        # 创建详细分析报告
        self.create_analysis_report()
    
    def create_analysis_report(self):
        """创建分析报告"""
        total_current = self.intersection_data['current_waiting'].sum()
        total_optimal = self.intersection_data['optimal_waiting'].sum()
        improvement = total_current - total_optimal
        improvement_rate = improvement / total_current * 100
        
        report = f"""
=== 交通信号灯优化分析报告 ===

1. 问题描述:
   - 目标：优化城市5个主要路口的信号灯配时
   - 方法：线性规划最小化车辆总等待时间

2. 数据概况:
   - 监测时段：24小时
   - 路口数量：5个
   - 交通流量范围：{self.traffic_flow.min():.1f} - {self.traffic_flow.max():.1f} 辆/小时

3. 优化结果:
   - 当前总等待时间：{total_current:.1f}
   - 优化后总等待时间：{total_optimal:.1f}
   - 总体改进：{improvement_rate:.1f}%
   - 节省等待时间：{improvement:.1f}

4. 各路口优化详情：
"""
        
        for i, intersection in enumerate(self.intersections):
            current = self.intersection_data.iloc[i]['current_waiting']
            optimal = self.intersection_data.iloc[i]['optimal_waiting']
            improvement_rate_i = (current - optimal) / current * 100
            optimal_cycle = self.intersection_data.iloc[i]['optimal_cycle']
            
            report += f"""
   {intersection}路口:
     - 当前等待时间：{current:.1f}
     - 优化后等待时间：{optimal:.1f}
     - 改进比例：{improvement_rate_i:.1f}%
     - 最优信号灯周期：{optimal_cycle:.1f}秒
"""
        
        report += f"""
5. 高峰时段分析:
   - 平均流量：{np.mean(self.traffic_flow):.1f} 辆/小时
   - 流量标准差：{np.std(self.traffic_flow):.1f} 辆/小时
   - 高峰时段：{np.where(self.traffic_flow > np.mean(self.traffic_flow) + np.std(self.traffic_flow))[0].tolist()} 时

6. 建议：
   - 在高峰时段（{np.where(self.traffic_flow > np.mean(self.traffic_flow) + np.std(self.traffic_flow))[0].tolist()}时）适当调整信号灯周期
   - 重点优化{self.intersections[np.argmax(self.intersection_data['current_waiting'])]}路口
   - 建议实施动态信号灯控制系统

报告生成时间：{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open('/root/clawd/optimization_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("✅ 分析报告已保存为: optimization_report.txt")
        print(report)

def main():
    """主函数"""
    print("🚦 开始交通流量优化建模...")
    
    # 创建优化实例
    optimizer = TrafficOptimization()
    
    # 分析交通模式
    traffic_analysis = optimizer.analyze_traffic_patterns()
    
    # 求解优化问题
    result = optimizer.solve_optimization()
    
    if result:
        # 创建可视化
        optimizer.create_visualizations()
        
        print("\n🎉 建模完成！")
        print("📁 生成的文件：")
        print("   - traffic_optimization_results.png (可视化图表)")
        print("   - optimization_report.txt (详细分析报告)")
    else:
        print("❌ 建模过程中出现错误")

if __name__ == "__main__":
    main()