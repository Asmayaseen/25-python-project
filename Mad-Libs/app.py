import streamlit as st # type: ignore

def generate_story(noun, verb, adjective, place):
    story = f"Ek {adjective} {noun} ne decide kiya ke wo {place} jayega. Wahan jaake usne {verb} kiya aur sab log hairan reh gaye!"
    return story

st.title('Mad Libs - Python Fun Project')
st.write("Apni Mad Libs story banaiye! Niche inputs fill karen.")

noun = st.text_input('Koi noun likhiye (e.g., kutta, ladka, car)')
verb = st.text_input('Koi verb likhiye (e.g., nacha, bhaga, soya)')
adjective = st.text_input('Koi adjective likhiye (e.g., pyara, tez, chota)')
place = st.text_input('Koi jagah ka naam likhiye (e.g., school, park, bazar)')

if st.button('Generate Story'):
    if noun and verb and adjective and place:
        story = generate_story(noun, verb, adjective, place)
        st.success('Yahan aapki story hai!')
        st.write(story)
    else:
        st.warning('Please sab fields fill karen!')
