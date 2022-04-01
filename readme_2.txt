categories

id | name    
1     tacos
2     quick
3     chinese

venues

id | name    | price    
1     chipotle    2
2     wok 88    3

VenueCategory
venue_categories
id | venue_id | category_id

1      1           1
2      1           2
3       2          3
4       2          2

create_venue_categories(venue, categories)