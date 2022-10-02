from utils import get_flats_by_map, load_seen_flats, update_seen_flats

tg_token = ''
tg_chat_id = ''
minutes_horizon = 24*60
myhome_links = [
    'https://www.myhome.ge/ru/s/Сдается-в-аренду-новопостроенная-квартира?AdTypeID=3&PrTypeID=1&NeLat=41.83678511781744&NeLng=44.82439368988739&SwLat=41.73592376566032&SwLng=44.72946494844041&mapC=41.78637%2C44.77693&mapZ=12&mapOp=1&EnableMap=1&EstateTypeID=1&FCurrencyID=1&FPriceFrom=650&FPriceTo=1000&AreaSizeFrom=70&RoomNums=3&BedRoomNums=2&action_map=on',
    'https://www.myhome.ge/ru/s/Сдается-в-аренду-новопостроенная-квартира?AdTypeID=3&PrTypeID=1&NeLat=41.729581476741544&NeLng=44.717658709195064&SwLat=41.716880016435255&SwLng=44.70604689798657&mapC=41.72323%2C44.71185&mapZ=14.98889454196967&mapOp=1&EnableMap=1&EstateTypeID=1&FCurrencyID=1&FPriceTo=1000&AreaSizeFrom=70&RoomNums=3&action_map=on'
]

if __name__ == '__main__':
    seen = load_seen_flats()

    seen = get_flats_by_map(
        myhome_links,
        seen,
        minutes_horizon,
        tg_token,
        tg_chat_id
    )

    update_seen_flats(seen)



