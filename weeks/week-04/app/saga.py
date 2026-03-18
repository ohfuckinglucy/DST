
# Реализуйте здесь простую машину состояний (State Machine).
# Функция должна принимать текущее состояние и событие,
# и возвращать следующее состояние.

def next_state(state: str, event: str) -> str:
    transitions = {
        ('NEW', 'PAY_OK'):   'PAID',
        ('NEW', 'PAY_FAIL'): 'CANCELLED',
        ('PAID', 'DONE'):    'DONE',
    }
    return transitions.get((state, event), 'CANCELLED')


def compensate(state: str) -> str:
    if state == 'NEW':
        return 'CANCELLED'
    return state

def run_saga(invoice_id: int, amount: float) -> str:
    state = 'NEW'

    payment_ok = process_payment(amount)

    if payment_ok:
        state = next_state(state, 'PAY_OK')
        state = next_state(state, 'DONE')
    else:
        release_with_retry()
        state = compensate(state)

    return state

def release_with_retry(max_retries: int = 3) -> bool:
    for attempt in range(max_retries):
        success = cancel_reserve()
        if success:
            return True
        print(f"Попытка {attempt + 1} не удалась, повторяем...")
    return False

def cancel_reserve() -> bool:
    return True

def process_payment(amount: float) -> bool:
    return True
