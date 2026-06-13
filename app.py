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
    priority: str

# 상태 초기화 함수
def init_session_state() -> None:
    """세션 상태를 초기화합니다."""
    if TODO_SESSION_KEY not in st.session_state:
        st.session_state[TODO_SESSION_KEY] = []

# 핵심 로직 함수들 (UI와 분리)
def add_todo(task: str, due_date: Optional[date] = None, priority: str = "보통") -> None:
    """새로운 할 일을 추가합니다."""
    if not task.strip():
        return
    new_todo: TodoItem = {
        "id": str(uuid.uuid4()),
        "task": task.strip(),
        "completed": False,
        "due_date": due_date,
        "priority": priority
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
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            priority = st.selectbox("우선순위", ["높음", "보통", "낮음"], index=1)
        with col2:
            use_due_date = st.checkbox("마감일 설정")
        with col3:
            due_date = st.date_input("마감일 선택", value="today")
        submitted = st.form_submit_button("추가")
        if submitted and new_task:
            final_due_date = due_date if use_due_date else None
            add_todo(new_task, final_due_date, priority)
            st.rerun()

    # 사이드바 (정렬/필터)
    with st.sidebar:
        st.header("설정")
        sort_by = st.selectbox("정렬 기준", ["기본 (추가순)", "우선순위 (높음 ➡ 낮음)", "마감일 (빠른순)"])

    # 정렬 로직 적용
    display_todos = todos.copy()
    if sort_by == "우선순위 (높음 ➡ 낮음)":
        priority_map = {"높음": 1, "보통": 2, "낮음": 3}
        display_todos.sort(key=lambda x: priority_map.get(x.get("priority", "보통"), 2))
    elif sort_by == "마감일 (빠른순)":
        MAX_DATE = date.max
        display_todos.sort(key=lambda x: x.get("due_date") or MAX_DATE)

    # 할 일 목록 표시
    st.markdown("---")
    for todo in display_todos:
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            # 상태 아이콘 표시 및 텍스트 구성
            icon = "✅" if todo["completed"] else "⬜"
            item_priority = todo.get("priority", "보통")
            base_text = f"{icon} [{item_priority}] {todo['task']}"
            label_text = base_text
            
            item_due_date = todo.get("due_date")
            if item_due_date:
                due_date_str = item_due_date.strftime("%Y-%m-%d")
                is_overdue = not todo["completed"] and item_due_date < date.today()
                if is_overdue:
                    label_text = f":red[{base_text} (마감: {due_date_str})]"
                else:
                    label_text = f"{base_text} (마감: {due_date_str})"

            # 체크박스로 완료 상태 표시 및 토글
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
