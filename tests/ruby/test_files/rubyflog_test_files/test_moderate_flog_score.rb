class Shop
 def inventory_missing_products
   # calculates the number of sold
   nbr_of_sold = Hash.new(0)
   receipts.each do |receipt|
     nbr_of_sold[receipt.product.name] += 1
   end
   #
   # calculates the number of stock
   nbr_in_stock = Hash.new(0)
   products_in_stock.each do |product|
     nbr_in_stock[product.name] += 1
   end
   #
   # calculate missing products
   nbr_of_bought.inject(Hash.new(0)) do |missing_of, (name, nbr)|
     missing_of[name] = nbr - nbr_of_sold - nbr_in_stock
   end
 end
end