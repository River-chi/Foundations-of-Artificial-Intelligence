import os
from pyvis.network import Network


def save_visual_graph(graph, path, output_name, title, is_directed=False, algo_name="Unknown"):
    # 初始化网络，不再设置 heading 属性
    net = Network(height="800px", width="100%", bgcolor="#ffffff", font_color="#000000", directed=is_directed)

    # 物理布局优化：让节点分布更均匀
    net.set_options("""
    var options = {
      "nodes": {
        "borderWidth": 2,
        "shadow": {"enabled": true},
        "font": { "size": 16, "face": "Tahoma" }
      },
      "edges": {
        "color": { "inherit": false },
        "smooth": { "type": "continuous" },
        "font": { "size": 11, "align": "top", "strokeWidth": 1 }
      },
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -200,
          "centralGravity": 0.01,
          "springLength": 200,
          "springConstant": 0.05
        },
        "solver": "forceAtlas2Based",
        "stabilization": { "iterations": 100 }
      }
    }
    """)

    # 收集所有节点
    all_nodes = set()
    for u in graph:
        all_nodes.add(u)
        for v, _ in graph[u]:
            all_nodes.add(v)

    # 添加节点并着色
    path_nodes = set(path) if path else set()
    for node in all_nodes:
        color = "#97c2fc"  # 默认蓝色
        size = 25
        label = f"Node {node}"

        if path:
            if node == path[0]:
                color = "#28a745";
                size = 40;
                label = f"START: {node}"
            elif node == path[-1]:
                color = "#dc3545";
                size = 40;
                label = f"GOAL: {node}"
            elif node in path_nodes:
                color = "#ffc107"

        net.add_node(str(node), label=label, color=color, size=size, shape="dot")
    # 信息框
    net.add_node("ALGO_INFO",
                 label=f" SEARCH RESULT \n Algorithm: {algo_name} ",
                 color="#f8f9fa",
                 size=40,
                 shape="box",
                 borderWidth=2,
                 font={'size': 22, 'color': '#333333', 'face': 'Courier'},
                 x=-400, y=-350,
                 physics=False)
    # 处理边
    path_edges = set()
    if path:
        for i in range(len(path) - 1):
            u_p, v_p = str(path[i]), str(path[i + 1])
            if is_directed:
                path_edges.add((u_p, v_p))
            else:
                path_edges.add(tuple(sorted((u_p, v_p))))

    seen_edges = set()
    for u in graph:
        for v, w in graph[u]:
            u_s, v_s = str(u), str(v)
            edge_key = (u_s, v_s) if is_directed else tuple(sorted((u_s, v_s)))

            if is_directed or (edge_key not in seen_edges):
                is_in_path = edge_key in path_edges

                edge_color = "#e67e22" if is_in_path else "#34495e"
                width = 8 if is_in_path else 1.2

                net.add_edge(u_s, v_s,
                             label=str(w),
                             color={'color': edge_color},
                             width=width,
                             arrows='to' if is_directed else '')
                seen_edges.add(edge_key)
    # 保存文件
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_path = os.path.join(base_dir, output_name)
    net.save_graph(save_path)
    print(f"  [Visual] Done: {output_name}")