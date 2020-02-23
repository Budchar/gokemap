import json, random

from .models import restaurant, ratedRestaurant
from .skills import req_rsp, skillResponse, singleResponse, simple_text, SkillResponseView


class randomRestaurant(SkillResponseView):
    def make_response(self, request):
        print(request.params)
        restaurant_obj = restaurant.objects.all()
        recommendedRestaurant = random.choice(restaurant_obj)
        name = recommendedRestaurant.name
        description = f"{recommendedRestaurant.occasion}\n{recommendedRestaurant.place}\n{recommendedRestaurant.childCategory if recommendedRestaurant.childCategory else recommendedRestaurant.parentCategory}"
        url = recommendedRestaurant.url
        restaurantCard = singleResponse(name, description).web_button("상세보기", url).card()
        positive = {"name":name, "result":1}
        negative = {"name":name, "result":-1}
        response = skillResponse(Homebutton=False).input(restaurantCard).quickReply("다시 뽑기", "다시 뽑기", "5e46597292690d00016cb7ef").quickReply("👍","좋아요","5e51de30ffa7480001302067",positive).quickReply("👎","별로에요","5e51de30ffa7480001302067",negative)
        return response.default


class restaurantRating(SkillResponseView):
    def make_response(self, request):
        user = request.user_id
        extra = request.client_data()
        if extra:
            Restaurant = restaurant.objects.filter(name=extra['name']).first()
            ratedRestaurant.objects.create(restaurant=Restaurant, user_id=user, rating=str(extra["result"]))
            return simple_text(f"{extra['name']}을 평가해주셔서 감사합니다.", False)
        else: 
            return simple_text("시스템 오류입니다. joel.e에게 알려주세요!", False)
