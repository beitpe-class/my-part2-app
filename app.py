import streamlit as st

# 상수 정의
APP_TITLE = "할 일(To-Do) 관리"
TASK_INPUT_LABEL = "새로운 할 일"
ADD_BUTTON_LABEL = "추가"
SUMMARY_FORMAT = "완료: {completed} / 미완료: {uncompleted}"
SESSION_TASKS_KEY = "tasks"

# Lucide Icons (SVG)
ICON_CLIPBOARD = '''<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: bottom; margin-right: 8px;"><rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/></svg>'''
ICON_SEARCH = '''<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 8px;"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>'''
ICON_FILTER = '''<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 8px;"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>'''

def init_state() -> None:
    """세션 상태 초기화 함수"""
    if SESSION_TASKS_KEY not in st.session_state:
        st.session_state[SESSION_TASKS_KEY] = []

def add_task(task_name: str) -> None:
    """새로운 할 일을 추가하는 함수"""
    if task_name.strip():
        st.session_state[SESSION_TASKS_KEY].append({"name": task_name.strip(), "done": False})

def toggle_task(task_index: int) -> None:
    """할 일의 완료 상태를 토글하는 함수"""
    task = st.session_state[SESSION_TASKS_KEY][task_index]
    task["done"] = not task["done"]

def delete_task(task_index: int) -> None:
    """할 일을 삭제하는 함수"""
    st.session_state[SESSION_TASKS_KEY].pop(task_index)

def get_summary() -> tuple[int, int]:
    """완료된 항목과 미완료 항목의 개수를 반환하는 함수"""
    completed = sum(1 for task in st.session_state[SESSION_TASKS_KEY] if task["done"])
    uncompleted = len(st.session_state[SESSION_TASKS_KEY]) - completed
    return completed, uncompleted

def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="📝")
    
    # 타이틀에 Lucide 아이콘 적용
    st.markdown(f"<h1>{ICON_CLIPBOARD} {APP_TITLE}</h1>", unsafe_allow_html=True)
    
    init_state()
    
    # 사이드바: 검색 및 필터 위젯 배치
    st.sidebar.markdown(f"### {ICON_SEARCH} 검색", unsafe_allow_html=True)
    search_query = st.sidebar.text_input("할 일 검색", label_visibility="collapsed", placeholder="검색어를 입력하세요...")
    
    st.sidebar.markdown(f"### {ICON_FILTER} 필터", unsafe_allow_html=True)
    filter_option = st.sidebar.radio("상태 필터", ["전체 보기", "완료된 항목", "미완료 항목"], label_visibility="collapsed")
    
    # 요약 정보 표시
    completed, uncompleted = get_summary()
    st.write(SUMMARY_FORMAT.format(completed=completed, uncompleted=uncompleted))
    st.divider()
    
    # 할 일 추가 입력 폼
    with st.form("add_task_form", clear_on_submit=True):
        new_task = st.text_input(TASK_INPUT_LABEL, placeholder="예: Streamlit 앱 개발하기")
        submitted = st.form_submit_button(ADD_BUTTON_LABEL)
        if submitted and new_task:
            add_task(new_task)
            st.rerun()
            
    # 필터 및 검색 적용된 목록 생성
    filtered_tasks = []
    for i, task in enumerate(st.session_state[SESSION_TASKS_KEY]):
        if search_query and search_query.lower() not in task["name"].lower():
            continue
        if filter_option == "완료된 항목" and not task["done"]:
            continue
        if filter_option == "미완료 항목" and task["done"]:
            continue
        filtered_tasks.append((i, task))

    # 할 일 목록 표시 (상태 아이콘 적용)
    if not filtered_tasks:
        st.info("조건에 맞는 할 일이 없습니다.")
    else:
        for i, task in filtered_tasks:
            col1, col2 = st.columns([0.85, 0.15])
            with col1:
                # 목록 항목엔 상태 아이콘 표시 (완료 ✅ / 미완료 ⬜)
                status_icon = "✅" if task["done"] else "⬜"
                st.checkbox(
                    f"{status_icon} {task['name']}",
                    value=task["done"],
                    key=f"check_{i}",
                    on_change=toggle_task,
                    args=(i,)
                )
            with col2:
                if st.button("❌", key=f"del_{i}", help="삭제"):
                    delete_task(i)
                    st.rerun()

if __name__ == "__main__":
    main()
