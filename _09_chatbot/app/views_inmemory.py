"""DB history와 비교하는 메모리 저장소 예제이며 URL에 연결하지 않는다."""
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage


def memory_history_example():
    # DatabaseChatMessageHistory와 같은 messages/add_messages/clear 인터페이스를 사용한다.
    # 객체를 잃거나 프로세스를 재시작하면 내용도 사라지며 다른 worker와 공유되지 않는다.
    history = InMemoryChatMessageHistory()
    history.add_messages([HumanMessage(content='백엔드를 배우고 싶어요.'),
                          AIMessage(content='HTTP와 Python부터 연습해 보세요.')])
    return history