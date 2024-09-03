import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from joblib import load
from datetime import date, datetime
import shap
import pickle
import numba
from sklearn.preprocessing import OneHotEncoder
from constants.functions import page_header_infos

page_header_infos(title='Predict')
st.title('Prediction')
#öncelikle kullanıcıdan alacağımız bilgilerin giriş ekrannı tasarlayacağız.
tenure = st.number_input("Tenure (Month)", help="Please enter Tenure as a number!", min_value=0, format='%d', value=0)
#tenure değişkeni sayı olarak girilmelidir. bu yüzden number_input kullandım.
#min_value en az değeri gösterir. format ise , den sonra sayı gösterip göstermemeyi düzenler.
#'%d' dersem 1 olarak görünür. '%.2f' ondalıklı göterilir. '%.0f' yuvarlar. '%,d' çok haneli sayıları virgülle ayırır.
#index=0 ve value=0 tüm değerlere atandı. sebebi null hatası oluşmamasıdır. 
#bu değerleri atayarak sayfa açılışında tüm alanlara değer atamış oluyoruz.
#CouponUsed değeri 1 olarak atanıyor. Çünkü bölme işleminin paydası. 0 değerini alırsa hata alırız.
preferredLoginDevice=st.selectbox('Preferred Login Device', ['Mobile Phone', 'Computer'],index=0)
#cityTier=st.number_input("City Tier (1-3)", help="Please enter CityTier as a number!",min_value=1, max_value=3, format='%d', value=1)
cityTier=st.selectbox('City Tier', ['Most developed cities', 'Moderately developed cities', 'Least developed cities'],index=0)
warehouseToHome=st.number_input("Warehouse To Home (KM)", help="Please enter WarehouseToHome as a number!",min_value=0, format='%d', value=0)
preferredPaymentMode=st.selectbox('Preferred Payment Mode', ['Debit Card', 'UPI', 'Credit Card', 'Cash on Delivery', 'E wallet'],index=0)
gender=st.selectbox('Gender', ['Female', 'Male'],index=0)
hourSpendOnApp=st.number_input("Hour Spend On App", help="Please enter HourSpendOnApp as a number!",min_value=0, format='%d', value=0)
numberOfDeviceRegistered=st.number_input("Number Of Device Registered", help="Please enter NumberOfDeviceRegistered as a number!",min_value=0, format='%d')
preferedOrderCat=st.selectbox('Prefered Order Category', ['Laptop & Accessory', 'Mobile Phone', 'Fashion','Grocery','Others'],index=0)
satisfactionScore=st.selectbox('Satisfaction Score', ['1', '2', '3','4','5'],index=0)
maritalStatus=st.selectbox('Marital Status', ['Single', 'Divorced', 'Married'],index=0)
numberOfAddress=st.number_input("Number Of Address", help="Please enter NumberOfAddress as a number!",min_value=0, format='%d', value=0)
complain=st.selectbox('Complaint', ['0', '1'],index=0)
orderAmountHikeFromlastYear=st.number_input("Order Amount Hike From Last Year", help="Please enter OrderAmountHikeFromlastYear as a number!",min_value=0, format='%d', value=0)
couponUsed=st.number_input("Coupon Used", help="Please enter CouponUsed as a number!",min_value=1, format='%d', value=1)
orderCount=st.number_input("Order Count", help="Please enter OrderCount as a number!",min_value=0, format='%d', value=0)
daySinceLastOrder=st.number_input("Day SinceLast Order", help="Please enter DaySinceLastOrder as a number!",min_value=0, format='%d', value=0)
cashbackAmount=st.number_input("Cashback Amount", help="Please enter CashbackAmount as a number!",min_value=0, format='%d', value=0)

#couponPerOrder=couponUsed/orderCount
#bu işlem şimdilik geçersiz. çünkü initial value ya 1 değerini verdik.
if(orderCount!=0):
    couponPerOrder=couponUsed/orderCount
else:
    couponPerOrder=0

if(cityTier=='Most developed cities'):
    cityTierVal=1
elif(cityTier=='Moderately developed cities'):
    cityTierVal=2
else:
    cityTierVal=3

#modelimizi yüklüyoruz. random_forest_model.pkl dosyasını notebookdaki son modelimden getiriyorum.
rf_model=load('random_forest_model.pkl')

#yukarıdaki değişkenlerimden bir dataframe oluşturuyorum. 
input_data = pd.DataFrame({
    'Tenure': [tenure],
    'PreferredLoginDevice':[preferredLoginDevice],
    'CityTier':[cityTierVal],
    'WarehouseToHome':[warehouseToHome],
    'PreferredPaymentMode':[preferredPaymentMode],
    'Gender':[gender],
    'HourSpendOnApp':[hourSpendOnApp],
    'NumberOfDeviceRegistered':[numberOfDeviceRegistered],
    'PreferedOrderCat':[preferedOrderCat],
    'SatisfactionScore':[satisfactionScore],
    'MaritalStatus':[maritalStatus],
    'NumberOfAddress':[numberOfAddress],
    'Complain':[complain],
    'OrderAmountHikeFromlastYear':[orderAmountHikeFromlastYear],
    'CouponUsed':[couponUsed],
    'OrderCount':[orderCount],
    'DaySinceLastOrder':[daySinceLastOrder],
    'CashbackAmount':[cashbackAmount],
})

#kategorik değişkenlerimi belirliyorum. Çünkü one hot encoding işlemi yapacağım.
categorical_columns=['PreferredLoginDevice', 'PreferredPaymentMode', 'Gender', 'PreferedOrderCat', 'MaritalStatus']

#verileri kontrol için kullandığım alanlar.
#st.write(input_data.info())
#st.write(input_data[categorical_columns])


#one hot encoding sırasında hangi sütunların işleneceğini belirtiyorum. bunu yapmazsam sorun oluyor.
ohe = OneHotEncoder(sparse_output=False, categories=[
    ['Mobile Phone', 'Computer'],
    ['Debit Card', 'UPI', 'Credit Card', 'Cash on Delivery', 'E wallet'],
    ['Female', 'Male'],
    ['Laptop & Accessory', 'Mobile Phone', 'Fashion', 'Grocery', 'Others'],
    ['Single', 'Divorced', 'Married']
])

# kategorik sütunları fit ediyorum. üstte oluşturmuştum categorical_columns kısmını
ohe_df = pd.DataFrame(ohe.fit_transform(input_data[categorical_columns]), 
                      columns=ohe.get_feature_names_out(categorical_columns))

# dataframeleri birleştiriyorum.
df_encoded = pd.concat([input_data.reset_index(drop=True).drop(categorical_columns, axis=1), 
                        ohe_df.reset_index(drop=True)], axis=1)

#artık manuel drop ediyorum çıkaracağım sütunları.
df_encoded=df_encoded.drop(columns=[
    'PreferredPaymentMode_Cash on Delivery',
    'PreferedOrderCat_Grocery',
    'PreferredPaymentMode_UPI',
    'MaritalStatus_Divorced',
    'PreferedOrderCat_Others',
    'CouponUsed'
])

#feature enginering ile oluşturduğum yeni feature ı dataframe e ekliyorum.
df_encoded['CouponPerOrder']=couponPerOrder

#henüz belirleyemediğim bir sebeple sütunlar farklı sıralamada geliyor.
#bu yüzden doğru sıraya sokuyorum.
last_column = [
    'Tenure', 'CityTier', 'WarehouseToHome', 'HourSpendOnApp',
    'NumberOfDeviceRegistered', 'SatisfactionScore', 'NumberOfAddress',
    'Complain', 'OrderAmountHikeFromlastYear', 'OrderCount',
    'DaySinceLastOrder', 'CashbackAmount', 'PreferredLoginDevice_Computer',
    'PreferredLoginDevice_Mobile Phone', 'PreferredPaymentMode_Credit Card',
    'PreferredPaymentMode_Debit Card', 'PreferredPaymentMode_E wallet',
    'Gender_Female', 'Gender_Male', 'PreferedOrderCat_Fashion',
    'PreferedOrderCat_Laptop & Accessory', 'PreferedOrderCat_Mobile Phone',
    'MaritalStatus_Married', 'MaritalStatus_Single', 'CouponPerOrder'
]

#yeni sütun sıralamamla tekrar güncelliyorum. Verilere dokunmuyoruz, sadece sütun sıraları düzenleniyor.
df_encoded = df_encoded.reindex(columns=last_column)

#verileri kontrol için kullandığım alanlar.
#st.write(ohe_df.columns)
#st.write(df_encoded.columns)
#st.write(len(df_encoded.columns))


# Model tahminini yaptığım alan.
prediction = rf_model.predict(df_encoded)
online_pred_probability = rf_model.predict_proba(df_encoded)

#
## Tahmin sonucunu ekranda gösterin
#st.write(f"Churn Tahmini: {'Evet' if prediction[0] == 1 else 'Hayır'}")

st.header("Results")

# Sonuç Ekranı
if st.button("Submit"):

    # Info mesajı oluşturma
    st.info("You can find the prediction results below.")

    today = date.today()
    time = datetime.now().strftime("%H:%M:%S")

    # Sonuçları Görüntülemek için DataFrame
    online_results_df = pd.DataFrame({
         'Tenure': [tenure],
 'PreferredLoginDevice':[preferredLoginDevice],
 'CityTier':[cityTierVal],
 'WarehouseToHome':[warehouseToHome],
 'PreferredPaymentMode':[preferredPaymentMode],
 'Gender':[gender],
 'HourSpendOnApp':[hourSpendOnApp],
 'NumberOfDeviceRegistered':[numberOfDeviceRegistered],
 'PreferedOrderCat':[preferedOrderCat],
 'SatisfactionScore':[satisfactionScore],
 'MaritalStatus':[maritalStatus],
 'NumberOfAddress':[numberOfAddress],
 'Complain':[complain],
 'OrderAmountHikeFromlastYear':[orderAmountHikeFromlastYear],
 'CouponUsed':[couponUsed],
 'OrderCount':[orderCount],
 'DaySinceLastOrder':[daySinceLastOrder],
 'CashbackAmount':[cashbackAmount],
    })
    st.write(f"Churn Tahmini: {prediction[0]}")

    st.dataframe(online_results_df)
    X_test5=pd.read_csv('X_test5.csv')

    explainer_last = shap.Explainer(rf_model)
    shap_val_class_last = explainer_last(X_test5)

    #with open("explainer3.pkl", "rb") as explainer:
    #   explainer = pickle.load(explainer)

    with open("test_features.pkl", "rb") as test_features:
        test_features = pickle.load(test_features)

    
    
    #test_data = pd.concat([test_features, input_data], ignore_index=True)
   # test_data_encoded = pd.concat([test_features.reset_index(drop=True).drop(categorical_columns, axis=1), 
   #                            pd.DataFrame(ohe.fit_transform(test_features[categorical_columns]), 
   #                                         columns=ohe.get_feature_names_out(categorical_columns))], axis=1)
   # 
    #st.write(ohe.column)
   #online_new_df=pd.DataFrame(ohe.fit_transform(test_features), columns=ohe.get_feature_names_out(categorical_columns))
   #test_data_encoded=pd.concat([online_new_df.reset_index(drop=True).drop(categorical_columns), online_new_df.reset_index(drop=True)], axis=1)


    #shap_values = explainer(test_data)
    test_data = pd.concat([test_features, df_encoded], ignore_index=True)

    shap_values = explainer_last(test_data)
    #shap_values = explainer_last(test_data)



    fig, ax = plt.subplots(figsize=(10, 6))
    shap.waterfall_plot(shap_values[-1,:,1], show=False)

    st.info("You can find the Shap Explanation of your prediction!")
    st.pyplot(fig)

else:
    st.markdown("Please click the *Submit Button*!")


#---------------ForBatch----------------------

    st.header("Batch Prediction")

uploaded_file = st.file_uploader("**Upload your file**", type="csv")

if uploaded_file is not None:

    batch_df = pd.read_csv(uploaded_file)

    columns = ['Churn','Tenure','PreferredLoginDevice','CityTier','WarehouseToHome','PreferredPaymentMode','Gender','HourSpendOnApp','NumberOfDeviceRegistered','PreferedOrderCat','SatisfactionScore','MaritalStatus','NumberOfAddress','Complain','OrderAmountHikeFromlastYear','CouponUsed','OrderCount','DaySinceLastOrder','CashbackAmount']
   
    batch_df = batch_df[columns]

   # if(batch_df['OrderCount']!=0):
    couponPerOrder_batch=batch_df['CouponUsed']/batch_df['OrderCount']
    #else:
    #    couponPerOrder_batch=0

    batch_df.drop(columns="Churn", inplace=True)

    ohe_batch = OneHotEncoder(sparse_output=False, categories=[
    ['Mobile Phone', 'Computer'],
    ['Debit Card', 'UPI', 'Credit Card', 'Cash on Delivery', 'E wallet'],
    ['Female', 'Male'],
    ['Laptop & Accessory', 'Mobile Phone', 'Fashion', 'Grocery', 'Others'],
    ['Single', 'Divorced', 'Married']
    ])

    # kategorik sütunları fit ediyorum. üstte oluşturmuştum categorical_columns kısmını
    ohe_batch_df = pd.DataFrame(ohe_batch.fit_transform(batch_df[categorical_columns]), 
                          columns=ohe_batch.get_feature_names_out(categorical_columns))

    # dataframeleri birleştiriyorum.
    df_batch_encoded = pd.concat([batch_df.reset_index(drop=True).drop(categorical_columns, axis=1), 
                            ohe_batch_df.reset_index(drop=True)], axis=1)

    #artık manuel drop ediyorum çıkaracağım sütunları.
    df_batch_encoded=df_batch_encoded.drop(columns=[
        'PreferredPaymentMode_Cash on Delivery',
        'PreferedOrderCat_Grocery',
        'PreferredPaymentMode_UPI',
        'MaritalStatus_Divorced',
        'PreferedOrderCat_Others',
        'CouponUsed'
    ])

    #feature enginering ile oluşturduğum yeni feature ı dataframe e ekliyorum.
    df_batch_encoded['CouponPerOrder']=couponPerOrder_batch

    #henüz belirleyemediğim bir sebeple sütunlar farklı sıralamada geliyor.
    #bu yüzden doğru sıraya sokuyorum.
    last_column = [
        'Tenure', 'CityTier', 'WarehouseToHome', 'HourSpendOnApp',
        'NumberOfDeviceRegistered', 'SatisfactionScore', 'NumberOfAddress',
        'Complain', 'OrderAmountHikeFromlastYear', 'OrderCount',
        'DaySinceLastOrder', 'CashbackAmount', 'PreferredLoginDevice_Computer',
        'PreferredLoginDevice_Mobile Phone', 'PreferredPaymentMode_Credit Card',
        'PreferredPaymentMode_Debit Card', 'PreferredPaymentMode_E wallet',
        'Gender_Female', 'Gender_Male', 'PreferedOrderCat_Fashion',
        'PreferedOrderCat_Laptop & Accessory', 'PreferedOrderCat_Mobile Phone',
        'MaritalStatus_Married', 'MaritalStatus_Single', 'CouponPerOrder'
    ]

    #yeni sütun sıralamamla tekrar güncelliyorum. Verilere dokunmuyoruz, sadece sütun sıraları düzenleniyor.
    df_batch_encoded = df_batch_encoded.reindex(columns=last_column)

    
    batch_pred = rf_model.predict(df_batch_encoded[last_column])
    batch_pred_probability = rf_model.predict_proba(df_batch_encoded[last_column])

    predictions = pd.DataFrame({
    "Prediction": batch_pred,
    "Cancellation Probability": batch_pred_probability[:,1] * 100
    })
   
    st.info("You can find the result below.")
    pred_df = pd.concat([predictions, batch_df], ignore_index=True, axis=1)

    pred_columns = ["prediction", "cancellation_probability", 'Tenure','PreferredLoginDevice','CityTier','WarehouseToHome',
                    'PreferredPaymentMode','Gender','HourSpendOnApp','NumberOfDeviceRegistered','PreferedOrderCat','SatisfactionScore',
                    'MaritalStatus','NumberOfAddress','Complain','OrderAmountHikeFromlastYear','CouponUsed','OrderCount','DaySinceLastOrder',
                    'CashbackAmount']

    pred_df.columns = pred_columns
    pred_df["prediction"] = pred_df["prediction"].apply(lambda pred: "0" if pred==0 else "1")
    st.dataframe(pred_df, hide_index=True)
