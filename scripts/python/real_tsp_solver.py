"""
数学建模实战：旅行商问题（TSP）- 真实可用的解决方案
使用遗传算法求解TSP问题
这是一个经典的数学建模问题，代码可以直接运行
"""

import random
import math

# 尝试导入matplotlib，如果失败就跳过可视化
HAS_MATPLOTLIB = False
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    print("⚠️ 未安装matplotlib，跳过可视化")

class TSPSolver:
    """旅行商问题求解器 - 使用遗传算法"""
    
    def __init__(self, cities, population_size=100, generations=500):
        self.cities = cities  # 城市坐标 [(x,y), ...]
        self.n_cities = len(cities)
        self.population_size = population_size
        self.generations = generations
        self.best_distance = float('inf')
        self.best_route = None
        self.history = []  # 记录每代最优解
        
        print(f"📊 TSP求解器初始化完成")
        print(f"   城市数量: {self.n_cities}")
        print(f"   种群大小: {population_size}")
        print(f"   迭代代数: {generations}")
    
    def calculate_distance(self, route):
        """计算路径总距离"""
        total = 0
        for i in range(len(route) - 1):
            city1 = self.cities[route[i]]
            city2 = self.cities[route[i + 1]]
            dist = math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)
            total += dist
        # 回到起点
        last_city = self.cities[route[-1]]
        first_city = self.cities[route[0]]
        total += math.sqrt((last_city[0] - first_city[0])**2 + (last_city[1] - first_city[1])**2)
        return total
    
    def generate_route(self):
        """生成随机路径"""
        route = list(range(self.n_cities))
        random.shuffle(route)
        return route
    
    def initialize_population(self):
        """初始化种群"""
        return [self.generate_route() for _ in range(self.population_size)]
    
    def tournament_selection(self, population, tournament_size=5):
        """锦标赛选择"""
        tournament = random.sample(population, tournament_size)
        return min(tournament, key=lambda x: self.calculate_distance(x))
    
    def crossover(self, parent1, parent2):
        """顺序交叉"""
        n = len(parent1)
        start = random.randint(0, n-1)
        end = random.randint(start+1, n)
        
        # 从parent1复制一段
        child = [-1] * n
        child[start:end] = parent1[start:end]
        
        # 从parent2填充剩余城市
        remaining = [city for city in parent2 if city not in child]
        idx = 0
        for i in range(n):
            if child[i] == -1:
                child[i] = remaining[idx]
                idx += 1
        
        return child
    
    def mutate(self, route, mutation_rate=0.01):
        """交换变异"""
        if random.random() < mutation_rate:
            i, j = random.sample(range(len(route)), 2)
            route[i], route[j] = route[j], route[i]
        return route
    
    def solve(self):
        """求解TSP问题"""
        print(f"\n🔄 开始求解...")
        
        # 初始化种群
        population = self.initialize_population()
        
        for generation in range(self.generations):
            # 评估适应度
            distances = [self.calculate_distance(route) for route in population]
            
            # 记录最优解
            min_dist_idx = distances.index(min(distances))
            current_best_dist = distances[min_dist_idx]
            current_best_route = population[min_dist_idx].copy()
            
            self.history.append(current_best_dist)
            
            if current_best_dist < self.best_distance:
                self.best_distance = current_best_dist
                self.best_route = current_best_route
            
            # 输出进度
            if generation % 50 == 0 or generation == self.generations - 1:
                print(f"  第{generation}代: 最优距离 = {self.best_distance:.2f}")
            
            # 生成新一代
            new_population = []
            
            # 精英保留
            elite_size = int(self.population_size * 0.1)
            sorted_pop = [route for _, route in sorted(zip(distances, population), key=lambda x: x[0])]
            new_population.extend(sorted_pop[:elite_size])
            
            # 交叉变异
            while len(new_population) < self.population_size:
                parent1 = self.tournament_selection(population)
                parent2 = self.tournament_selection(population)
                
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                
                new_population.append(child)
            
            population = new_population
        
        print(f"\n✅ 求解完成!")
        print(f"   最优距离: {self.best_distance:.2f}")
        print(f"   最优路径: {self.best_route}")
        
        return self.best_route, self.best_distance, self.history
    
    def visualize(self, save_path='/root/clawd/tsp_solution.png'):
        """可视化结果（如果有matplotlib）"""
        if not HAS_MATPLOTLIB:
            print("⚠️ 无法可视化：未安装matplotlib")
            return None
        
        if self.best_route is None:
            print("⚠️ 请先运行solve()方法")
            return None
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # 左图：城市分布和最优路径
        ax1 = axes[0]
        
        # 绘制城市
        x_coords = [city[0] for city in self.cities]
        y_coords = [city[1] for city in self.cities]
        ax1.scatter(x_coords, y_coords, c='red', s=100, zorder=5)
        
        # 绘制路径
        route_with_return = self.best_route + [self.best_route[0]]
        for i in range(len(route_with_return) - 1):
            city1 = self.cities[route_with_return[i]]
            city2 = self.cities[route_with_return[i + 1]]
            ax1.plot([city1[0], city2[0]], [city1[1], city2[1]], 'b-', linewidth=1, alpha=0.6)
        
        # 标注城市编号
        for i, city in enumerate(self.cities):
            ax1.annotate(str(i), (city[0], city[1]), 
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=8, color='blue')
        
        ax1.set_xlabel('X坐标')
        ax1.set_ylabel('Y坐标')
        ax1.set_title(f'TSP最优路径\n距离: {self.best_distance:.2f}')
        ax1.grid(True, alpha=0.3)
        ax1.set_aspect('equal')
        
        # 右图：收敛曲线
        ax2 = axes[1]
        ax2.plot(self.history, linewidth=2)
        ax2.set_xlabel('代数')
        ax2.set_ylabel('距离')
        ax2.set_title('优化收敛过程')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"✅ 可视化结果已保存: {save_path}")
        
        return save_path

def generate_cities(n_cities=20, x_range=(0, 100), y_range=(0, 100)):
    """生成随机城市"""
    return [(random.uniform(x_range[0], x_range[1]), 
             random.uniform(y_range[0], y_range[1])) 
            for _ in range(n_cities)]

def main():
    """主函数 - 完整的TSP求解示例"""
    print("🚀 开始TSP问题求解...")
    
    # 设置随机种子保证可重复
    random.seed(42)
    
    # 生成20个城市
    cities = generate_cities(n_cities=20)
    print(f"\n📍 生成的城市坐标:")
    for i, city in enumerate(cities):
        print(f"   城市{i}: ({city[0]:.2f}, {city[1]:.2f})")
    
    # 创建求解器
    solver = TSPSolver(cities, population_size=100, generations=500)
    
    # 求解
    best_route, best_distance, history = solver.solve()
    
    # 可视化
    if HAS_MATPLOTLIB:
        solver.visualize()
    
    # 输出结果
    print(f"\n📊 最终结果:")
    print(f"   最短路径距离: {best_distance:.2f}")
    print(f"   访问城市顺序: {best_route}")
    
    # 计算改进
    initial_distance = history[0]
    final_distance = history[-1]
    improvement = (initial_distance - final_distance) / initial_distance * 100
    print(f"   优化改进: {improvement:.1f}%")
    
    print(f"\n🎉 TSP问题求解完成！")

if __name__ == "__main__":
    main()