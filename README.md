# Final-Assignment

Below i explain my solution:

- ###### Step 1.

Working with MySQL i did the following query to extract the data that i wanted.

    use	liquorsales;
    with q1 as ( SELECT city, (zip_code * 10) as zipCode , item_number, item_description, store_name, store_number, bottles_sold, volume_sold_liters from finance_liquor_sales where date < "2020/01/01" AND date > "2015/12/31") SELECT city, zipCode, store_name, store_number, item_number, item_description as item, volume_sold_liters as liters_sold from q1;

- ###### Step 2.

I read the csv file with the extracted data and i group them by zipCode and item_number to sum.

    data = pd.read_csv("liquorsales.csv")
    data_df = pd.DataFrame(data)

    byRegion = data_df.groupby(["zipCode", "item_number"], as_index=False).sum()

- ###### Step 3.

With step two i have by region (zipCode) the total consumption of each liquor so i only need to get the max from each total consumption to get the favorite. If just use the max() method in byRegion df after grouping it, it will give me false data because it will give the max from each columns, i will have wrong item_number and item.

So i create a second df with only zipCode and the maximum liters_sold and then i merge it with byRegion df to create the df favRegion with the favorite of each region.

    litersTotal = byRegion.groupby("zipCode", as_index=False)["liters_sold"].max()

    favRegion = pd.merge(litersTotal, byRegion, how="left", on=["zipCode", "liters_sold"])[["zipCode", "item_number", "item","liters_sold"]]
    favRegion = favRegion.rename(columns={"liters_sold":"total_liters_sold_in_zipCode"})

- ###### Step 4.

I groupby my data again but by store and use sum() method to calculate the total liters of liquor sold by each store. After i calculate the total liters sold in total by all the stores and i sue assign() method to add a column with the percentage of liters of liquor sold by each store.

    stores = data_df.groupby("store_number", as_index=False).sum()[["store_number","liters_sold"]]
    totalLitersSold = stores.liters_sold.sum()
    stores = stores.assign(salesPercent = lambda x:( x.liters_sold / totalLitersSold) * 100)

- ###### Step 5.

Finally after having gathered all the wanted data i illustrate them using matplotlib's pyplot methods.

      plt.subplot(1,2,1)
      plt.bar(favRegion.zipCode, favRegion.total_liters_sold_in_zipCode, width=1000, color="aqua")
      plt.ylabel("Total liters")
      plt.xlabel("Zipcode plus liquor name")
      plt.xticks(rotation=-10)
      plt.subplot(1,2,2)
      plt.pie(stores.salesPercent, labels=stores.store_number)
      # plt.legend(loc='lower right', ncol=4)
      plt.show()
