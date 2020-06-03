In the service server quiz:

This new service will be called /move_bb8_in_square_custom

This new service will have to use service messages of the BB8CustomServiceMessage type, which is defined here:

float64 side         # The distance of each side of the square
int32 repetitions    # The number of times BB-8 has to execute the square movement when the service is called
---
bool success         # Did it achieve it?






