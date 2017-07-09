class Shop
 def inventory_missing_products
    nbr_of_sold = how_many_sold_products
    nbr_in_stock = how_many_products_in_stock
    nbr_of_bought.inject(Hash.new(0)) do |missing_of, (name, nbr)|
      missing_of[name] = nbr - nbr_of_sold - nbr_in_stock
    end
 end
#
 private
 def how_many_sold_products
   receipts.inject(Hash.new(0)) do |nbr_of_sold, receipt|
     nbr_of_sold[receipt.product.name] += 1
     nbr_of_sold
   end
 end
#
 def how_many_products_in_stock
   products_in_stock.inject(Hash.new(0)) do |nbr_in_stock, product|
     nbr_in_stock[product.name] += 1
     nbr_in_stock
   end
 end
end