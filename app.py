import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime
import time

# ページ設定
st.set_page_config(
    page_title="日本人口統計ダッシュボード",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# タイトル
st.title("🗾 日本人口統計ダッシュボード")
st.markdown("オープンデータを活用した日本の人口統計の可視化")

# サイドバー
st.sidebar.title("設定")
st.sidebar.markdown("表示したいデータを選択してください")

# データタイプ選択
data_type = st.sidebar.selectbox(
    "データタイプ",
    ["都道府県別人口", "年齢別人口", "人口推移", "人口密度"]
)

# サンプルデータの生成（実際のプロジェクトではAPIからデータを取得）
@st.cache_data
def load_prefecture_data():
    """都道府県別人口データ（サンプル）"""
    prefectures = [
        "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
        "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
        "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
        "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
        "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
        "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
        "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
    ]
    
    # サンプル人口データ（実際の値に近似）
    populations = [
        5224614, 1237984, 1210534, 2301996, 959502, 1068027, 1833152,
        2867009, 1933146, 1939110, 7344765, 6287734, 14047594, 9237337,
        2201272, 1034814, 1132526, 766863, 809974, 2048011, 1978742,
        3633202, 7542415, 1770254, 1413610, 2578087, 8837685, 5465002,
        1324473, 922584, 553407, 671602, 1888432, 2799702, 1342059,
        728633, 950244, 1334841, 691527, 5135214, 811442, 1312317,
        1738301, 1123852, 1069576, 1588256, 1467480
    ]
    
    # 実際の都道府県面積（km²）に近似したデータ
    areas = [
        83424, 9646, 15275, 7282, 11638, 9323, 13784,  # 北海道〜福島
        6097, 6408, 6362, 3798, 5158, 2194, 2416,      # 茨城〜神奈川
        12584, 4248, 4186, 4190, 4465, 13562, 10621,   # 新潟〜岐阜
        7777, 5173, 5774, 4017, 4612, 1905, 8401,      # 静岡〜兵庫
        3691, 4725, 3507, 6708, 7115, 2833, 6112,      # 奈良〜山口
        4147, 1877, 5676, 7103, 4988, 832, 1311,       # 徳島〜長崎
        7409, 6341, 7735, 9187, 2281                    # 熊本〜沖縄
    ]
    
    return pd.DataFrame({
        "都道府県": prefectures,
        "人口": populations,
        "面積": areas,
        "人口密度": [pop / area for pop, area in zip(populations, areas)]
    })

@st.cache_data
def load_age_data():
    """年齢別人口データ（サンプル）- 10歳間隔"""
    age_groups = [
        "0-9歳", "10-19歳", "20-29歳", "30-39歳", "40-49歳", 
        "50-59歳", "60-69歳", "70-79歳", "80-89歳", "90歳以上"
    ]
    # より現実的な年齢分布（サンプルデータ）
    populations = [
        9500000, 11200000, 12800000, 14500000, 16800000,
        17200000, 16500000, 12400000, 8100000, 2500000
    ]
    
    return pd.DataFrame({
        "年齢層": age_groups,
        "人口": populations
    })

@st.cache_data
def load_time_series_data():
    """人口推移データ（サンプル）"""
    years = list(range(2010, 2024))
    total_pop = [128057000, 127799000, 127515000, 127298000, 127095000,
                 126933000, 126706000, 126443000, 126167000, 125836000,
                 125502000, 125124000, 124777000, 124612000]
    
    return pd.DataFrame({
        "年": years,
        "総人口": total_pop
    })

# メインコンテンツ
if data_type == "都道府県別人口":
    st.header("📍 都道府県別人口分布")
    
    df_pref = load_prefecture_data()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 地図表示（バブルマップ）
        fig = px.scatter(
            df_pref, 
            x="都道府県", 
            y="人口",
            size="人口",
            color="人口密度",
            hover_name="都道府県",
            title="都道府県別人口分布",
            color_continuous_scale="Viridis"
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("統計サマリー")
        st.metric("総人口", f"{df_pref['人口'].sum():,}人")
        st.metric("最大人口", f"{df_pref['人口'].max():,}人")
        st.metric("最小人口", f"{df_pref['人口'].min():,}人")
        st.metric("平均人口", f"{df_pref['人口'].mean():.0f}人")
    
    # 上位・下位ランキング
    st.subheader("📊 人口ランキング")
    col3, col4 = st.columns(2)
    
    with col3:
        st.write("**人口上位10都道府県**")
        top_10 = df_pref.nlargest(10, "人口")[["都道府県", "人口"]]
        st.dataframe(top_10, use_container_width=True)
    
    with col4:
        st.write("**人口下位10都道府県**")
        bottom_10 = df_pref.nsmallest(10, "人口")[["都道府県", "人口"]]
        st.dataframe(bottom_10, use_container_width=True)

elif data_type == "年齢別人口":
    st.header("👥 年齢別人口構成")
    
    df_age = load_age_data()
    
    # 年齢層選択オプション
    view_type = st.radio(
        "表示タイプ",
        ["詳細（10歳間隔）", "従来分類（年少・生産年齢・高齢）"],
        horizontal=True
    )
    
    if view_type == "従来分類（年少・生産年齢・高齢）":
        # 従来の3分類に集約
        young = df_age[df_age["年齢層"].isin(["0-9歳", "10-19歳"])]["人口"].sum()
        working = df_age[df_age["年齢層"].isin(["20-29歳", "30-39歳", "40-49歳", "50-59歳"])]["人口"].sum()
        elderly = df_age[df_age["年齢層"].isin(["60-69歳", "70-79歳", "80-89歳", "90歳以上"])]["人口"].sum()
        
        df_display = pd.DataFrame({
            "年齢層": ["年少人口（0-19歳）", "生産年齢人口（20-59歳）", "高齢人口（60歳以上）"],
            "人口": [young, working, elderly]
        })
    else:
        df_display = df_age.copy()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 円グラフ
        fig = px.pie(
            df_display, 
            values="人口", 
            names="年齢層",
            title=f"年齢層別人口構成比 ({view_type})"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 棒グラフ
        fig = px.bar(
            df_display, 
            x="年齢層", 
            y="人口",
            title=f"年齢層別人口数 ({view_type})",
            color="年齢層"
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # 人口ピラミッド風の表示（詳細表示時のみ）
    if view_type == "詳細（10歳間隔）":
        st.subheader("📊 年齢分布詳細")
        
        # 横棒グラフで人口ピラミッド風に
        fig_pyramid = px.bar(
            df_age.sort_values("年齢層"), 
            y="年齢層", 
            x="人口",
            orientation='h',
            title="年齢別人口分布（人口ピラミッド風）",
            color="人口",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig_pyramid, use_container_width=True)
    
    # 統計サマリー
    col3, col4, col5 = st.columns(3)
    
    with col3:
        total_pop = df_display["人口"].sum()
        st.metric("総人口", f"{total_pop:,}人")
    
    with col4:
        max_group = df_display.loc[df_display["人口"].idxmax()]
        st.metric("最大人口層", max_group["年齢層"])
        st.caption(f"{max_group['人口']:,}人")
    
    with col5:
        if view_type == "従来分類（年少・生産年齢・高齢）":
            elderly_ratio = (df_display[df_display["年齢層"].str.contains("高齢")]["人口"].sum() / total_pop * 100)
            st.metric("高齢化率", f"{elderly_ratio:.1f}%")
        else:
            elderly_60plus = df_age[df_age["年齢層"].isin(["60-69歳", "70-79歳", "80-89歳", "90歳以上"])]["人口"].sum()
            elderly_ratio = (elderly_60plus / total_pop * 100)
            st.metric("高齢化率（60歳以上）", f"{elderly_ratio:.1f}%")
    
    # 詳細データ
    st.subheader("📋 詳細データ")
    df_display["構成比"] = (df_display["人口"] / df_display["人口"].sum() * 100).round(1)
    df_display["構成比表示"] = df_display["構成比"].astype(str) + "%"
    st.dataframe(df_display, use_container_width=True)

elif data_type == "人口推移":
    st.header("📈 人口推移トレンド")
    
    df_time = load_time_series_data()
    
    # 線グラフ
    fig = px.line(
        df_time, 
        x="年", 
        y="総人口",
        title="日本の総人口推移（2010-2023年）",
        markers=True
    )
    fig.update_layout(
        xaxis_title="年",
        yaxis_title="総人口（人）"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 統計情報
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("2023年人口", f"{df_time['総人口'].iloc[-1]:,}人")
    
    with col2:
        change = df_time['総人口'].iloc[-1] - df_time['総人口'].iloc[0]
        st.metric("2010年からの変化", f"{change:,}人", delta=int(change))
    
    with col3:
        annual_change = change / len(df_time)
        st.metric("年平均変化", f"{annual_change:.0f}人")
    
    with col4:
        change_rate = (change / df_time['総人口'].iloc[0]) * 100
        st.metric("変化率", f"{change_rate:.1f}%")

elif data_type == "人口密度":
    st.header("🏙️ 人口密度分析")
    
    df_pref = load_prefecture_data()
    
    # 人口密度ランキング
    fig = px.bar(
        df_pref.nlargest(20, "人口密度"), 
        x="人口密度", 
        y="都道府県",
        orientation='h',
        title="人口密度トップ20都道府県",
        color="人口密度",
        color_continuous_scale="Reds"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 散布図：人口 vs 人口密度
    fig2 = px.scatter(
        df_pref, 
        x="人口", 
        y="人口密度",
        hover_name="都道府県",
        title="人口と人口密度の関係",
        size="人口",
        color="人口密度",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig2, use_container_width=True)

# フッター
st.markdown("---")
st.markdown("""
**データソース**: サンプルデータ（実際のプロジェクトでは政府統計APIを使用）  
**更新日時**: {}  
**作成**: Streamlit Population Dashboard
""".format(datetime.now().strftime('%Y年%m月%d日 %H:%M')))

# サイドバーにアプリ情報
st.sidebar.markdown("---")
st.sidebar.info("""
このダッシュボードは日本の人口統計データを
インタラクティブに可視化します。

**機能:**
- 都道府県別人口分布
- 年齢別人口構成
- 人口推移トレンド
- 人口密度分析
""")

# 自動更新機能（オプション）
if st.sidebar.checkbox("自動更新（30秒間隔）"):
    time.sleep(30)
    st.rerun()
