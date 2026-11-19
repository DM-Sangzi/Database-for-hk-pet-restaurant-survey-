# -*- coding: utf-8 -*-
import os
"""核实两份问卷数据的真实分布"""
import io
import zipfile
import pandas as pd

pd.set_option('display.max_colwidth', 200)
pd.set_option('display.width', 200)

# ---------- 主问卷 144 份 ----------
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, 'data')
df1 = pd.read_csv(os.path.join(DATA, 'survey_a_main_144.csv'), encoding='utf-8-sig')

# ---------- 追访问卷 63 份 ----------
df2 = pd.read_csv(os.path.join(DATA, 'survey_b_followup_63.csv'), encoding='utf-8-sig')

print('主问卷 shape:', df1.shape)
print('追访问卷 shape:', df2.shape)


def show_single(df, col, label=''):
    s = df[col].dropna().astype(str).str.strip()
    s = s[s != '']
    vc = s.value_counts()
    total = len(s)
    print(f'\n--- {label or col[:40]} (n={total}) ---')
    for k, v in vc.items():
        print(f'  {v:>3}  {v/total*100:>5.1f}%  {k[:80]}')


def show_multi(df, col, label=''):
    s = df[col].dropna().astype(str)
    s = s[s.str.strip() != '']
    items = []
    for row in s:
        parts = [x.strip() for x in row.replace('；', ';').split(';') if x.strip()]
        items.extend(parts)
    vc = pd.Series(items).value_counts()
    total = len(s)
    print(f'\n--- [MULTI] {label or col[:40]} (respondents={total}, selections={len(items)}) ---')
    for k, v in vc.items():
        print(f'  {v:>3} ({v/total*100:>5.1f}% of respondents)  {k[:70]}')


print('\n' + '=' * 78)
print('主问卷 144 份 — 逐题分布')
print('=' * 78)
for i, c in enumerate(df1.columns):
    if i == 0:
        continue
    col = df1[c]
    multi = col.dropna().astype(str).str.contains(';', regex=False).mean()
    if multi > 0.05 or '多選' in str(c) or '最多選' in str(c):
        show_multi(df1, c, label=f'{i}. {str(c)[-45:]}')
    else:
        show_single(df1, c, label=f'{i}. {str(c)[-45:]}')

print('\n' + '=' * 78)
print('追访问卷 63 份 — 逐题分布')
print('=' * 78)
for i, c in enumerate(df2.columns):
    if i == 0:
        continue
    show_multi(df2, c, label=f'{i}. {str(c)[-45:]}')
