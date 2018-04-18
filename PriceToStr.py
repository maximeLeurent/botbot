def priceToStr( price):
    kamas = str(price)
    firstSpace = len(kamas)%3
    if(kamas and len(kamas)%3 ==0 ):
        firstSpace = 3
    textKamas = kamas[0:firstSpace]
    while firstSpace < len(kamas):
        textKamas += " " +kamas[firstSpace:firstSpace+3]
        firstSpace +=3
    textKamas += " K"
    return textKamas
