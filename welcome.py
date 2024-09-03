import streamlit as st
#title örneği
st.title('Hello Canim')
#subheader örneği
st.subheader('Nettin')
#header örneği
st.header('Goca Başlık')
#text örneği
st.text('Burası bir text')
#markdown örneği
st.markdown('Bu markdown, **bu da kalını** ve bu da *italik* ve # kalın # ')
#markdown link örneği
st.markdown('[Google](https://google.com)')
#caption örneği
st.caption('Merhaba ben captionım')

#json oluşturuyoruz.
json={
    'İsim': 'Emre',
    'Sınıf' : '5'
    }
#oluşturduğumuz jsonı gönderiyoruz.
st.json(json)

#eğer kod örneği göndermek istersek code parametresini kullanacağız.
#code görünümü arayüzde farklı.
code="""
def func():
    return 1;"""
st.code(code)


