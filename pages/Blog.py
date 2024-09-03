import streamlit as st
from constants.functions import page_header_infos

page_header_infos(title='Charts')

# Verileri temsil eden örnek liste
articles = [
   {
        "title": "Gartner Says CRM Will Be at the Heart of Digital Initiatives for Years to Come",
        "date": "February 12, 2014",
        "image": "images/gartner.jpeg",
        "link": "https://www.gartner.com/en/newsroom/press-releases/2014-02-12-gartner-says-crm-will-be-at-the-heart-of-digital-initiatives-for-years-to-come"
    },
    {
        "title": "Decreasing churn: How to use win-loss analysis to effectively drive net retention",
        "date": "February 22, 2024",
        "image": "images/cx.jpeg",
        "link": "https://www.cxnetwork.com/customer-churn/videos/decreasing-churn-how-to-use-win-loss-analysis-to-effectively-drive-net-retention"
    },
    {
        "title": "What Is Churn Rate and How Is It Calculated? (2024 Guide)",
        "date": "Jun 28, 2024",
        "image": "images/market_watch.jpeg",
        "link": "https://www.marketwatch.com/guides/business/churn-rate/"
    },
    {
        "title": "TBI Tech & Analysis: How Foxtel’s Hubbl is tackling subscriber churn",
        "date": "April 15, 2024",
        "image": "images/tbi.jpeg",
        "link": "https://tbivision.com/2024/04/15/tbi-tech-analysis-how-foxtels-hubbl-is-tackling-subscriber-churn/#close-modal"
    }
]

# Streamlit uygulaması
st.title("Blog")

for article in articles:
    col1, col2 = st.columns([1, 4])
    
    with col1:
        # Resim sadece gösterilir, tıklanabilir değildir
        st.image(article["image"], width=150)
    
    with col2:
        # Başlık tıklanabilir olarak ayarlanır
        st.markdown(f"[**{article['title']}**]({article['link']})")
        st.text(f"{article['date']}")

    st.markdown("---")  # Ayırıcı çizgi
