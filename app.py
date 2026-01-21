import streamlit as st
import pandas as pd
from datetime import datetime

# BMI 판정 함수
def get_bmi_status(bmi):
    """BMI 수치에 따른 판정 결과 반환"""
    if bmi < 18.5:
        return "저체중", "🔵"
    elif bmi < 23:
        return "정상", "🟢"
    elif bmi < 25:
        return "과체중", "🟡"
    elif bmi < 30:
        return "비만", "🟠"
    else:
        return "고도비만", "🔴"

# 페이지 설정
st.set_page_config(page_title="건강 기록 앱2", page_icon="❤️")
st.title("❤️ 나의 건강 기록")

# 데이터 저장소 초기화
if 'health_data' not in st.session_state:
    st.session_state.health_data = []

# --- 입력 영역 ---
st.subheader("📝 오늘의 건강 기록")

col1, col2, col3, col4 = st.columns(4)

with col1:
    date = st.date_input("날짜", datetime.now())

with col2:
    height = st.number_input(
        "키 (cm)",
        min_value=100.0,
        max_value=250.0,
        value=170.0,
        step=0.1
    )

with col3:
    weight = st.number_input(
        "체중 (kg)",
        min_value=30.0,
        max_value=200.0,
        value=65.0,
        step=0.1
    )

with col4:
    systolic = st.number_input(
        "수축기 혈압",
        min_value=80,
        max_value=200,
        value=120
    )
    diastolic = st.number_input(
        "이완기 혈압",
        min_value=50,
        max_value=150,
        value=80
    )

# --- 실시간 BMI 표시 ---
st.divider()
st.subheader("⚖️ 현재 BMI")

height_m = height / 100
current_bmi = weight / (height_m ** 2)
status, emoji = get_bmi_status(current_bmi)

bmi_col1, bmi_col2, bmi_col3 = st.columns(3)

with bmi_col1:
    st.metric("BMI 수치", f"{current_bmi:.1f}")

with bmi_col2:
    st.metric("판정", f"{emoji} {status}")

with bmi_col3:
    st.metric("정상 범위", "18.5 ~ 22.9")

st.divider()

# 저장 버튼
if st.button("💾 기록 저장", type="primary"):
    new_record = {
        "날짜": date,
        "키": height,
        "체중": weight,
        "BMI": round(current_bmi, 1),
        "수축기": systolic,
        "이완기": diastolic
    }
    st.session_state.health_data.append(new_record)
    st.success(f"저장되었습니다! BMI: {current_bmi:.1f} ({status})")

# --- 기록 보기 ---
if st.session_state.health_data:
    st.divider()
    st.subheader("📊 나의 건강 기록")
    
    df = pd.DataFrame(st.session_state.health_data)
    df = df.sort_values("날짜")
    
    st.dataframe(df, use_container_width=True)
    
    # ========== 삭제 기능 ==========
    st.subheader("🗑️ 기록 삭제")
    
    del_col1, del_col2, del_col3 = st.columns(3)
    
    # 마지막 기록 삭제
    with del_col1:
        if st.button("마지막 기록 삭제"):
            st.session_state.health_data.pop()  # 마지막 항목 제거
            st.warning("마지막 기록이 삭제되었습니다.")
            st.rerun()  # 화면 새로고침
    
    # 전체 기록 삭제
    with del_col2:
        if st.button("⚠️ 전체 기록 삭제"):
            st.session_state.delete_confirm = True
    
    # 선택 삭제
    with del_col3:
        if len(st.session_state.health_data) > 0:
            delete_index = st.selectbox(
                "삭제할 기록 선택",
                range(len(st.session_state.health_data)),
                format_func=lambda x: f"{st.session_state.health_data[x]['날짜']} - {st.session_state.health_data[x]['체중']}kg"
            )
            if st.button("선택 항목 삭제"):
                del st.session_state.health_data[delete_index]
                st.warning("선택한 기록이 삭제되었습니다.")
                st.rerun()
    
    # 전체 삭제 확인 (별도 영역)
    if st.session_state.get('delete_confirm', False):
        st.error("⚠️ 정말 모든 기록을 삭제하시겠습니까?")
        confirm_col1, confirm_col2 = st.columns(2)
        with confirm_col1:
            if st.button("✅ 예, 삭제합니다", type="primary"):
                st.session_state.health_data = []  # 전체 삭제
                st.session_state.delete_confirm = False
                st.success("모든 기록이 삭제되었습니다.")
                st.rerun()
        with confirm_col2:
            if st.button("❌ 취소"):
                st.session_state.delete_confirm = False
                st.rerun()
    # ================================
    
    st.divider()
    
    # 그래프 탭
    tab1, tab2, tab3 = st.tabs(["체중 변화", "BMI 변화", "혈압 변화"])
    
    with tab1:
        st.line_chart(df.set_index("날짜")["체중"])
        
    with tab2:
        st.line_chart(df.set_index("날짜")["BMI"])
        
    with tab3:
        st.line_chart(df.set_index("날짜")[["수축기", "이완기"]])
        
else:
    st.info("아직 기록이 없습니다. 위에서 건강 정보를 입력해주세요!")
