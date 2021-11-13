import sys
import random
sys.path.append('../../src/python/')
from lora_radio import LoRaRadio

radio = LoRaRadio

if len(sys.argv) < 2:
    print('Usage: test_lora random_seed')

else:
    random.seed(int(sys.argv[1]))

    try:
        for i in range(3):
        # while True:
            print(random.random())
    except KeyboardInterrupt:
        pass