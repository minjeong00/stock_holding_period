# import pandas as pd
# pd.set_option("display.max_row", 100)
# pd.set_option("display.max_column", 100)
#
# train = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/데이콘_NH/stk_hld_train.csv")
# test = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/데이콘_NH/stk_hld_test.csv")
# cus = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/데이콘_NH/cus_info.csv")
# iem = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/데이콘_NH/iem_info_20210902.csv")
# hist = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/데이콘_NH/stk_bnc_hist.csv")
#
# submission = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/데이콘_NH/sample_submission.csv")
#
# id_거래량_value = hist['act_id'].value_counts().values
# id_거래량_index = hist['act_id'].value_counts().index
# id_거래량 = pd.DataFrame({'act_id' : id_거래량_index, '거래량' : id_거래량_value})
#
# train = pd.merge(train, id_거래량, how = "left", on = ["act_id"])
# test = pd.merge(test, id_거래량, how = "left", on = ["act_id"])