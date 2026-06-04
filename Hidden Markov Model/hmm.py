import numpy as np

# 转移矩阵
T = np.array([
    [0.7, 0.3],
    [0.3, 0.7],
])

# 观测矩阵
O = np.array([
    [0.9, 0.2],
    [0.1, 0.8],
])

# 先验
P0 = np.array([0.5, 0.5])

# 观测序列
observations_raw = [True, True, False, True, True]
obs_idx = [0 if o else 1 for o in observations_raw]

STATE_NAMES = ['+r', '-r']

# 辅助函数
def normalize(v):
    s = v.sum()
    return v / s, s

def obs_vec(e_idx):
    return O[e_idx]

# 前向算法
def forward_all(obs_list, prior):
    f = prior.copy()
    fs = []
    for e in obs_list:
        predicted = T.T @ f
        updated = obs_vec(e) * predicted
        f, _ = normalize(updated)
        fs.append(f.copy())
    return fs

# 预测
def predict_one_step(f):
    return T.T @ f

# 后向算法、平滑
def backward_all(obs_list):
    n = len(obs_list)
    b = np.ones(2)
    bs = [None] * n
    bs[n - 1] = b.copy()

    for k in range(n - 2, -1, -1):
        e_next = obs_list[k + 1]
        b = T @ (obs_vec(e_next) * b)
        bs[k] = b.copy()
    return bs

def smooth(fs, bs, k):
    fk = fs[k - 1]
    bk = bs[k - 1]
    s, _ = normalize(fk * bk)
    return s

# 维特比算法
def viterbi(obs_list, prior):
    n = len(obs_list)
    n_states = len(prior)

    delta = np.zeros((n, n_states))
    psi = np.zeros((n, n_states), dtype=int)
    e0 = obs_list[0]
    delta[0] = obs_vec(e0) * prior

    # 递推
    for t in range(1, n):
        e = obs_list[t]
        for s in range(n_states):
            probs = delta[t - 1] * T[:, s]
            psi[t, s] = np.argmax(probs)
            delta[t, s] = obs_vec(e)[s] * np.max(probs)
    # 回溯
    path = np.zeros(n, dtype=int)
    path[n - 1] = np.argmax(delta[n - 1])
    for t in range(n - 2, -1, -1):
        path[t] = psi[t + 1, path[t + 1]]

    labels = [STATE_NAMES[s] for s in path]
    max_probs = [delta[t, path[t]] for t in range(n)]
    return labels, max_probs

# 主程序
if __name__ == '__main__':
    T_steps = len(obs_idx)

    fs = forward_all(obs_idx, P0)

    bs = backward_all(obs_idx)

    print("  HMM 模型推断结果")
    print("  观测序列: ", observations_raw)

    print("\n各时刻滤波分布:")
    for t, f in enumerate(fs, 1):
        obs_sym = '+u' if observations_raw[t-1] else '-u'
        print(f"  t={t} (e={obs_sym}): P(+r)={f[0]:.6f}, P(-r)={f[1]:.6f}")
# q1
    f5 = fs[4]
    print(f"\nq1:第5天滤波分布 P(x5 | e1:5)")
    print(f"  P(+r | e1:5) = {f5[0]:.6f}")
    print(f"  P(-r | e1:5) = {f5[1]:.6f}")

# q2
    f6_pred = predict_one_step(f5)
    print(f"\nq2:第6天预测分布 P(x6 | e1:5)")
    print(f"  P(+r | e1:5) = {f6_pred[0]:.6f}")
    print(f"  P(-r | e1:5) = {f6_pred[1]:.6f}")

# q3
    s3 = smooth(fs, bs, k=3)
    print(f"\nq3:第3天平滑分布 P(x3 | e1:5)")
    print(f"  P(+r | e1:5) = {s3[0]:.6f}")
    print(f"  P(-r | e1:5) = {s3[1]:.6f}")

# q4
    vit_labels, vit_probs = viterbi(obs_idx, P0)
    print(f"\nq4:维特比最可能状态序列 [x1, x2, x3, x4, x5]")
    print(f"  序列: {vit_labels}")
    print(f"  各时刻最大路径概率:")
    for t, (lbl, p) in enumerate(zip(vit_labels, vit_probs), 1):
        print(f"    t={t}: {lbl}  路径概率={p:.8f}")
    print("  汇总")
    print(f"  P(x6|e1:5): +r={f6_pred[0]:.4f}, -r={f6_pred[1]:.4f}")
    print(f"  P(x5|e1:5): +r={f5[0]:.4f}, -r={f5[1]:.4f}")
    print(f"  P(x3|e1:5): +r={s3[0]:.4f}, -r={s3[1]:.4f}")
    print(f"  Viterbi   : {vit_labels}")
