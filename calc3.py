import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.title("Кредитный калькулятор")

# Ввод данных пользователя
with st.form("credit_form"):
    st.subheader("Введите параметры кредита")
    loan_amount = st.number_input("Сумма кредита (₽)", min_value=0.01, step=1000.0)
    annual_rate = st.number_input("Годовая процентная ставка (%)", min_value=0.0, step=0.1)
    term_months = st.number_input("Срок кредита (месяцев)", min_value=1, step=1)

    payment_type = st.radio(
        "Тип платежа",
        ("Аннуитетный", "Дифференциальный")
    )

    start_date_str = st.text_input("Дата первого платежа (гггг-мм-дд)", value=str(datetime.today().date()))
    submitted = st.form_submit_button("Рассчитать")

if not submitted:
    st.info("Пожалуйста, заполните все параметры и нажмите 'Рассчитать'")
    st.stop()

# Проверка формата даты
try:
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
except ValueError:
    st.error("Некорректный формат даты. Используйте формат YYYY-MM-DD.")
    st.stop()

# Проверка числовых параметров
if loan_amount <= 0 or annual_rate < 0 or term_months <= 0:
    st.error("Пожалуйста, убедитесь, что все числа введены правильно.")
    st.stop()

# Месячная ставка
monthly_rate = annual_rate / 12 / 100

# Функция для расчёта аннуитетных платежей
def calculate_annuity_payments(principal, rate, months):
    if rate == 0:
        # Без процентов
        payment = principal / months
        return [payment] * months
    else:
        discount_factor = (rate * (1 + rate) ** months) / ((1 + rate) ** months - 1)
        payment = principal * discount_factor
        return [payment] * months

# Создаем список для выплат, если нужен аннуитет
if payment_type == "Аннуитетный":
    payments = calculate_annuity_payments(loan_amount, monthly_rate, term_months)
else:
    payments = []

# Создаем таблицу для выплат
schedule = []

# Изначально остаток долга
remaining_principal = loan_amount

# Месячная дата
for month in range(1, term_months + 1):
    begin_balance = remaining_principal  # Остаток на начало периода

    if payment_type == "Дифференцированный":
        principal_payment = loan_amount / term_months
        interest = begin_balance * monthly_rate
        total_payment = principal_payment + interest
        remaining_principal -= principal_payment
        remaining_principal = max(remaining_principal, 0)
        end_balance = remaining_principal
    else:
        # Аннуитетный платеж
        total_payment = payments[month - 1]
        interest = begin_balance * monthly_rate
        principal_part = total_payment - interest
        remaining_principal -= principal_part
        remaining_principal = max(remaining_principal, 0)
        end_balance = remaining_principal

    # Запись в таблицу
    schedule.append({
        "Месяц": month,
        "Дата": (start_date + timedelta(days=30 * month)).date(),
        "Остаток долга (начало)": round(begin_balance, 2),
        "Ежемесячный платеж": round(total_payment, 2),
        "Процентная часть": round(interest, 2),
        "Долговая часть": round(total_payment - interest, 2),
        "Остаток долга (конец)": round(end_balance, 2)
    })

# Создаем DataFrame для отображения
df = pd.DataFrame(schedule)

# Отображение графика
st.subheader("График погашения")
st.dataframe(df)

# Подсчет итогов
total_payments = df["Ежемесячный платеж"].sum()
total_interest = df["Процентная часть"].sum()

# Вывод итогов
st.markdown(f"### Итоги")
st.write(f"Общая сумма платежей: **{total_payments:.2f} ₽**")
st.write(f"Общая сумма процентов: **{total_interest:.2f} ₽**")