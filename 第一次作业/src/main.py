import os
import json
import random
from structures import Stack, Queue, PriorityQueue
from search import generic_search
from visualizer import save_visual_graph


def get_graph(config, base_dir):
    graph = {}
    # 统一默认值为 False
    is_directed = config.get("is_directed", False)

    if config['use_random_graph']:
        if config['use_seed']: random.seed(config['random_seed'])
        n = config['node_count']
        graph = {i: [] for i in range(n)}
        for i in range(n):
            targets = random.sample([x for x in range(n) if x != i], 2)
            for t in targets:
                w = random.randint(1, 20)
                graph[i].append((t, w))
                if not is_directed:
                    # 确保目标节点也在字典中，并添加反向边
                    if t not in graph: graph[t] = []
                    graph[t].append((i, w))
        print(f"随机{'有向' if is_directed else '无向'}图已生成")
    else:
        input_path = os.path.join(base_dir, config['input_file'])
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                # 强制转换为 int 确保类型统一
                u, v, w = map(int, line.split())
                if u not in graph: graph[u] = []
                if v not in graph: graph[v] = []
                graph[u].append((v, w))
                if not is_directed:
                    graph[v].append((u, w))
        print(f"已从文件加载{'有向' if is_directed else '无向'}图")
    return graph


def run():
    # 寻找项目绝对路径
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config.json")

    if not os.path.exists(config_path):
        print(f"错误: 找不到配置文件 {config_path}")
        return

    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # 【关键修改 1】：强制将起点和终点转为 int
    # 这样可以防止 config.json 中写成字符串导致的类型不匹配
    start = int(config['start_node'])
    goal = int(config['goal_node'])

    # 【关键修改 2】：此处默认值需与 get_graph 保持一致 (False)
    is_directed = config.get("is_directed", False)

    graph = get_graph(config, base_dir)

    algorithms_map = {
        "DFS": Stack,
        "BFS": Queue,
        "UCS": PriorityQueue
    }

    target_algo = config.get("algorithm", "ALL").upper()
    tasks = []

    if target_algo == "ALL":
        tasks = [("DFS", Stack()), ("BFS", Queue()), ("UCS", PriorityQueue())]
    elif target_algo in algorithms_map:
        tasks = [(target_algo, algorithms_map[target_algo]())]
    else:
        print(f"错误: config.json 中的算法 '{target_algo}' 不支持")
        print("可选值: DFS, BFS, UCS, ALL")
        return

    # 搜索+可视化部分
    print(f">> 任务目标: 节点 {start} -> 节点 {goal}")
    print("=" * 60)

    for name, fringe in tasks:
        print(f"【执行:{name}】")
        # 执行搜索
        path, cost, expanded = generic_search(graph, start, goal, fringe)

        if path:
            print(f"  - 状态: 成功找到路径")
            print(f"  - 路径: {' -> '.join(map(str, path))}")
            print(f"  - 累计权重代价: {cost}")
        else:
            print(f"  - 状态: 无法找到从 {start} 到 {goal} 的路径")

        # 如果此值为 0，说明起点 start 在图中完全找不到邻居，或者 start 的值本身有问题
        print(f"  - 扩展节点数: {expanded}")

        # 调用可视化模块
        visual_file = f"result_{name}.html"
        save_visual_graph(
            graph=graph,
            path=path,
            output_name=visual_file,
            title=f"{name} Results",
            is_directed=is_directed,
            algo_name=name
        )
        print("-" * 60)

    print("\n可视化结果保存在项目根目录。")


if __name__ == "__main__":
    run()