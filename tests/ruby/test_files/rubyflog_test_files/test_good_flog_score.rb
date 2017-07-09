class Book
 def buy
   if available?
     puts 'buy'
   end
 end
#
 def available?
   false
 end
end