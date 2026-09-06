import streamlit as st

# 상수 정의
APP_TITLE = "할 일(To-Do) 관리"
TASK_INPUT_LABEL = "새로운 할 일"
ADD_BUTTON_LABEL = "추가"
SUMMARY_FORMAT = "완료: {completed} / 미완료: {uncompleted}"
SESSION_TASKS_KEY = "tasks"

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
    st.title(APP_TITLE)
    
    init_state()
    
    # 요약 정보 표시
    completed, uncompleted = get_summary()
    st.write(SUMMARY_FORMAT.format(completed=completed, uncompleted=uncompleted))
    st.divider()
    
    # 할 일 추가 입력 폼
    with st.form("add_task_form", clear_on_submit=True):
        new_task = st.text_input(TASK_INPUT_LABEL)
        submitted = st.form_submit_button(ADD_BUTTON_LABEL)
        if submitted and new_task:
            add_task(new_task)
            st.rerun()
            
    # 할 일 목록 표시
    for i, task in enumerate(st.session_state[SESSION_TASKS_KEY]):
        col1, col2 = st.columns([0.9, 0.1])
        with col1:
            st.checkbox(task["name"], value=task["done"], key=f"check_{i}", on_change=toggle_task, args=(i,))
        with col2:
            if st.button("❌", key=f"del_{i}"):
                delete_task(i)
                st.rerun()

if __name__ == "__main__":
    main()
