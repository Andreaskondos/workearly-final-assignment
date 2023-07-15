import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option("display.max_rows", None)
data = pd.read_csv("liquorsales.csv")
data_df = pd.DataFrame(data)

byRegion = data_df.groupby(["zipCode", "item_number"], as_index=False).sum()

litersTotal = byRegion.groupby("zipCode", as_index=False)["liters_sold"].max()

favRegion = pd.merge(litersTotal, byRegion, how="left", on=["zipCode", "liters_sold"])[["zipCode", "item_number", "item","liters_sold"]]
favRegion = favRegion.rename(columns={"liters_sold":"total_liters_sold_in_zipCode"})

stores = data_df.groupby("store_number", as_index=False).sum()[["store_number","liters_sold"]]
totalLitersSold = stores.liters_sold.sum()
stores = stores.assign(salesPercent = lambda x:( x.liters_sold / totalLitersSold) * 100)

plt.subplot(1,2,1)
plt.bar(favRegion.zipCode, favRegion.total_liters_sold_in_zipCode, width=1000, color="aqua")
plt.ylabel("Total liters")
plt.xlabel("Zipcode plus liquor name")
plt.xticks(rotation=-10)
plt.subplot(1,2,2)
plt.pie(stores.salesPercent, labels=stores.store_number)
# plt.legend(loc='lower right', ncol=4)
plt.show()