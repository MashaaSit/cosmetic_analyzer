import streamlit as st
from analyzer import calculate_risk
st.title('Cosmetic Acne Risk Analyzer')

product = st.text_input('Введите название косметического средства:')
composition = st.text_area('Введите состав продукта (через запятую):')
# product_ = 'Orlane Paris Concentre Vitamin C 153 mg, Energizing,1 fl oz/30 mL'
# composition_ = 'Acrylates/C10-30 Alkyl Acrylate Crosspolymer, Aqua (Water), Glycerin, Magnesium Ascorbyl Phosphate, Pentylene Glycol, Phenoxyethanol, Tetrasodium Edta, Triethanolamine'
calculate_button = st.button('Рассчитать риск')
if calculate_button:
    result = calculate_risk(composition.split(','))
    if result <= -0.5:
        st.write(f'Результат расчета {result}. Данное средство безопасно для ежедневного применения и подходит для чувствительной кожи ')
    elif result > -0.5 and result <= 0.5:
        st.write(f'Результат расчета {result}. Данное средство рекомендуется применять 1-2 раза в неделю, есть риски появления воспалений.')
    else:
        st.write(f'Результат расчета {result}. Данное средство с большей вероятностью приводит к проявлению аллергической реакции')

         
