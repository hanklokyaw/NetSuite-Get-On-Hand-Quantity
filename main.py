from netsuite_login import download_reports
from read_files import get_latest_inventory_df, merge_df
import os
import pandas as pd
from datetime import datetime

now = datetime.now()
# Format the datetime as a string
current_time = now.strftime('%Y%m%d-%H%M')


# Set up Net Suite Login details
net_suite_username = os.getenv('NS_USERNAME')
net_suite_password = os.getenv('NS_PASSWORD')
net_suite_question_1 = os.getenv('NS_QUES1')
net_suite_answer_1 = os.getenv('NS_ANS1')
net_suite_question_2 = os.getenv('NS_QUES2')
net_suite_answer_2 = os.getenv('NS_ANS2')
net_suite_question_3 = os.getenv('NS_QUES3')
net_suite_answer_3 = os.getenv('NS_ANS3')

# Use 3 different location to download the report
inventory_on_hand = ("https://4228061.app.netsuite.com/app/common/search/searchresults.nl?searchid=898150&saverun=T&whence=")

inv_item_base_path = "C:/Users/hank.aungkyaw/Downloads/"
inv_item_prefix = "AnatometalOnHandHKResults"  # Exclude random suffix numbers

sku_list = pd.read_excel("C:/Users/hank.aungkyaw/Desktop/Get On Hand Quantity.xlsx")

download_reports(net_suite_username,
                 net_suite_password,
                 net_suite_question_1,
                 net_suite_answer_1,
                 net_suite_question_2,
                 net_suite_answer_2,
                 net_suite_question_3,
                 net_suite_answer_3,
                 inventory_on_hand)


inventory_df = get_latest_inventory_df(inv_item_base_path, inv_item_prefix)

final_df = merge_df(inventory_df, sku_list)

final_df.to_excel(f"C:/Users/hank.aungkyaw/Desktop/Get On Hand Quantity Result {current_time}.xlsx", index=False)
print("Generated Result File.")
