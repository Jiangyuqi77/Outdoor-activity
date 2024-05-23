import pandas as pd  
from sklearn.linear_model import LinearRegression  
  
# 读取CSV文件  
file_path = 'D:\\HONGKONG\\Research\\Air Pollution\\SVI\\NO2\\Long3.csv'  
df = pd.read_csv(file_path)  
  
# 创建一个字典来保存预测结果  
predictions = {}  
  
# 对每个pointid进行迭代  
for pointid in df['pointid'].unique():  
    # 选择当前pointid的数据  
    point_data = df[df['pointid'] == pointid]  
  
    # 检查是否有足够的数据点进行预测  
    if len(point_data) < 5:  
        continue  # 如果数据点不足5个，则跳过当前pointid的预测  
  
    # 提取年份和NO2值作为特征和目标变量  
    X = point_data['year'].values.reshape(-1, 1)  # 特征：年份  
    y = point_data['NO2'].values  # 目标变量：NO2值  
  
    # 确保数据按照年份排序  
    sorted_indices = X.argsort()  
    X = X[sorted_indices]  
    y = y[sorted_indices]  
  
    # 如果数据点不足5个，在之前的检查中就已经跳过了  
    # 所以这里可以确保至少有5个数据点进行模型的训练和预测  
  
    # 创建并训练线性回归模型  
    model = LinearRegression()  
    model.fit(X[:-1], y[:-1])  # 使用除了最后一个数据点的所有数据来训练模型  
  
    # 使用模型预测最后一个数据点的NO2值  
    predicted_no2 = model.predict(X[-1:].reshape(1, -1))[0]  # 预测第5年的值  
  
    # 将预测结果保存到字典中  
    predictions[pointid] = predicted_no2  
  
# 检查predictions字典是否为空，如果不为空则创建DataFrame  
if predictions:  
    # 将预测结果转换为DataFrame  
    predicted_df = pd.DataFrame(list(predictions.items()), columns=['pointid', 'predicted_NO2'])  
  
    # 打印预测结果  
    print(predicted_df)  
  
    # 将预测结果保存到CSV文件中  
    predicted_df.to_csv('predicted_NO2_values.csv', index=False)  
else:  
    print("没有足够的数据点来进行预测。")