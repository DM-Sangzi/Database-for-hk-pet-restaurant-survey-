# -*- coding: utf-8 -*-
"""从原始 CSV 生成 report 用图表（英文标签，学术风格）"""
import io
import os
import zipfile

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.unicode_minus'] = False

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'charts')
os.makedirs(OUT, exist_ok=True)

GREEN = '#2E6B4F'
GREEN_LIGHT = '#7FA99B'
GREY = '#5C5C5C'
GRID = '#DDDDDD'


def style_axes(ax):
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(axis='both', colors=GREY, labelsize=9, length=0)
    ax.xaxis.grid(True, color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)


def hbar(values, labels, title, fname, xlabel='% of respondents', color=GREEN,
         figsize=(7.2, 3.6), highlight_max=True):
    fig, ax = plt.subplots(figsize=figsize, dpi=220)
    ypos = range(len(values))
    colors = [color] * len(values)
    if highlight_max:
        mx = max(values)
        colors = ['#1F4A36' if v == mx else color for v in values]
    bars = ax.barh(list(ypos), values, color=colors, height=0.62)
    ax.set_yticks(list(ypos))
    ax.set_yticklabels(labels, fontsize=9.5)
    ax.invert_yaxis()
    ax.set_xlabel(xlabel, fontsize=9, color=GREY)
    ax.set_title(title, fontsize=11.5, fontweight='bold', color='#1F2328', pad=12, loc='left')
    ax.set_xlim(0, max(values) * 1.22)
    style_axes(ax)
    for b, v in zip(bars, values):
        ax.text(b.get_width() + max(values) * 0.015, b.get_y() + b.get_height() / 2,
                f'{v:.1f}%', va='center', fontsize=9, color=GREY)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('saved', fname)


# ---------- 读取数据 ----------
DATA = os.path.join(BASE, 'data')
df1 = pd.read_csv(os.path.join(DATA, 'survey_a_main_144.csv'), encoding='utf-8-sig')

df2 = pd.read_csv(os.path.join(DATA, 'survey_b_followup_63.csv'), encoding='utf-8-sig')

cols1 = list(df1.columns)
cols2 = list(df2.columns)


def pct_single(series, order):
    s = series.dropna().astype(str).str.strip()
    s = s[s != '']
    n = len(s)
    vc = s.value_counts()
    return [vc.get(k, 0) / n * 100 for k in order], n


def pct_multi(series, order):
    s = series.dropna().astype(str)
    s = s[s.str.strip() != '']
    n = len(s)
    counts = {}
    for row in s:
        for item in [x.strip() for x in row.replace('；', ';').split(';') if x.strip()]:
            counts[item] = counts.get(item, 0) + 1
    return [counts.get(k, 0) / n * 100 for k in order], n


# ================= Fig 1: 整体态度 =================
att_order = ['非常支持', '支持', '中立', '暫時未有足夠資訊判斷', '反對', '非常反對']
att_en = ['Strongly support', 'Support', 'Neutral', 'Not enough info', 'Oppose', 'Strongly oppose']
vals, n = pct_single(df1[cols1[2]], att_order)
hbar(vals, att_en,
     f'Fig. 1  Overall attitude towards allowing dogs in restaurants (n = {n})',
     'fig1_overall_attitude.png')

# ================= Fig 2: 主要顾虑 =================
con_order = ['突發攻擊行為或安全隱患', '寵物排泄或弄污餐廳設施', '寵物毛髮散播與過敏源',
             '食品衛生與環境清潔', '寵物吠叫或噪音滋擾']
con_en = ['Sudden aggression / safety', 'Excretion or soiling', 'Hair and allergens',
          'Food hygiene', 'Barking / noise nuisance']
vals, n = pct_multi(df1[cols1[8]], con_order)
hbar(vals, con_en,
     f'Fig. 3  Main concerns when dining (up to 2 choices, n = {n})',
     'fig3_main_concerns.png')

# ================= Fig 3: 主人应履行的责任 =================
resp_order = ['必須使用牽引繩、寵物袋或寵物推車', '禁止寵物使用人類餐具或直接接觸餐桌',
              '確保寵物全程留在座椅旁，不進入公共通道或離開座位',
              '必須為寵物穿上禮貌帶或生理褲/尿布', '確保寵物保持安靜，不持續發出噪音']
resp_en = ['Leash / carrier / stroller', 'No human tableware', 'Stay beside the seat',
           'Pet diaper / belly band', 'Keep the pet quiet']
vals, n = pct_multi(df1[cols1[5]], resp_order)
hbar(vals, resp_en,
     f'Fig. 2  Responsibilities owners should fulfil before entry (multi-select, n = {n})',
     'fig2_owner_duties.png')

# ================= Fig 4: 措施偏好对比（主问卷 vs 追访）=================
m_order = ['餐廳入口設清晰守則及職員提醒', '加重罰款或違規後果', '強制飼主完成責任課程／考試',
           '公眾教育宣傳（短片、海報、社交媒體）', '免費寵物行為訓練課程', '鼓勵市民舉報或即場提醒']
m_en = ['Clear rules at entrance', 'Heavier fines', 'Mandatory course / exam',
        'Public education', 'Free training course', 'Encourage reporting']
v1, n1 = pct_multi(df1[cols1[13]], m_order)
v2, n2 = pct_multi(df2[cols2[1]], m_order)

fig, ax = plt.subplots(figsize=(7.2, 4.0), dpi=220)
ypos = range(len(m_order))
h = 0.36
b1 = ax.barh([y - h / 2 for y in ypos], v1, height=h, color=GREEN,
             label=f'Main survey (n = {n1})')
b2 = ax.barh([y + h / 2 for y in ypos], v2, height=h, color=GREEN_LIGHT,
             label=f'Follow-up survey (n = {n2})')
ax.set_yticks(list(ypos))
ax.set_yticklabels(m_en, fontsize=9.5)
ax.invert_yaxis()
ax.set_xlabel('% of respondents', fontsize=9, color=GREY)
ax.set_title('Fig. 5  Measures to improve owner responsibility: main vs follow-up survey',
             fontsize=11.5, fontweight='bold', color='#1F2328', pad=12, loc='left')
ax.set_xlim(0, max(max(v1), max(v2)) * 1.25)
style_axes(ax)
for bars, vals in ((b1, v1), (b2, v2)):
    for b, v in zip(bars, vals):
        ax.text(b.get_width() + max(max(v1), max(v2)) * 0.012,
                b.get_y() + b.get_height() / 2, f'{v:.0f}%', va='center',
                fontsize=8.5, color=GREY)
ax.legend(frameon=False, fontsize=9, loc='lower right', labelcolor=GREY)
fig.tight_layout()
fig.savefig(os.path.join(OUT, 'fig5_measures_comparison.png'), bbox_inches='tight', facecolor='white')
plt.close(fig)
print('saved fig5_measures_comparison.png')

# ================= Fig 5: 疫苗与社交训练要求 =================
q9_order = ['非常同意', '同意', '普通', '不同意', '非常不同意']
q9_en = ['Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree']
vals, n = pct_single(df1[cols1[11]], q9_order)
hbar(vals, q9_en,
     f'Fig. 4  Support for vaccination and social training before entry (n = {n})',
     'fig4_training_requirement.png')

# ================= Fig 6: 饲主 vs 非饲主 交叉对比 =================
a1 = df1[cols1[1]].astype(str).str.strip()
is_owner = a1.str.startswith('有飼養')
q9 = df1[cols1[11]].astype(str).str.strip()
sup_q9 = q9.str.contains('非常同意') | q9.str.contains('^同意')
a2 = df1[cols1[2]].astype(str).str.strip()
sup_a2 = a2.str.contains('非常支持') | (a2.str.contains('支持') & ~a2.str.contains('反對'))

owner_a2 = sup_a2[is_owner].mean() * 100
non_a2 = sup_a2[~is_owner].mean() * 100
owner_q9 = sup_q9[is_owner].mean() * 100
non_q9 = sup_q9[~is_owner].mean() * 100
n_owner = int(is_owner.sum())
n_non = int((~is_owner).sum())

fig, ax = plt.subplots(figsize=(7.2, 3.6), dpi=220)
labels = ['Support allowing dogs\nin restaurants', 'Support mandatory vaccination\nand training']
x = [0, 1]
w = 0.34
b1 = ax.bar([i - w / 2 for i in x], [owner_a2, owner_q9], width=w, color=GREEN,
            label=f'Pet owners (n = {n_owner})')
b2 = ax.bar([i + w / 2 for i in x], [non_a2, non_q9], width=w, color=GREEN_LIGHT,
            label=f'Non-owners (n = {n_non})')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=9.5)
ax.set_ylabel('% of group', fontsize=9, color=GREY)
ax.set_title('Fig. 6  Attitudes towards pets in restaurants by pet ownership',
             fontsize=11.5, fontweight='bold', color='#1F2328', pad=12, loc='left')
ax.set_ylim(0, 105)
for s in ['top', 'right']:
    ax.spines[s].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)
ax.tick_params(axis='both', colors=GREY, labelsize=9, length=0)
ax.yaxis.grid(True, color=GRID, linewidth=0.7)
ax.set_axisbelow(True)
for bars, vals in ((b1, [owner_a2, owner_q9]), (b2, [non_a2, non_q9])):
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 2, f'{v:.1f}%',
                ha='center', va='bottom', fontsize=9, color=GREY)
ax.legend(frameon=False, fontsize=9, loc='upper right', labelcolor=GREY, ncol=2)
fig.tight_layout()
fig.savefig(os.path.join(OUT, 'fig6_owner_comparison.png'), bbox_inches='tight', facecolor='white')
plt.close(fig)
print('saved fig6_owner_comparison.png')

print('\nAll charts saved to', OUT)
