"""
数学建模常用库完整示例
展示 numpy, pandas, scipy, matplotlib, seaborn, sklearn, statsmodels 的使用
"""

import numpy as np
import pandas as pd
import scipy
import scipy.optimize as opt
import scipy.stats as stats
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("🚀 数学建模常用库完整演示")
print("=" * 60)

# ========================================
# 1. NumPy - 数值计算
# ========================================
print("\n【1. NumPy - 数值计算】")
print("-" * 40)

# 创建数组
arr = np.array([1, 2, 3, 4, 5])
matrix = np.random.rand(3, 3)

print(f"一维数组: {arr}")
print(f"3x3矩阵:\n{matrix}")
print(f"矩阵行列式: {np.linalg.det(matrix):.4f}")
print(f"矩阵特征值: {np.linalg.eigvals(matrix)}")

# 矩阵运算
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
print(f"\n矩阵A:\n{a}")
print(f"矩阵B:\n{b}")
print(f"A+B:\n{a + b}")
print(f"A@B (矩阵乘法):\n{a @ b}")

# ========================================
# 2. Pandas - 数据处理
# ========================================
print("\n【2. Pandas - 数据处理】")
print("-" * 40)

# 创建DataFrame
data = {
    '城市': ['北京', '上海', '广州', '深圳', '杭州'],
    'GDP': [41610, 43214, 28231, 30664, 18109],
    '人口': [2189, 2487, 1867, 1756, 1194]
}
df = pd.DataFrame(data)

print("原始数据:")
print(df)

# 数据统计
print(f"\n数据统计:")
print(df.describe())

# 数据排序
print(f"\n按GDP排序:")
print(df.sort_values('GDP', ascending=False))

# ========================================
# 3. SciPy - 科学计算
# ========================================
print("\n【3. SciPy - 科学计算】")
print("-" * 40)

# 优化问题示例：最小化函数
def rosenbrock(x):
    """Rosenbrock函数（经典的优化测试函数）"""
    return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

# 初始猜测
x0 = np.array([-1.5, 2.5])

# 使用BFGS算法优化
result = opt.minimize(rosenbrock, x0, method='BFGS')
print(f"优化问题: 最小化 Rosenbrock 函数")
print(f"初始点: {x0}")
print(f"最优解: {result.x}")
print(f"最优值: {result.fun:.6f}")
print(f"是否收敛: {result.success}")

# 统计检验
print(f"\n统计检验示例:")
data_sample = np.random.normal(loc=5, scale=2, size=100)

# 单样本t检验
t_stat, p_value = stats.ttest_1samp(data_sample, popmean=5)
print(f"单样本t检验 (假设均值=5):")
print(f"  t统计量: {t_stat:.4f}")
print(f"  p值: {p_value:.4f}")
print(f"  结论: {'拒绝原假设' if p_value < 0.05 else '无法拒绝原假设'}")

# ========================================
# 4. Matplotlib + Seaborn - 可视化
# ========================================
print("\n【4. Matplotlib + Seaborn - 可视化】")
print("-" * 40)

try:
    import matplotlib
    matplotlib.use('Agg')  # 使用非交互式后端
    import matplotlib.pyplot as plt
    import seaborn as sns

    # 创建图表
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('数学建模可视化示例', fontsize=16, fontweight='bold')

    # 1. 折线图 - 时间序列
    time = np.arange(0, 10, 0.1)
    y1 = np.sin(time)
    y2 = np.cos(time)
    y3 = np.random.normal(0, 0.2, len(time)) + y1  # 带噪声的正弦波

    axes[0, 0].plot(time, y1, label='sin(t)', linewidth=2)
    axes[0, 0].plot(time, y2, label='cos(t)', linewidth=2)
    axes[0, 0].plot(time, y3, label='sin(t)+noise', linewidth=1, alpha=0.6)
    axes[0, 0].set_xlabel('时间')
    axes[0, 0].set_ylabel('值')
    axes[0, 0].set_title('时间序列图')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # 2. 散点图 + 回归线
    x_reg = np.random.randn(100) * 2 + 5
    y_reg = 3 * x_reg + 10 + np.random.randn(100) * 3

    axes[0, 1].scatter(x_reg, y_reg, alpha=0.6, s=50)

    # 添加回归线
    z = np.polyfit(x_reg, y_reg, 1)
    p = np.poly1d(z)
    axes[0, 1].plot(x_reg, p(x_reg), "r--", linewidth=2, label=f'y={z[0]:.2f}x+{z[1]:.2f}')

    axes[0, 1].set_xlabel('X')
    axes[0, 1].set_ylabel('Y')
    axes[0, 1].set_title('散点图与回归分析')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # 3. 直方图 + 分布拟合
    data_normal = np.random.normal(loc=0, scale=1, size=1000)

    axes[1, 0].hist(data_normal, bins=30, density=True, alpha=0.7, color='skyblue', edgecolor='black')

    # 添加正态分布曲线
    x_range = np.linspace(-4, 4, 100)
    y_normal = stats.norm.pdf(x_range, 0, 1)
    axes[1, 0].plot(x_range, y_normal, 'r-', linewidth=2, label='标准正态分布')

    axes[1, 0].set_xlabel('值')
    axes[1, 0].set_ylabel('密度')
    axes[1, 0].set_title('直方图与分布拟合')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # 4. 热力图 - 相关性矩阵
    corr_df = pd.DataFrame({
        'A': np.random.randn(100),
        'B': np.random.randn(100),
        'C': np.random.randn(100) * 2,
        'D': np.random.randn(100) + 1
    })
    correlation = corr_df.corr()

    im = axes[1, 1].imshow(correlation, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
    axes[1, 1].set_xticks(range(len(correlation.columns)))
    axes[1, 1].set_yticks(range(len(correlation.columns)))
    axes[1, 1].set_xticklabels(correlation.columns)
    axes[1, 1].set_yticklabels(correlation.columns)

    # 添加数值标注
    for i in range(len(correlation.columns)):
        for j in range(len(correlation.columns)):
            text = axes[1, 1].text(j, i, f'{correlation.iloc[i, j]:.2f}',
                                  ha="center", va="center", color="black")

    axes[1, 1].set_title('相关性热力图')
    plt.colorbar(im, ax=axes[1, 1])

    plt.tight_layout()
    plt.savefig('/root/clawd/math_modeling_visualization.png', dpi=150, bbox_inches='tight')
    print("✅ 可视化图表已保存为: math_modeling_visualization.png")

except Exception as e:
    print(f"⚠️ 可视化部分跳过: {e}")

# ========================================
# 5. Scikit-learn - 机器学习
# ========================================
print("\n【5. Scikit-learn - 机器学习】")
print("-" * 40)

# 线性回归示例
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 5, 4, 5])

model = LinearRegression()
model.fit(X, y)

print("线性回归示例:")
print(f"训练数据: X={X.flatten()}, y={y}")
print(f"斜率: {model.coef_[0]:.4f}")
print(f"截距: {model.intercept_:.4f}")
print(f"预测 X=6: {model.predict([[6]])[0]:.4f}")

# K-means聚类示例
from sklearn.datasets import make_blobs

# 生成聚类数据
X_cluster, _ = make_blobs(n_samples=300, centers=3, cluster_std=0.60, random_state=42)

# 标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_cluster)

# 聚类
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans.fit(X_scaled)

print(f"\nK-means聚类示例:")
print(f"聚类数量: 3")
print(f"样本数: 300")
print(f"聚类中心:\n{kmeans.cluster_centers_}")
print(f"惯性(Inertia): {kmeans.inertia_:.4f}")

# ========================================
# 6. Statsmodels - 统计建模
# ========================================
print("\n【6. Statsmodels - 统计建模】")
print("-" * 40)

# 创建回归数据
np.random.seed(42)
x_stat = np.random.randn(100)
y_stat = 2.5 * x_stat + 5 + np.random.randn(100) * 1.5

# 添加常数项
X_stat = sm.add_constant(x_stat)

# OLS回归
model_stat = sm.OLS(y_stat, X_stat).fit()

print("OLS回归结果:")
print(model_stat.summary())

print(f"\n关键指标:")
print(f"R²: {model_stat.rsquared:.4f}")
print(f"调整R²: {model_stat.rsquared_adj:.4f}")
print(f"F统计量: {model_stat.fvalue:.4f}")
print(f"AIC: {model_stat.aic:.4f}")
print(f"BIC: {model_stat.bic:.4f}")

# ========================================
# 总结
# ========================================
print("\n" + "=" * 60)
print("🎉 演示完成！")
print("=" * 60)
print("\n📚 已演示的库和功能:")
print("  1. NumPy: 数组运算、矩阵计算、线性代数")
print("  2. Pandas: 数据创建、统计分析、排序")
print("  3. SciPy: 优化算法、统计检验")
print("  4. Matplotlib: 折线图、散点图、直方图、热力图")
print("  5. Scikit-learn: 线性回归、K-means聚类")
print("  6. Statsmodels: OLS回归、统计建模")
print("\n💡 这些库覆盖了数学建模的主要需求！")
print("=" * 60)