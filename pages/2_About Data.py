import streamlit as st
import pandas as pd
from constants.functions import page_header_infos

page_header_infos(title='Data')
st.title('Data Information')
st.image('images/homepage.jpeg')

df=pd.read_csv('ecommerce_last.csv')
st.markdown("**Data Dictionary**")
st.markdown("""| Variable                 | Description                                                      |
|--------------------------|------------------------------------------------------------------|
| *CustomerID*            | Unique customer ID                                              |
| *Churn*                 | Churn Flag                                                      |
| *Tenure*                | Tenure of customer in organization                              |
| *PreferredLoginDevice*  | Preferred login device of customer                              |
| *CityTier*              | City tier                                                       |
| *WarehouseToHome*       | Distance in between warehouse to home of customer               |
| *PreferredPaymentMode*  | Preferred payment method of customer                            |
| *Gender*                | Gender of customer                                              |
| *HourSpendOnApp*        | Number of hours spend on mobile application or website          |
| *NumberOfDeviceRegistered* | Total number of devices registered on particular customer   |
| *PreferedOrderCat*      | Preferred order category of customer in last month              |
| *SatisfactionScore*     | Satisfactory score of customer on service                       |
| *MaritalStatus*         | Marital status of customer                                      |
| *NumberOfAddress*       | Total number of addresses added on particular customer          |
| *Complain*              | Any complaint has been raised in last month                     |
| *OrderAmountHikeFromlastYear* | Percentage increase in order from last year              |
| *CouponUsed*            | Total number of coupons used in last month                      |
| *OrderCount*            | Total number of orders placed in last month                     |
| *DaySinceLastOrder*     | Day since last order by customer                                |
| *CashbackAmount*        | Average cashback in last month                                  |""")

st.markdown('**Initial Churn Distribution**')
st.dataframe(df['Churn'].value_counts())

churn_status = st.selectbox("**Churn Status Selection**", df["Churn"].unique())
filtered_df = df[df["Churn"] == churn_status]
st.dataframe(filtered_df.sample(10), hide_index=True)


