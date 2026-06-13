import streamlit as st
import uuid
from typing import TypedDict, List, Optional
from datetime import date

# 상수 정의
PAGE_TITLE = "할 일(To-Do) 앱"
SUMMARY_TEXT_FORMAT = "✅ 완료: {completed_count} / ❌ 미완료: {uncompleted_count}"
TODO_SESSION_KEY = "todos"

# 타입 정의
class TodoItem(TypedDict):
    id: str
    task: str
    completed: bool
    due_date: Optional[date]

# 상태 초기화 함수
def init_session_state() -> None:
    """세션 상태를 초기화합니다."""
    if TODO_SESSION_KEY not in st.session_state:
        st.session_state[TODO_SESSION_KEY] = []

# 핵심 로직 함수들 (UI와 분리)
def add_todo(task: str, due_date: Optional[date] = None) -> None:
    """새로운 할 일을 추가합니다."""
    if not task.strip():
        return
    new_todo: TodoItem = {
        "id": str(uuid.uuid4()),
        "task": task.strip(),
        "completed": False,
        "due_date": due_date
    }
    st.session_state[TODO_SESSION_KEY].append(new_todo)

def toggle_todo(todo_id: str) -> None:
    """특정 할 일의 완료 여부를 토글합니다."""
    for todo in st.session_state[TODO_SESSION_KEY]:
        if todo["id"] == todo_id:
            todo["completed"] = not todo["completed"]
            break

def delete_todo(todo_id: str) -> None:
    """특정 할 일을 삭제합니다."""
    st.session_state[TODO_SESSION_KEY] = [
        todo for todo in st.session_state[TODO_SESSION_KEY] 
        if todo["id"] != todo_id
    ]

# UI 렌더링
def main() -> None:
    st.set_page_config(page_title=PAGE_TITLE, page_icon="📝")
    init_session_state()

    st.title(PAGE_TITLE)

    # 요약 정보 계산 및 표시
    todos: List[TodoItem] = st.session_state[TODO_SESSION_KEY]
    completed_count = sum(1 for todo in todos if todo["completed"])
    uncompleted_count = len(todos) - completed_count

    st.subheader(SUMMARY_TEXT_FORMAT.format(
        completed_count=completed_count, 
        uncompleted_count=uncompleted_count
    ))

    # 할 일 추가 폼
    with st.form("add_todo_form", clear_on_submit=True):
        new_task = st.text_input("새로운 할 일을 입력하세요", placeholder="예: 코딩 공부하기")
        col1, col2 = st.columns(2)
        with col1:
            use_due_date = st.checkbox("마감일 설정")
        with col2:
            due_date = st.date_input("마감일 선택", value="today")
        submitted = st.form_submit_button("추가")
        if submitted and new_task:
            final_due_date = due_date if use_due_date else None
            add_todo(new_task, final_due_date)
            st.rerun()

    # 할 일 목록 표시
    st.markdown("---")
    for todo in todos:
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            # 체크박스로 완료 상태 표시 및 토글
            label_text = todo["task"]
            item_due_date = todo.get("due_date")
            
            if item_due_date:
                due_date_str = item_due_date.strftime("%Y-%m-%d")
                is_overdue = not todo["completed"] and item_due_date < date.today()
                if is_overdue:
                    label_text = f":red[{todo['task']} (마감: {due_date_str})]"
                else:
                    label_text = f"{todo['task']} (마감: {due_date_str})"

            is_completed = st.checkbox(
                label_text, 
                value=todo["completed"], 
                key=f"check_{todo['id']}"
            )
            if is_completed != todo["completed"]:
                toggle_todo(todo["id"])
                st.rerun()
        with col2:
            # 삭제 버튼
            if st.button("삭제", key=f"del_{todo['id']}"):
                delete_todo(todo["id"])
                st.rerun()

if __name__ == "__main__":
    main()
